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
    check = ""
    if intake == 1:
        targets = [4, 6, 8, 9]
        check = "sleep_hours"

    elif intake == 2:
        targets = [17, 19, 22, 25, 26]
        check = "age"
    elif intake == 3:
        targets = [5, 10, 15, 20, 25, 30, 40, 50]
        check = "bmi"
    elif intake == 4:
        mostImportant()

    if intake != 4:
        dataCheck(targets, check)


def dataCheck(targets, check):
    # Open the CSV file in read mode
    # The file needs to be opened inside the functions, mainly, because of the scoping rules behind the with operator
    # you can do it without but, thats mroe effort that I want to put in.

    with open("student_academic_performance_1M.csv", mode="r") as file:
        # Create a CSV reader object
        # we will do 4> 4-6 6-8, 8+
        bins = [[0, 0.0, 0.0] for j in range(len(targets))]
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            for target in range(len(targets)):
                if float(row[check]) <= targets[target]:
                    bins[target][0] += 1
                    bins[target][1] += float(row["final_gpa"])
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
                )
            else:
                print("the target", targets[i], "has no members")

        print(bins)


def mostImportant():
    # count , sleep_hours,age,bmi
    bins = [[0, 0.0, 0.0, 0.0] for j in range(5)]

    with open("student_academic_performance_1M.csv", mode="r") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if float(row["final_gpa"]) >= 4:
                bins[0][0] += 1
                bins[0][1] += float(row["sleep_hours"])
                bins[0][2] += float(row["age"])
                bins[0][3] += float(row["bmi"])
            elif float(row["final_gpa"]) >= 3:
                bins[1][0] += 1
                bins[1][1] += float(row["sleep_hours"])
                bins[1][2] += float(row["age"])
                bins[1][3] += float(row["bmi"])
            elif float(row["final_gpa"]) >= 2:
                bins[2][0] += 1
                bins[2][1] += float(row["sleep_hours"])
                bins[2][2] += float(row["age"])
                bins[2][3] += float(row["bmi"])
            elif float(row["final_gpa"]) >= 1:
                bins[3][0] += 1
                bins[3][1] += float(row["sleep_hours"])
                bins[3][2] += float(row["age"])
                bins[3][3] += float(row["bmi"])
            else:
                bins[4][0] += 1
                bins[4][1] += float(row["sleep_hours"])
                bins[4][2] += float(row["age"])
                bins[4][3] += float(row["bmi"])

        for x in range(5):
            for y in range(1, 4):
                bins[x][y] = bins[x][y] / bins[x][0]
                print(x, y)


if __name__ == "__main__":
    main()
