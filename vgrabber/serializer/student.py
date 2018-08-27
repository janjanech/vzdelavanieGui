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

        for grade in self.__student.grades:
            finalexam_element = Element(
                'finalexam',
                id=str(grade.final_exam.id),
                grade=grade.grade.name
            )
            student_element.append(finalexam_element)

        return student_element
