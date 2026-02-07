import csv


def main():
    sleep_hours()


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


if __name__ == "__main__":
    main()
