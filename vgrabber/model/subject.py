from typing import Set, List

from vgrabber.base.importaction import ImportAction
from vgrabber.utilities.accents import strip_accents
from .student import Student
from .teacher import Teacher
from .homework import HomeWorkCategory
from .test import Test
from .finalexam import FinalExam


class Subject:
    number: str
    name: str
    year: str
    progress: Set[ImportAction]
    students: List[Student]
    teachers: List[Teacher]
    home_work_categories: List[HomeWorkCategory]
    tests: List[Test]
    final_exams: List[FinalExam]

    def __init__(self, number, name, year):
        self.number = number
        self.name = name
        self.year = year
        self.progress = set()
        self.start_date = None
        self.students = []
        self.teachers = []
        self.home_work_categories = []
        self.tests = []
        self.final_exams = []

    def __str__(self):
        return "<Subject {0} {1} in year {2}>".format(self.number, self.name, self.year)

    def finish_action(self, action):
        self.progress.add(action)

    def add_final_exam(self, final_exam):
        self.final_exams.append(final_exam)

    def add_student(self, student):
        self.students.append(student)

    def add_teacher(self, teacher):
        self.teachers.append(teacher)

    def add_test(self, test):
        self.tests.append(test)

    def add_home_work_category(self, home_work_category):
        self.home_work_categories.append(home_work_category)

    def add_home_work_to_category(self, home_work, category='unknown'):
        for found_category in self.home_work_categories:
            if found_category.name == category:
                break
        else:
            found_category = HomeWorkCategory(category)
            self.home_work_categories.append(found_category)

        found_category.add_home_work(home_work)

    def clear_final_exams(self):
        self.final_exams = []

    def clear_students(self):
        self.students.clear()

    def clear_teachers(self):
        self.teachers.clear()

    def clear_tests(self):
        self.tests.clear()

    def clear_teacher_groups(self):
        for teacher in self.teachers:
            teacher.clear_groups()

    def clear_home_works(self):
        for category in self.home_work_categories:
            category.clear_home_works()

    def clear_final_exam_points(self):
        for student in self.students:
            student.clear_final_exam_points()

    def clear_home_work_points(self):
        for student in self.students:
            student.clear_home_work_points()

    def clear_test_points(self):
        for student in self.students:
            student.clear_test_points()

    def clear_final_exam_files(self):
        for student in self.students:
            student.clear_final_exam_files()

    def clear_home_work_files(self):
        for student in self.students:
            student.clear_home_work_files()

    def clear_test_files(self):
        for student in self.students:
            student.clear_test_files()

    def get_final_exam_by_date_time(self, date_time):
        for final_exam in self.final_exams:
            if final_exam.date_time == date_time:
                return final_exam

    def get_test_by_id(self, item_id):
        for test in self.tests:
            if test.id == item_id:
                return test

    def get_home_work_by_id(self, item_id):
        for home_work_category in self.home_work_categories:
            for home_work in home_work_category.home_works:
                if home_work.id == item_id:
                    return home_work

    def get_student_by_email(self, moodle_email):
        for student in self.students:
            if student.moodle_email == moodle_email:
                return student

    def get_student_by_moodle_id(self, moodle_id):
        for student in self.students:
            if student.moodle_id == moodle_id:
                return student

    def get_teacher_by_surname(self, teacher_surname):
        teacher_surname = strip_accents(teacher_surname)

        for teacher in self.teachers:
            if teacher.surname and strip_accents(teacher.surname) == teacher_surname:
                return teacher
        else:
            return self.get_unknown_teacher()

    def get_unknown_teacher(self):
        for teacher in self.teachers:
            if teacher.surname is None:
                return teacher
        else:
            teacher = Teacher(None, None, None, None)
            self.teachers.append(teacher)
            return teacher

    def save(self, directory):
        for student in self.students:
            student.save(directory)

    def get_group_by_moodle_id(self, moodle_group_id):
        for teacher in self.teachers:
            for group in teacher.taught_groups:
                if group.moodle_id == moodle_group_id:
                    return group
