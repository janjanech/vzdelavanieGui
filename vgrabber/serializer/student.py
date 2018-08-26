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

        for grade in self.__student.grades:
            finalexam_element = Element(
                'finalexam',
                id=str(grade.final_exam.id),
                grade=grade.grade.name
            )
            student_element.append(finalexam_element)

        return student_element
