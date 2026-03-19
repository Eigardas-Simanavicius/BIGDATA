import csv
import os
import findspark
import time

os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-21-openjdk"
findspark.init()

from pyspark import SparkConf, SparkContext

metric = 33
bins = []
GPA = 42
EXAM_SCORE = 43
IMPROVEMENT_SCORE = 44


def get_metric_range(metric_val):
    for i in range(len(bins) - 1):
        if metric_val <= bins[i]:
            return str(bins[i]) + "-" + str(bins[i + 1])
    else:
        return str(bins[len(bins) - 1]) + ".1 +"


# filters a given line down to only the fields we need
def parse_line(line):
    fields = line.split(",")
    measured_metric = float(fields[metric])
    f1 = float(fields[GPA])
    f2 = float(fields[EXAM_SCORE])
    f3 = float(fields[IMPROVEMENT_SCORE])
    return measured_metric, f1, f2, f3


def select_bins(intake):
    binList = [
        [1, 2, 4, 6, 8, 10, 12, 14],      # online_course_hours
        [1, 3, 6, 10, 15, 20, 25, 30],    # lms_login_frequency
        [0.5, 1, 2, 3, 4, 5, 6],          # coding_practice_hours
        [0, 1],                           # ai_tool_usage
        [2, 3, 4, 5, 6, 7, 8, 9],         # digital_literacy
        [0.5, 1, 2, 4, 6, 8, 10, 12],     # video_watch_hours
        [1, 3, 5, 7, 9],                  # forum_participation
        [1, 2, 3]                         # device_availability
    ]
    return binList[intake]


# finds the "numerical" position of the metric being measured based on its name
def find_metric(header, metric_name):
    fields = header.split(",")
    print(fields[GPA])
    for x in range(len(fields)):
        if fields[x] == metric_name:
            return x


def main():
    global metric
    global bins

    intake = int(input(
        "Choose which academic effort factor to analyse: \n"
        " 1. Online Course Hours \n"
        " 2. LMS Login Frequency \n"
        " 3. Coding Practice Hours \n"
        " 4. AI Tool Usage \n"
        " 5. Digital Literacy \n"
        " 6. Video Watch Hours \n"
        " 7. Forum Participation \n"
        " 8. Device Availability \n"
    ))

    checkList = [
        "online_course_hours",
        "lms_login_frequency",
        "coding_practice_hours",
        "ai_tool_usage",
        "digital_literacy",
        "video_watch_hours",
        "forum_participation",
        "device_availability"
    ]

    metric_name = checkList[intake - 1]
    bins = select_bins(intake - 1)

    conf = SparkConf().setAppName("Student Data Analysis")
    sc = SparkContext(conf=conf)

    # Load CSV
    data = sc.textFile("student_academic_performance_1M.csv")
    header = data.first()
    metric = find_metric(header, metric_name)
    rows = data.filter(lambda line: line != header)

    start = time.time()

    # parses every row
    parsed = rows.map(parse_line)

    # uses the Map function to create key value pairs, which look like (metric, (target1, target2, target3, counter))
    # counter used for averages later
    key_val_pairs = parsed.map(lambda x: (get_metric_range(x[0]), (x[1], x[2], x[3], 1)))

    # reduces, resulting in tuples of (metric_range, (target1_sum, target2_sum, target3_sum, number of rows in range))
    range_totals = key_val_pairs.reduceByKey(
        lambda a, b: (a[0] + b[0], a[1] + b[1], a[2] + b[2], a[3] + b[3])
    )

    # calculates average for each range
    range_averages = range_totals.mapValues(lambda x: (x[0] / x[3], x[1] / x[3], x[2] / x[3]))

    # collects and displays results
    results = range_averages.collect()

    print(f"\nAverage Final GPA, Standardized Exam Score, and Improvement Next Term by {metric_name} Range:")
    print("-" * 80)
    for metric_range, averages in sorted(results):
        avg_gpa, avg_exam, avg_improvement = averages
        print(
            f"{metric_name} Range {metric_range}: "
            f"Final GPA: {avg_gpa:.2f}, "
            f"Standardized Exam Score: {avg_exam:.2f}, "
            f"Improvement Next Term: {avg_improvement:.2f}"
        )

    sc.stop()
    end = time.time()
    print("time taken ", end - start)


main()