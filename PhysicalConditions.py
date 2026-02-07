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

    dataCheck(targets, check)


def dataCheck(targets, check):
    # Open the CSV file in read mode
    # The file needs to be opened inside the functions, mainly, because of the scoping rules behind the with operator
    # you can do it without but, thats mroe effort that I want to put in.

    with open("student_academic_performance_1M.csv", mode="r") as file:
        # Create a CSV reader object
        # we will do 4> 4-6 6-8, 8+
        bins = [[0, 0.0] for j in range(len(targets))]
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

        print(bins)
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


def age():
    # Open the CSV file in read mode
    # The file needs to be opened inside the functions, mainly, because of the scoping rules behind the with operator
    # you can do it without but, thats mroe effort that I want to put in.
    with open("student_academic_performance_1M.csv", mode="r") as file:
        # Create a CSV reader object
        # we will do 18> 18-19, 20-22, 22-25,26+
        bins = [[0, 0.0], [0, 0.0], [0, 0.0], [0, 0.0], [0, 0.0]]
        results = [0, 0, 0, 0, 0]
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if float(row["age"]) < 18:
                bins[0][0] += 1
                bins[0][1] += float(row["final_gpa"])
            elif float(row["age"]) <= 19:
                bins[1][0] += 1
                bins[1][1] += float(row["final_gpa"])
            elif float(row["age"]) <= 22:
                bins[2][0] += 1
                bins[2][1] += float(row["final_gpa"])
            elif float(row["age"]) >= 25:
                bins[3][0] += 1
                bins[3][1] += float(row["final_gpa"])
            elif float(row["age"]) >= 26:
                bins[4][0] += 1
                bins[4][1] += float(row["final_gpa"])

        for i in range(len(bins) - 1):
            if bins[i][1] != 0 and bins[i][0] != 0:
                print("The results for bin ", i, " are ", (bins[i][1] / bins[i][0]))
            else:
                print("bin", i, "contains no members ")


if __name__ == "__main__":
    main()
