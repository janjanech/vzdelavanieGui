from lxml.etree import Element

from vgrabber.model import Student


class StudentSerializer:
    __student: Student

    def __init__(self, student):
        self.__student = student

    def serialize(self):
        optional_info = {}
        if self.__student.moodle_id is not None:
            optional_info['moodleid'] = str(self.__student.moodle_id)
        if self.__student.moodle_group is not None:
            optional_info['moodlegroup'] = str(self.__student.moodle_group)
        if self.__student.moodle_email is not None:
            optional_info['moodleemail'] = self.__student.moodle_email
        if self.__student.group is not None:
            optional_info['group'] = self.__student.group
        if self.__student.number is not None:
            optional_info['number'] = self.__student.number

        student_element = Element(
            'student',
            name=self.__student.name,
            surname=self.__student.surname,
            **optional_info
        )

        for home_work_point in self.__student.home_work_points:
            homework_element = Element(
                'homework',
                id=str(home_work_point.home_work.id),
                points=str(home_work_point.points)
            )
            student_element.append(homework_element)

        for test_point in self.__student.test_points:
            test_element = Element(
                'test',
                id=str(test_point.test.id),
                points=str(test_point.points)
            )
            student_element.append(test_element)

        for grade in self.__student.grades:
            optional_info = {}

            if grade.grade is not None:
                optional_info['grade'] = grade.grade.name
            if grade.points is not None:
                optional_info['points'] = str(grade.points)

            finalexam_element = Element(
                'finalexam',
                id=str(grade.final_exam.id),
                **optional_info
            )
            student_element.append(finalexam_element)

        return student_element
