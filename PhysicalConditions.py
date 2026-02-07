import csv


def main():
    print("Hello World!")
    sleep_hours()


def sleep_hours():
    # Open the CSV file in read mode
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
                print(float(row["sleep_hours"]))
                bins[3][0] += 1
                bins[3][1] += float(row["final_gpa"])

        # Skip the header row (if there is one)
        next(csv_reader, None)
        for i in range(4):
            results[i] = bins[i][1] / bins[i][0]
        print(results)


if __name__ == "__main__":
    main()
