import csv
import os
import findspark
os.environ["SPARK_HOME"] = "./spark-3.3.1-bin-hadoop3"
os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-8-openjdk-amd64"
findspark.init()
from pyspark.sql import SparkSession
from pyspark.sql.functions import round,when,col,avg

# This program will take in a file, a target and the bins you want, and will find the average final gpa of them
# your targets will be inclsive so if your bin has 25 it will be >= 25 and be put into the 25 bin
# the last bin will be treated as a "none of the above sections" if done correctly it will be > than largest check, this is done to try to catch all the data
# and obviosuly your first bin will include anything smaller than it aswell
def main():
    #Setting up spark to use MapReduce to process the data
    spark = SparkSession.builder.master("local[*]").getOrCreate()
    spark.conf.set("spark.sql.repl.eagerEval.enabled", True) #  This will format our output tables a bit nicer when not using the show() method
    spark
    df = spark.read.csv("student_academic_performance_1M.csv", header = True, mode = "DROPMALFORMED",inferSchema=True)

    intake = int(input("Choose which economic factor's effect on physical conditions to analyse: \n 1. Family Income \n 2. Parent Education \n 3. Part-time Job Hours \n 4. Parent Involvement (*) \n 5. Financial Stress (*) \nOr enter '10' to compare averages for all of the above with different GPAs/Exam Results \n"))
    bins = [0]
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
    checkList = ["family_income", "parent_education", "part_time_job_hours", "parent_involvement", "financial_stress"]
    target = checkList[intake-1]
    dataCheck(target, bins, spark, df)

def dataCheck(target, bins, spark, df):
    sc = spark.sparkContext
    average = df.groupBy(
        when((col(target) >= 0) & (col(target) <= bins[0]), "0-"+str(bins[0]))
        .when((col(target) > bins[0]) & (col(target) <= bins[1]), str(bins[0]) + "-" + str(bins[1]))
        .when((col(target) > bins[1]) & (col(target) <= bins[2]), str(bins[1]) + "-" + str(bins[2]))
        .when((col(target) > bins[2]) & (col(target) <= bins[3]), str(bins[2]) + "-" + str(bins[3]))
        .when((col(target) > bins[3]) & (col(target) <= bins[4]), str(bins[3]) + "-" + str(bins[4]))
        .otherwise(str(bins[4]) + "+").alias(target)).avg("sleep_quality", "illness_days", "junk_food_freq").sort().show()

main()

    