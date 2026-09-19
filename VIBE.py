"""Student Grade Calculator.

Data structure choice: Option B, a Student class.
"""

FILE_NAME = "student_grades.txt"


class Student:
	"""Store one student's information and calculated grade."""

	def __init__(self, name, student_id, test1, test2, test3):
		self.name = name
		self.student_id = student_id
		self.test1 = test1
		self.test2 = test2
		self.test3 = test3
		self.average = (test1 + test2 + test3) / 3
		self.grade = calculate_grade(self.average)

	def to_file_line(self):
		"""Return the student in the required pipe-delimited format."""
		return (
			f"{self.name}|{self.student_id}|{self.test1:.2f}|"
			f"{self.test2:.2f}|{self.test3:.2f}|{self.average:.2f}|{self.grade}"
		)


def calculate_grade(average):
	"""Return a letter grade for an average score."""
	if average >= 90:
		return "A"
	if average >= 80:
		return "B"
	if average >= 70:
		return "C"
	if average >= 60:
		return "D"
	return "F"


def read_text(prompt):
	"""Read text input and allow ESC or the word ESC to exit."""
	try:
		value = input(prompt).strip()
	except (EOFError, KeyboardInterrupt):
		print("\nExiting Student Grade Calculator.")
		raise SystemExit

	if value == "\x1b" or value.upper() == "ESC":
		print("Exiting Student Grade Calculator.")
		raise SystemExit
	return value


def read_score(prompt):
	"""Read and validate a test score from 0 through 100."""
	while True:
		value = read_text(prompt)
		try:
			score = float(value)
			if 0 <= score <= 100:
				return score
			print("Please enter a score from 0 to 100.")
		except ValueError:
			print("Please enter a valid number.")


def load_students():
	"""Load student records, skipping malformed records with a message."""
	students = []
	try:
		with open(FILE_NAME, "r", encoding="utf-8") as file:
			for line_number, line in enumerate(file, start=1):
				fields = line.rstrip("\n").split("|")
				if len(fields) != 7:
					print(f"Skipped invalid record on line {line_number}.")
					continue
				try:
					student = Student(
						fields[0],
						fields[1],
						float(fields[2]),
						float(fields[3]),
						float(fields[4]),
					)
					students.append(student)
				except ValueError:
					print(f"Skipped invalid scores on line {line_number}.")
	except FileNotFoundError:
		print("No saved student file found. Starting with an empty class.")
	except OSError as error:
		print(f"Could not load student records: {error}")
	return students


def save_students(students):
	"""Save all student records to the required file."""
	try:
		with open(FILE_NAME, "w", encoding="utf-8") as file:
			for student in students:
				file.write(student.to_file_line() + "\n")
		return True
	except OSError as error:
		print(f"Could not save student records: {error}")
		return False


def add_student(students):
	"""Prompt for and add one student."""
	print("\nAdd Student (enter ESC at any prompt to exit)")
	name = read_text("Student name: ")
	while not name:
		print("Name cannot be blank.")
		name = read_text("Student name: ")
	student_id = read_text("Student ID: ")
	while not student_id:
		print("Student ID cannot be blank.")
		student_id = read_text("Student ID: ")
	test1 = read_score("Test 1 score: ")
	test2 = read_score("Test 2 score: ")
	test3 = read_score("Test 3 score: ")

	student = Student(name, student_id, test1, test2, test3)
	students.append(student)
	save_students(students)
	print(f"Added {student.name}: average {student.average:.2f}, grade {student.grade}.")


def display_students(students):
	"""Display all students in a formatted table."""
	if not students:
		print("\nNo student records to display.")
		return

	print("\nStudent Records")
	print("-" * 87)
	print(
		f"{'Name':<20} {'ID':<14} {'Test 1':>8} {'Test 2':>8} "
		f"{'Test 3':>8} {'Average':>9} {'Grade':>6}"
	)
	print("-" * 87)
	for student in students:
		print(
			f"{student.name:<20.20} {student.student_id:<14.14} "
			f"{student.test1:>8.2f} {student.test2:>8.2f} "
			f"{student.test3:>8.2f} {student.average:>9.2f} "
			f"{student.grade:>6}"
		)
	print("-" * 87)


def display_statistics(students):
	"""Display highest, lowest, and class average scores."""
	if not students:
		print("\nNo student records available for statistics.")
		return

	averages = [student.average for student in students]
	print("\nClass Statistics")
	print(f"Highest average: {max(averages):.2f}")
	print(f"Lowest average:  {min(averages):.2f}")
	print(f"Class average:   {sum(averages) / len(averages):.2f}")


def search_students(students):
	"""Find and display students whose names match the search text."""
	search_term = read_text("\nEnter a student name to search: ").lower()
	matches = [student for student in students if search_term in student.name.lower()]
	if not matches:
		print("No matching students found.")
		return
	display_students(matches)


def display_menu():
	"""Display the main menu."""
	print("\nStudent Grade Calculator")
	print("1. Add a student")
	print("2. Display all students")
	print("3. Display class statistics")
	print("4. Search by student name")
	print("5. Save records")
	print("ESC. Exit")


def main():
	"""Run the Student Grade Calculator menu."""
	students = load_students()
	print(f"Loaded {len(students)} student record(s).")

	while True:
		display_menu()
		choice = read_text("Choose an option: ")
		if choice == "1":
			add_student(students)
		elif choice == "2":
			display_students(students)
		elif choice == "3":
			display_statistics(students)
		elif choice == "4":
			search_students(students)
		elif choice == "5":
			if save_students(students):
				print("Student records saved.")
		else:
			print("Please choose 1, 2, 3, 4, 5, or ESC.")


if __name__ == "__main__":
	main()