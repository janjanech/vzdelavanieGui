from lxml.etree import Element

from vgrabber.model import Student


class StudentSerializer:
    __student: Student

    def __init__(self, student):
        self.__student = student

    def serialize(self):
        student_element = Element(
            'student',
            number=self.__student.number,
            name=self.__student.name,
            surname=self.__student.surname,
            group=self.__student.group,
        )

        return student_element
