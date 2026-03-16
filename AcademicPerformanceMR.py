import csv
import os
import findspark

os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-21-openjdk"
findspark.init()

from pyspark.sql import SparkSession
from pyspark.sql.functions import when, col, avg


def main():

    # start spark
    spark = SparkSession.builder.master("local[*]").getOrCreate()

    df = spark.read.csv(
        "student_academic_performance_1M.csv",
        header=True,
        mode="DROPMALFORMED",
        inferSchema=True
    )

    intake = int(input(
        "Choose which academic effort variable to analyse:\n"
        "1. Online Course Hours\n"
        "2. LMS Login Frequency\n"
        "3. Coding Practice Hours\n"
        "4. AI Tool Usage\n"
        "5. Digital Literacy\n"
        "6. Video Watch Hours\n"
        "7. Forum Participation\n"
        "8. Device Availability\n"
    ))

    bins = [0]

    if intake == 1:
        bins = [1,2,4,6,8]
    elif intake == 2:
        bins = [1,3,6,10,15]
    elif intake == 3:
        bins = [1,2,3,4,5]
    elif intake == 4:
        bins = [0,1]
    elif intake == 5:
        bins = [2,4,6,8]
    elif intake == 6:
        bins = [1,2,4,6,8]
    elif intake == 7:
        bins = [1,3,5,7,9]
    elif intake == 8:
        bins = [1,2,3]

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

    target = checkList[intake-1]

    dataCheck(target, bins, spark, df)


def dataCheck(target, bins, spark, df):
    average = df.groupBy(
        when((col(target) >= 0) & (col(target) <= bins[0]), "0-" + str(bins[0]))
        .when((col(target) > bins[0]) & (col(target) <= bins[1]), str(bins[0]) + "-" + str(bins[1]))
        .when((col(target) > bins[1]) & (col(target) <= bins[2]), str(bins[1]) + "-" + str(bins[2]))
        .when((col(target) > bins[2]) & (col(target) <= bins[3]), str(bins[2]) + "-" + str(bins[3]))
        .when((col(target) > bins[3]) & (col(target) <= bins[4]), str(bins[3]) + "-" + str(bins[4]))
        .otherwise(str(bins[4]) + "+").alias(target)).avg("final_gpa", "standardized_exam_score","improvement_next_term").sort(target).show()


main()