import os.path

from vgrabber.model import Student, StudentGrade, Grade
from vgrabber.model.files import StoredFile


class StudentDeserializer:
    def __init__(self, subject, tests, home_works, final_exams, student_element, path):
        self.__subject = subject
        self.__tests = {test.id: test for test in tests}
        self.__home_works = {home_work.id: home_work for home_work in home_works}
        self.__final_exams = {final_exam.id: final_exam for final_exam in final_exams}
        self.__student_element = student_element
        self.__path = path

    def deserialize(self):
        student = Student(
            self.__subject,
            self.__student_element.attrib.get('number'),
            self.__student_element.attrib['name'],
            self.__student_element.attrib['surname'],
            self.__student_element.attrib.get('group'),
        )

        if 'moodleid' in self.__student_element.attrib:
            student.moodle_id = int(self.__student_element.attrib['moodleid'])
        if 'moodlegroup' in self.__student_element.attrib:
            student.moodle_group = int(self.__student_element.attrib['moodlegroup'])
        if 'moodleemail' in self.__student_element.attrib:
            student.moodle_email = self.__student_element.attrib['moodleemail']

        for test_element in self.__student_element.xpath('.//test'):
            test = self.__tests[int(test_element.attrib['id'])]

            if 'points' in test_element.attrib:
                student.add_test_points(test, float(test_element.attrib['points']))

            for file in self.__deserialize_files(test_element):
                student.add_test_file(test, file)

        for homework_element in self.__student_element.xpath('.//homework'):
            home_work = self.__home_works[int(homework_element.attrib['id'])]

            if 'points' in homework_element.attrib:
                student.add_home_work_points(home_work, float(homework_element.attrib['points']))

            for file in self.__deserialize_files(homework_element):
                student.add_home_work_file(home_work, file)

        for finalexam_element in self.__student_element.xpath('.//finalexam'):
            grade_mark = None
            if 'grade' in finalexam_element.attrib:
                grade_mark = Grade[finalexam_element.attrib['grade']]

            grade = StudentGrade(
                self.__subject,
                self.__final_exams[int(finalexam_element.attrib['id'])],
                grade_mark
            )

            if 'points' in finalexam_element.attrib:
                grade.points = float(finalexam_element.attrib['points'])

            for file in self.__deserialize_files(finalexam_element):
                grade.files.add_file(file)

            student.add_grade(grade)

        return student

    def __deserialize_files(self, parent_element):
        for file_element in parent_element.xpath('./file'):
            yield StoredFile(
                file_element.attrib['filename'],
                os.path.join(self.__path, file_element.attrib['path'])
            )
