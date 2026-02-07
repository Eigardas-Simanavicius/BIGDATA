import csv


def main():
    print("choose which data set to analyse /n 1. sleep_hours /n 2.Age")
    intake = input()
    if intake == 1:
        sleep_hours()
    elif intake == 2:
        age()


def sleep_hours():
    # Open the CSV file in read mode
    # The file needs to be opened inside the functions, mainly, because of the scoping rules behind the with operator
    # you can do it without but, thats mroe effort that I want to put in.
    with open("student_academic_performance_1M.csv", mode="r") as file:
        # Create a CSV reader object
        # we will do 4> 4-6 6-8, 8+
        bins = [[0, 0.0], [0, 0.0], [0, 0.0], [0, 0.0]]
        results = [0, 0, 0, 0]
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if float(row["sleep_hours"]) < 4:
                bins[0][0] += 1
                bins[0][1] += float(row["final_gpa"])
            elif float(row["sleep_hours"]) < 6:
                bins[1][0] += 1
                bins[1][1] += float(row["final_gpa"])
            elif float(row["sleep_hours"]) < 8:
                bins[2][0] += 1
                bins[2][1] += float(row["final_gpa"])
            elif float(row["sleep_hours"]) >= 8:
                bins[3][0] += 1
                bins[3][1] += float(row["final_gpa"])

        for i in range(4):
            results[i] = bins[i][1] / bins[i][0]
            print("The results for bin ", i, " are ", (bins[i][1] / bins[i][0]))


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

        for i in range(4):
            results[i] = bins[i][1] / bins[i][0]
            print("The results for bin ", i, " are ", (bins[i][1] / bins[i][0]))


if __name__ == "__main__":
    main()
