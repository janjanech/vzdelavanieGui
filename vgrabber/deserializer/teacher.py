from vgrabber.model import Teacher, Group


class TeacherDeserializer:
    def __init__(self, teacher_element):
        self.__teacher_element = teacher_element

    def deserialize(self):
        if 'name' in self.__teacher_element.attrib:
            teacher = Teacher(
                self.__teacher_element.attrib['name'],
                self.__teacher_element.attrib['surname'],
                int(self.__teacher_element.attrib['moodleid']),
                self.__teacher_element.attrib['moodleemail']
            )
        else:
            teacher = Teacher(None, None, None, None)

        for group_element in self.__teacher_element.xpath('./group'):
            moodleid = None
            if 'moodleid' in group_element.attrib:
                moodleid = int(group_element.attrib['moodleid'])

            group = Group(
                group_element.attrib.get('number'),
                moodleid,
                group_element.attrib.get('moodlename')
            )
            teacher.add_taught_group(group)

        return teacher
