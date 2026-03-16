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
IMPORVMENT_SCORE = 44

def get_metric_range(metric_val):
    for i in range(len(bins)-1):
        if metric_val <= bins[i]:
            return str(bins[i]) + "-" + str(bins[i+1])
    else:
        return str(bins[4]) + ".1 +"


# filters a given line down to only the fields we need
def parse_line(line):
    fields = line.split(",")
    measured_metric = float(fields[metric])
    f1 = float(fields[GPA])
    f2 = float(fields[EXAM_SCORE])
    f3 = float(fields[IMPORVMENT_SCORE])
    return measured_metric, f1, f2, f3


def select_bins(intake):
    binList = [
    [4, 5, 6, 7, 8, 9],
    [17, 19, 22, 25, 26],
    [5, 10, 15, 20, 25, 30, 40, 50],
    [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    [2, 4, 6, 8, 10, 12, 14, 16]]
    return binList[intake]

#finds the "numerical" position of the metric being measured based on its name
def find_metric(header, metric_name):
    fields = header.split(",")
    print(fields[GPA])
    for x in range(52):
        if fields[x] == metric_name:
            return x

def main():
    global metric
    global bins

    intake = int(input("Choose which economic factor's effect on physical conditions to analyse: \n 1. Family Income \n 2. Parent Education \n 3. Part-time Job Hours \n 4. Parent Involvement (*) \n 5. Financial Stress (*)"))
    checkList = ["sleep_hours", "parent_education", "part_time_job_hours", "parent_involvement", "financial_stress"]
    metric_name = checkList[intake-1]
    bins = select_bins(intake-1)


    conf = SparkConf().setAppName("Student Data Analysis")
    sc = SparkContext(conf=conf)

    # Load CSV
    data = sc.textFile("student_academic_performance_1M.csv")
    header = data.first()
    metric = find_metric(header, metric_name)
    rows = data.filter(lambda line: line != header)

    start = time.time()

    #parses every row
    parsed = rows.map(parse_line)

    #uses the Map function to create key value pairs, which look like (metric, (target1, target2, target3, counter))
    #counter used for averages later
    key_val_pairs = parsed.map(lambda x: (get_metric_range(x[0]), (x[1], x[2], x[3], 1)))

    #reduces, resulting in tuples of (metric_range, (target1_sum, target2_sum, target3_sum, number of rows in range))
    range_totals = key_val_pairs.reduceByKey(
        lambda a, b: (a[0] + b[0], a[1] + b[1], a[2] + b[2], a[3] + b[3])
    )

    # calculates average for each range
    range_averages = range_totals.mapValues(lambda x: (x[0] / x[3], x[1] / x[3], x[2] / x[3]))

    # collects and displays results
    results = range_averages.collect()

    print(f"\nAverage Sleep Quality, Illness Days, and Junk Food Frequency by {metric_name} Range:")
    print("-" * 60)
    for metric_range, averages in sorted(results):
        avg_sleep, avg_illness, avg_junk_food = averages
        print(f"{metric_name} Range {metric_range}: Sleep Quality: {avg_sleep:.2f}, Illness Days: {avg_illness:.2f}, Junk Food Frequency: {avg_junk_food:.2f}")

    sc.stop()
    end = time.time()
    print("time taken ",end-start)

main()
