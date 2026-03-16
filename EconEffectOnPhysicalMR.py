import csv
import os
import findspark
import time
os.environ["SPARK_HOME"] = "./spark-3.3.1-bin-hadoop3"
os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-8-openjdk-amd64"
findspark.init()
from pyspark import SparkConf, SparkContext

metric = 33
bins = []

def get_metric_range(metric_val):
    if metric_val <= bins[0]:
        return "0-" + str(bins[0])
    elif metric_val <= bins[1]:
        return str(bins[0]) + "-" + str(bins[1])
    elif metric_val <= bins[2]:
        return str(bins[1]) + "-" + str(bins[2])
    elif metric_val <= bins[3]:
        return str(bins[2]) + "-" + str(bins[3])
    elif metric_val <= bins[4]:
        return str(bins[3]) + "-" + str(bins[4])
    else:
        return "11+"

# filters a given line down to only the fields we need
def parse_line(line):
    fields = line.split(",")
    measured_metric = float(fields[metric])
    sleep_qual = float(fields[26])
    illness_days = float(fields[24])
    junk_food_freq = float(fields[22])
    return (measured_metric, sleep_qual, illness_days, junk_food_freq)


#grabs the right bins based on the metric we're assessing
def select_bins(intake):
    if intake == 1:
        bins = [0.2, 0.4, 0.6, 0.8, 1]
    elif intake == 2:
        bins = [1, 2, 3, 4, 5]
    elif intake == 3:
        bins = [2, 4, 6, 8, 10]
    elif intake == 4:
        bins = [2, 4, 6, 8, 10]
    elif intake == 5:
        bins = [2, 4, 6, 8, 10]
    return bins

#finds the "numerical" position of the metric being measured based on its name
def find_metric(header, metric_name):
    fields = header.split(",")
    for x in range(52):
        if(fields[x] == metric_name):
            return x

def main():
    global metric
    global bins

    intake = int(input("Choose which economic factor's effect on physical conditions to analyse: \n 1. Family Income \n 2. Parent Education \n 3. Part-time Job Hours \n 4. Parent Involvement (*) \n 5. Financial Stress (*)"))
    checkList = ["family_income", "parent_education", "part_time_job_hours", "parent_involvement", "financial_stress"]
    metric_name = checkList[intake-1]
    bins = select_bins(intake)


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
    print(end-start)

main()