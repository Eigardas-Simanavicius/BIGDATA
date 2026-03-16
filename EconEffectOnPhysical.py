import csv


# This program will take in a file, a target and the bins you want, and will find the average final gpa of them
# your targets will be inclsive so if your bin has 25 it will be >= 25 and be put into the 25 bin
# the last bin will be treated as a "none of the above sections" if done correctly it will be > than largest check, this is done to try to catch all the data
# and obviosuly your first bin will include anything smaller than it aswell
def main():
    intake = int(
        input("Choose which economic factor's effect on physical conditions to analyse: \n 1. Family Income \n 2. Parent Education \n 3. Part-time Job Hours \n 4. Parent Involvement (*) \n 5. Financial Stress (*) \nOr enter '10' to compare averages for all of the above with different GPAs/Exam Results \n")
    )
    targets = [0]
    checkList = ["family_income", "parent_education", "part_time_job_hours", "parent_involvement", "financial_stress"]
    if intake == 1:
        targets = [0.2, 0.4, 0.6, 0.8, 1]
    elif intake == 2:
        targets = [0, 1, 2, 3, 4]
    elif intake == 3:
        targets = [2, 4, 6, 8, 10, 12]
    elif intake == 4:
        targets = [2, 4, 6, 8, 10]
    elif intake == 5:
        targets = [2, 4, 6, 8, 10]
    dataCheck(targets, checkList[intake - 1])

def dataCheck(targets, check):
    # Open the CSV file in read mode
    # The file needs to be opened inside the functions, mainly, because of the scoping rules behind the with operator
    # you can do it without but, thats mroe effort that I want to put in.

    with open("student_academic_performance_1M.csv", mode="r") as file:
        # Create a CSV reader object
        bins = [[0, 0.0, 0.0, 0.0] for j in range(len(targets))]
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            for target in range(len(targets)):
                if float(row[check]) <= targets[target]:
                    bins[target][0] += 1
                    bins[target][1] += float(row["illness_days"])
                    bins[target][2] += float(row["sleep_quality"])
                    bins[target][3] += float(row["junk_food_freq"])
                    break
                elif target == len(targets) - 1:
                    bins[target][0] += 1
                    bins[target][1] += float(row["illness_days"])
                    bins[target][2] += float(row["sleep_quality"])
                    bins[target][3] += float(row["junk_food_freq"])

        for i in range(len(targets)):
            if bins[i][1] != 0 and bins[i][0] != 0:
                print(
                    "The illness days for bin for target",
                    targets[i],
                    " are ",
                    (bins[i][1] / bins[i][0]),
                    " and the sleep quality is",
                    (bins[i][2] / bins[i][0]),
                    " and the junk food frequency is",
                    (bins[i][3] / bins[i][0]),
                )
            else:
                print("the target", targets[i], "has no members")

main()