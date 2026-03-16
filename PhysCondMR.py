import findspark
import os
import time
import csv
from pyspark.sql import SparkSession
os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-21-openjdk"
from pyspark.sql.functions import round, when, col, avg, col,lit,concat,count

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
        1,
        2,
        5,
        10,
        1,
        1,
        1,
        1,
        2,
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


def dataCheck(target, range, spark, df):
    sc = spark.sparkContext

    df_grouped = (
        df.withColumn("bracket_start", (col(str(target)) / range).cast("int") * range)
        .withColumn(str(target), concat(col("bracket_start"),lit("-"),(col("bracket_start") + range)))
        .groupBy(str(target), "bracket_start") .avg("final_gpa", "standardized_exam_score", "improvement_next_term").orderBy("bracket_start").drop("bracket_start"))
    df_grouped.show()

    print("the difference between the last and first row with regards to gpa is: ",df_grouped.select("avg(final_gpa)").tail(1).pop(0).__getitem__("avg(final_gpa)")-df_grouped.select("avg(final_gpa)").head(1).pop(0).__getitem__("avg(final_gpa)"))
    print("the difference between the last and first row with regards to standardized_exam_score is: ",
          df_grouped.select("avg(standardized_exam_score)").tail(1).pop(0).__getitem__("avg(standardized_exam_score)") - df_grouped.select(
              "avg(standardized_exam_score)").head(1).pop(0).__getitem__("avg(standardized_exam_score)"))
    print("the difference between the last and first row with regards to improvement_next_term is: ",
          df_grouped.select("avg(improvement_next_term)").tail(1).pop(0).__getitem__("avg(improvement_next_term)") - df_grouped.select(
              "avg(improvement_next_term)").head(1).pop(0).__getitem__("avg(improvement_next_term)"))


main()