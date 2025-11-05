#gradebook.py
# Author: jain akshat naveenkumar
# Date: 2025-11-05
# Title: Gradebook Analyzer Project

import csv

print("🎓 Welcome to the Gradebook Analyzer 🎓")
print("--------------------------------------")
print("Choose your data input method:")
print("1. Manual Entry")
print("2. Import from CSV File\n")

# 🧩 Task 2: Data Entry or CSV Import
def get_data():
    choice = input("Enter 1 for manual entry or 2 for CSV import: ")
    marks = {}

    if choice == "1":
        n = int(input("How many students? "))
        for i in range(n):
            name = input("Enter student name: ")
            score = int(input("Enter marks: "))
            marks[name] = score
    elif choice == "2":
        filename = input("Enter CSV file name (with .csv): ")
        try:
            with open(filename, newline='') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if len(row) == 2:
                        name, score = row
                        marks[name] = int(score)
        except FileNotFoundError:
            print("⚠ File not found. Please check the file name.")
    else:
        print("Invalid choice.")
    return marks

# 🧩 Task 3: Statistical Analysis
def calculate_average(marks_dict):
    return sum(marks_dict.values()) / len(marks_dict) if marks_dict else 0

def calculate_median(marks_dict):
    if not marks_dict:
        return 0
    scores = sorted(marks_dict.values())
    n = len(scores)
    if n % 2 == 1:
        return scores[n // 2]
    else:
        return (scores[n//2 - 1] + scores[n//2]) / 2

def find_max_score(marks_dict):
    return max(marks_dict.values()) if marks_dict else 0

def find_min_score(marks_dict):
    return min(marks_dict.values()) if marks_dict else 0

# 🧩 Task 4: Grade Assignment and Distribution
def assign_grades(marks_dict):
    grades = {}
    for name, score in marks_dict.items():
        if score >= 90:
            grade = "A"
        elif score >= 80:
            grade = "B"
        elif score >= 70:
            grade = "C"
        elif score >= 60:
            grade = "D"
        else:
            grade = "F"
        grades[name] = grade
    return grades

def count_grades(grades):
    grade_count = {}
    for g in grades.values():
        grade_count[g] = grade_count.get(g, 0) + 1
    return grade_count

# 🧩 NEW: Save Results to CSV
def save_results_to_csv(marks, grades, filename="gradebook_results.csv"):
    with open(filename, mode="w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Marks", "Grade", "Status"])
        for name in marks:
            status = "Pass" if marks[name] >= 40 else "Fail"
            writer.writerow([name, marks[name], grades[name], status])
    print(f"\n💾 Results saved successfully to '{filename}'")

# 🧩 Task 5 + 6: Results Table, Pass/Fail, Loop
while True:
    marks = get_data()
    if not marks:
        print("⚠ No data entered. Try again.\n")
        continue

    grades = assign_grades(marks)

    print("\n📊 Student Results:")
    print("----------------------------")
    print("Name\tMarks\tGrade")
    print("----------------------------")
    for name in marks:
        print(f"{name}\t{marks[name]}\t{grades[name]}")

    print("\n📈 Statistics:")
    print(f"Average: {calculate_average(marks):.2f}")
    print(f"Median: {calculate_median(marks)}")
    print(f"Highest: {find_max_score(marks)}")
    print(f"Lowest: {find_min_score(marks)}")

    print("\nGrade Distribution:", count_grades(grades))

    passed_students = [name for name, score in marks.items() if score >= 40]
    failed_students = [name for name, score in marks.items() if score < 40]

    print(f"\n✅ Passed Students ({len(passed_students)}): {passed_students}")
    print(f"❌ Failed Students ({len(failed_students)}): {failed_students}")

    # 🔹 Save the output to CSV
    save_results_to_csv(marks, grades)

    again = input("\nDo you want to run again? (y/n): ").lower()
    if again != "y":
        print("👋 Goodbye! Thanks for using Gradebook Analyzer.")
        break

