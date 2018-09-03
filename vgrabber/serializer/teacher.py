from lxml.etree import Element

from vgrabber.model import Teacher


class TeacherSerializer:
    __teacher: Teacher

    def __init__(self, teacher):
        self.__teacher = teacher

    def serialize(self):
        if self.__teacher.surname is not None:
            teacher_element = Element(
                'teacher',
                name=self.__teacher.name,
                surname=self.__teacher.surname,
                moodleid=str(self.__teacher.moodle_id),
                moodleemail=self.__teacher.moodle_email
            )
        else:
            teacher_element = Element(
                'teacher'
            )

        for group in self.__teacher.taught_groups:
            optional_info = {}

            if group.number is not None:
                optional_info['number'] = group.number

            group_element = Element(
                'group',
                moodlename = group.moodle_name,
                moodleid = str(group.moodle_id),
                **optional_info
            )

            teacher_element.append(group_element)

        return teacher_element
