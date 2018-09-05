from lxml.etree import Element

from vgrabber.model import Subject
from .homeworkcategory import HomeWorkCategorySerializer
from .test import TestSerializer
from .teacher import TeacherSerializer
from .student import StudentSerializer
from .finalexam import FinalExamSerializer


class SubjectSerializer:
    __subject: Subject

    def __init__(self, subject):
        self.__subject = subject

    def serialize(self):
        subject_element = Element(
            'subject',
            number=self.__subject.number,
            name=self.__subject.name,
            year=self.__subject.year
        )

        students_element = Element('students')

        for student in self.__subject.students:
            student_element = StudentSerializer(student).serialize()
            students_element.append(student_element)

        subject_element.append(students_element)

        teachers_element = Element('teachers')

        for teacher in self.__subject.teachers:
            teacher_element = TeacherSerializer(teacher).serialize()
            teachers_element.append(teacher_element)

        subject_element.append(teachers_element)

        homeworks_element = Element('homeworks')

        for home_work_category in self.__subject.home_work_categories:
            category_element = HomeWorkCategorySerializer(home_work_category).serialize()
            homeworks_element.append(category_element)

        subject_element.append(homeworks_element)

        tests_element = Element('tests')

        for test in self.__subject.tests:
            test_element = TestSerializer(test).serialize()
            tests_element.append(test_element)

        subject_element.append(tests_element)

        finalexams_element = Element('finalexams')

        for final_exam in self.__subject.final_exams:
            finalexam_element = FinalExamSerializer(final_exam).serialize()
            finalexams_element.append(finalexam_element)

        subject_element.append(finalexams_element)

        return subject_element
