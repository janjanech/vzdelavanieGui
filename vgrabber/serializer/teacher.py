from lxml.etree import Element

from vgrabber.model import Teacher


class TeacherSerializer:
    __teacher: Teacher

    def __init__(self, teacher):
        self.__teacher = teacher

    def serialize(self):
        teacher_element = Element(
            'teacher',
            name=self.__teacher.name,
            surname=self.__teacher.surname,
            moodleid=str(self.__teacher.moodle_id),
            moodleemail=self.__teacher.moodle_email
        )

        return teacher_element
