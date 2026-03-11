import findspark
import os
import time
import csv
from pyspark.sql import SparkSession
os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-21-openjdk"
from pyspark.sql.functions import round, when, col, avg

findspark.init()

def main():
    #Setting up spark to use MapReduce to process the data
    spark = SparkSession.builder.master("local[*]").getOrCreate()
    spark.conf.set("spark.sql.repl.eagerEval.enabled", True) #  This will format our output tables a bit nicer when not using the show() method
    spark
    df = spark.read.csv("student_academic_performance_1M.csv", header = True, mode = "DROPMALFORMED",inferSchema=True)

    intake = int(input("Choose which economic factor's effect on physical conditions to analyse: \n 1. Family Income \n 2. Parent Education \n 3. Part-time Job Hours \n 4. Parent Involvement (*) \n 5. Financial Stress (*) \nOr enter '10' to compare averages for all of the above with different GPAs/Exam Results \n"))
    bins = [0]
    targetList = [
        [4, 5, 6, 7, 8, 9],
        [17, 19, 22, 25, 26],
        [5, 10, 15, 20, 25, 30, 40, 50],
        [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        [2, 4, 6, 8, 10, 12, 14, 16],
    ]
    checkList = [
        "sleep_hours",
        "age",
        "bmi",
        "physical_activity",
        "screen_time",
        "stress_index",
        "mental_stress",
        "sleep_quality",
        "illness_days",
    ]
    start = time.time()
    dataCheck(checkList[intake-1], targetList[intake-1], spark, df)
    end = time.time()
    print("time taken, with spark", (end - start))


def dataCheck(target, bins, spark, df):
    sc = spark.sparkContext
    average = df.groupBy(
        when((col(target) >= 0) & (col(target) <= bins[0]), "0-"+str(bins[0]))
        .when((col(target) > bins[0]) & (col(target) <= bins[1]), str(bins[0]) + "-" + str(bins[1]))
        .when((col(target) > bins[1]) & (col(target) <= bins[2]), str(bins[1]) + "-" + str(bins[2]))
        .when((col(target) > bins[2]) & (col(target) <= bins[3]), str(bins[2]) + "-" + str(bins[3]))
        .when((col(target) > bins[3]) & (col(target) <= bins[4]), str(bins[3]) + "-" + str(bins[4]))
        .otherwise(str(bins[4]) + "+").alias(target)).avg("sleep_quality", "illness_days", "junk_food_freq").sort(target).show()

main()