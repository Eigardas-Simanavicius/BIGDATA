import csv


def main():
    print("Hello World!")
    csv = setup()
    sleepHours(csv)


def setup():
    # Open the CSV file in read mode
    with open("example.csv", mode="r") as file:
        # Create a CSV reader object
        csv_reader = csv.reader(file)

        # Skip the header row (if there is one)
        next(csv_reader, None)
        return csv_reader


def sleepHours(csv):
    filtered_data = [row for row in csv if int(row["sleep_hours"]) > 25]


if __name__ == "__main__":
    main()
