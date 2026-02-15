import csv


# This program will take in a file, a target and the bins you want, and will find the average final gpa of them
# your targets will be inclsive so if your bin has 25 it will be >= 25 and be put into the 25 bin
# the last bin will be treated as a "none of the above sections" if done correctly it will be > than largest check, this is done to try to catch all the data
# and obviosuly your first bin will include anything smaller than it aswell
def main():
    intake = int(
        input("Choose which data set to analyse: \n 1. Family Income \n 2. Parent Education \n 3. Internet Access \n 4. Private Tuition \n 5. Tuition Hours (*) \n 6. Parent Involvement (*) \n 7. Financial Stress (*) \nOr enter '10' to compare averages for all of the above with different GPAs/Exam Results \n")
    )
    targets = [0]
    checkList = ["family_income", "parent_education", "internet_access", "private_tuition", "tuition_hours", "parent_involvement", "financial_stress"]
    if intake == 1:
        targets = [0.2, 0.4, 0.6, 0.8, 1]
    elif intake == 2:
        targets = [0, 1, 2, 3, 4]
    elif intake == 3:
        targets = [0, 1]
    elif intake == 4:
        targets = [0, 1]
    elif intake == 5:
        targets = [2, 4, 6, 8, 10, 12]
    elif intake == 6:
        targets = [2, 4, 6, 8, 10]
    elif intake == 7:
        targets = [2, 4, 6, 8, 10]
    elif intake == 10:
        intake = int(input("Check using:\n 1. Final Gpa, or\n 2. Exam scores (*)\n"))
        if intake == 1:
            check = "final_gpa"
        else:
            check = "standardized_exam_score"

        mostImportant(checkList, check)
        intake = 10
    if intake != 10:
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
                    bins[target][1] += float(row["final_gpa"])
                    bins[target][2] += float(row["standardized_exam_score"])
                    break
                elif target == len(targets) - 1:
                    bins[target][0] += 1
                    bins[target][1] += float(row["final_gpa"])
                    bins[target][2] += float(row["standardized_exam_score"])


        for i in range(len(targets)):
            if bins[i][1] != 0 and bins[i][0] != 0:
                print(
                    "The results for bin for target",
                    targets[i],
                    " are ",
                    (bins[i][1] / bins[i][0]),
                    " and the exam scores are",
                    (bins[i][2] / bins[i][0]),
                )
            else:
                print("the target", targets[i], "has no members")


def mostImportant(checkList, check):
    if check == "final_gpa":
        targets = [4, 3.5, 3, 2.5, 2, 1, 0]
    else:
        targets = [90, 80, 70, 60, 50, 40, 30, 20, 10, 0]

    bins = [[0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0] for j in range(len(targets))]

    with open("student_academic_performance_1M.csv", mode="r") as file:
        csv_reader = csv.DictReader(file)
        n = len(targets) - 1
        for row in csv_reader:
            for x in range(len(targets) + 1):
                if float(row[check]) >= targets[x]:
                    n = x
                    break

            bins[n][0] += 1
            for x in range(len(checkList)):
                bins[n][x + 1] += float(row[checkList[x]])

        for x in range(len(targets)):
            print(
                "The students with a",
                check,
                "of",
                targets[x],
                "or more and their average values are: ",
            )
            for y in range(len(checkList)):
                bins[x][y + 1] = round(bins[x][y + 1] / bins[x][0], 2)
                print(checkList[y], ":", bins[x][y + 1])

        intake = (
            input(
                "Would you like to compare the difference between best and worst students Y/N\n"
            )
        ).lower()

        if intake == "y":
            print("\n\nThe average best student vs worst student looks like this: \n")
            for y in range(len(checkList)):
                print(checkList[y], ":", bins[0][y + 1] - bins[len(bins) - 1][y + 1])


if __name__ == "__main__":
    main()
