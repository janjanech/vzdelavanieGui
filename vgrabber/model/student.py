import os.path

from vgrabber.utilities.accents import strip_accents
from .grade import StudentGrade
from .homeworkpoints import HomeWorkPoints
from .testpoints import TestPoints


class Student:
    def __init__(self, number, name, surname, group):
        self.number = number
        self.name = name
        self.surname = surname
        self.group = group
        self.grades = []
        self.moodle_id = None
        self.moodle_group = None
        self.moodle_email = None
        self.home_work_points = []
        self.test_points = []

    def __str__(self):
        graded = ""
        if self.grades:
            graded = ", graded {0}".format(self.grades[-1])
        return "<Student {0} {1} in group {2}, number {3}{4}>".format(
            self.name,
            self.surname,
            self.group,
            self.number,
            graded
        )

    def add_grade(self, grade):
        self.grades.append(grade)

    def add_test_points(self, test, points):
        self.test_points.append(TestPoints(test, points))

    def add_home_work_points(self, home_work, points):
        self.home_work_points.append(HomeWorkPoints(home_work, points))

    def add_final_exam_points(self, final_exam, points):
        for grade in self.grades:
            if grade.final_exam == final_exam:
                grade.points = points
                break
        else:
            grade = StudentGrade(final_exam, None)
            grade.points = points
            self.grades.append(grade)

    def add_final_exam_file(self, final_exam, file):
        for grade in self.grades:
            if grade.final_exam == final_exam:
                grade.files.add_file(file)
                break
        else:
            grade = StudentGrade(final_exam, None)
            grade.files.add_file(file)
            self.grades.append(grade)

    def clear_grades(self):
        self.grades.clear()

    def clear_final_exam_points(self):
        for grade in self.grades:
            grade.points = None

    def clear_final_exam_files(self):
        for grade in self.grades:
            grade.files.clear()

    def clear_home_work_points(self):
        self.home_work_points.clear()

    def clear_test_points(self):
        self.test_points.clear()

    def save(self, directory):
        for grade in self.grades:
            grade.save(
                os.path.join(
                    directory,
                    '{0}_{1}{2}'.format(self.number, strip_accents(self.surname), strip_accents(self.name))
                )
            )
