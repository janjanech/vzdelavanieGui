from .homeworkcategory import HomeWorkCategoryDeserializer
from .test import TestDeserializer
from .teacher import TeacherDeserializer
from .progresschecker import ProgressChecker
from .student import StudentDeserializer
from .finalexam import FinalExamDeserializer
from vgrabber.model import Subject


class SubjectDeserializer:
    def __init__(self, subject_element, path):
        self.__subject_element = subject_element
        self.__path = path

    def deserialize(self):
        subject = Subject(
            self.__subject_element.attrib['number'],
            self.__subject_element.attrib['name'],
            self.__subject_element.attrib['year']
        )

        for action in ProgressChecker(self.__subject_element).find_out_progress():
            subject.finish_action(action)

        for finalexam_element in self.__subject_element.xpath('//finalexams/finalexam'):
            final_exam = FinalExamDeserializer(subject, finalexam_element).deserialize()
            subject.add_final_exam(final_exam)

        for test_element in self.__subject_element.xpath('//tests/test'):
            test = TestDeserializer(subject, test_element).deserialize()
            subject.add_test(test)

        for category_element in self.__subject_element.xpath('//homeworks/category'):
            home_work_category = HomeWorkCategoryDeserializer(subject, category_element).deserialize()
            subject.add_home_work_category(home_work_category)

        for student_element in self.__subject_element.xpath('//students/student'):
            home_works = [
                home_work
                    for home_work_category in subject.home_work_categories
                        for home_work in home_work_category.home_works
            ]
            student = StudentDeserializer(
                subject,
                subject.tests,
                home_works,
                subject.final_exams,
                student_element,
                self.__path
            ).deserialize()
            subject.add_student(student)

        for teacher_element in self.__subject_element.xpath('//teachers/teacher'):
            teacher = TeacherDeserializer(subject, teacher_element).deserialize()
            subject.add_teacher(teacher)

        return subject
