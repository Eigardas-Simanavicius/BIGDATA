import csv


# This program will take in a file, a target and the bins you want, and will find the average final gpa of them
# your targets will be inclusive so if your bin has 25 it will be >= 25 and be put into the 25 bin
# the last bin will be treated as a "none of the above sections" if done correctly it will be > than largest check
# and obviously your first bin will include anything smaller than it as well
def main():
    # Ask user which academic effort variable they want to analyze
    intake = int(
        input(
            "Choose which data set to analyse: \n"
            " 1. Online Course Hours \n"
            " 2. LMS Login Frequency \n"
            " 3. Coding Practice Hours \n"
            " 4. AI Tool Usage \n"
            " 5. Digital Literacy \n"
            " 6. Video Watch Hours \n"
            " 7. Forum Participation \n"
            " 8. Device Availability \n"
            "Or enter '10' to compare averages for all of the above with different GPAs/Exam Results \n"
        )
    )
    # List of column names in the CSV corresponding to academic effort
    targets = [0]
    checkList = [
        "online_course_hours",
        "lms_login_frequency",
        "coding_practice_hours",
        "ai_tool_usage",
        "digital_literacy",
        "video_watch_hours",
        "forum_participation",
        "device_availability",
    ]

    #Depending on the chosen variable, define bin thresholds
    if intake == 1:
        targets = [1, 2, 4, 6, 8, 10, 12, 14]
    elif intake == 2:
        targets = [1, 3, 6, 10, 15, 20, 25, 30]
    elif intake == 3:
        targets = [0.5, 1, 2, 3, 4, 5, 6]
    elif intake == 4:
        targets = [0, 1]  # binary
    elif intake == 5:
        targets = [2, 3, 4, 5, 6, 7, 8, 9]
    elif intake == 6:
        targets = [0.5, 1, 2, 4, 6, 8, 10, 12]
    elif intake == 7:
        targets = [1, 3, 5, 7, 9]
    elif intake == 8:
        targets = [1, 2, 3]

    # Option 10: compare all variables by GPA or exam score groups
    elif intake == 10:
        intake = int(input("Check using:\n 1. Final Gpa, or\n 2. Exam scores (*)\n"))
        # Decide which performance metric to use
        if intake == 1:
            check = "final_gpa"
        else:
            check = "standardized_exam_score"
        # Run comparison for all variables
        mostImportant(checkList, check)
        intake = 10
    # If not option 10, analyze just the chosen variable
    if intake != 10:
        dataCheck(targets, checkList[intake - 1])

# This function performs bin analysis for one chosen variable
def dataCheck(targets, check):
    # Open the CSV file in read mode
    # The file needs to be opened inside the functions, mainly, because of the scoping rules behind the with operator
    # you can do it without but, thats more effort that I want to put in.
    with open("student_academic_performance_1M.csv", mode="r", newline="") as file:
        # bins: count, sum_gpa, sum_exam
        bins = [[0, 0.0, 0.0] for j in range(len(targets))]
        csv_reader = csv.DictReader(file)
        # Loop through every student
        for row in csv_reader:
            try:
                # Read effort value, GPA, and exam score
                x = float(row[check])
                gpa = float(row["final_gpa"])
                exam = float(row["standardized_exam_score"])
            except Exception:
                continue  # skip bad/missing rows
            # Place student into the correct bin
            for target in range(len(targets)):
                if x <= targets[target]:
                    bins[target][0] += 1            # increment student count
                    bins[target][1] += gpa          # add GPA
                    bins[target][2] += exam         # add exam score
                    break
                # Catch all last bin
                elif target == len(targets) - 1:
                    bins[target][0] += 1
                    bins[target][1] += gpa
                    bins[target][2] += exam
        # Print average GPA and exam score for each bin
        for i in range(len(targets)):
            if bins[i][0] != 0:
                print(
                    "The results for bin for target",
                    targets[i],
                    "are",
                    (bins[i][1] / bins[i][0]),       # average GPA
                    "and the exam scores are",
                    (bins[i][2] / bins[i][0]),       # average exam score
                )
            else:
                print("the target", targets[i], "has no members")

# This function compares averages across GPA or exam score groups
def mostImportant(checkList, check):

    # Define performance brackets
    if check == "final_gpa":
        targets = [4, 3.5, 3, 2.5, 2, 1, 0]
    else:
        targets = [90, 80, 70, 60, 50, 40, 30, 20, 10, 0]

    # bins: count + one slot per feature in checkList
    bins = [[0] + [0.0 for _ in range(len(checkList))] for j in range(len(targets))]

    with open("student_academic_performance_1M.csv", mode="r", newline="") as file:
        csv_reader = csv.DictReader(file)

        # Assign each student to a performance group
        for row in csv_reader:
            try:
                y = float(row[check])
            except Exception:
                continue

            # find which performance group this student belongs to
            n = len(targets) - 1
            for x in range(len(targets)):
                try:
                    if y >= targets[x]:
                        n = x
                        break
                except Exception:
                    pass

            bins[n][0] += 1       # increment group count
            # Add all academic effort variables
            for x in range(len(checkList)):
                try:
                    bins[n][x + 1] += float(row[checkList[x]])
                except Exception:
                    pass
        # Print average effort values per performance group
        for x in range(len(targets)):
            print(
                "The students with a",
                check,
                "of",
                targets[x],
                "or more and their average values are: ",
            )

            for y in range(len(checkList)):
                if bins[x][0] != 0:
                    bins[x][y + 1] = round(bins[x][y + 1] / bins[x][0], 2)
                print(checkList[y], ":", bins[x][y + 1])
        # Optional: compare best vs worst students
        intake = (
            input(
                "Would you like to compare the difference between best and worst students Y/N\n"
            )
        ).lower()

        if intake == "y":
            print("\n\nThe average best student vs worst student looks like this: \n")
            for y in range(len(checkList)):
                print(checkList[y], ":", bins[0][y + 1] - bins[len(bins) - 1][y + 1])

#Run
if __name__ == "__main__":
    main()
