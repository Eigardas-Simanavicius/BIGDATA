import csv


# This program will take in a file, a target and the bins you want, and will find the average final gpa of them
# your targets will be inclsive so if your bin has 25 it will be >= 25 and be put into the 25 bin
# the last bin will be treated as a "none of the above sections" if done correctly it will be > than largest check, this is done to try to catch all the data
# and obviosuly your first bin will include anything smaller than it aswell
def main():
    intake = int(
        input("choose which data set to analyse \n 1. sleep_hours \n 2.Age \n")
    )
    targets = [0]
    checkList = ["sleep_hours", "age", "bmi", "physical_activity", "screen_time"]
    if intake == 1:
        targets = [4, 5, 6, 7, 8, 9]
    elif intake == 2:
        targets = [17, 19, 22, 25, 26]
    elif intake == 3:
        targets = [5, 10, 15, 20, 25, 30, 40, 50]
    elif intake == 4:
        targets = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    elif intake == 5:
        targets = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    elif intake == 10:
        intake = int(input("check using 1. Final Gpa, or 2. Exam scores"))
        if intake == 1:
            check = "final_gpa"
        else:
            check = "standardized_exam_score"

        mostImportant(checkList, check)
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

        print(bins)


def mostImportant(checkList, check):
    if check == "final_gpa":
        targets = [4, 3.5, 3, 2.5, 2, 1, 0]
    else:
        targets = [90, 80, 70, 60, 50, 40, 30, 20, 10, 0]

    bins = [[0, 0.0, 0.0, 0.0, 0.0, 0.0] for j in range(len(targets))]

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

        for x in range(len(targets) - 1):
            print(
                "The students with a",
                check,
                " of ",
                targets[x],
                "or more and their average values are ",
            )
            for y in range(len(checkList)):
                bins[x][y + 1] = round(bins[x][y + 1] / bins[x][0], 2)
                print(checkList[y], ":", bins[x][y + 1])

        intake = (
            input(
                "would you like to compare the difference between best and worst students Y/N"
            )
        ).lower()
        if intake == "y":
            print("todo")
            # TODO


if __name__ == "__main__":
    main()
