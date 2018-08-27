from vgrabber.model import Teacher


class TeacherDeserializer:
    def __init__(self, teacher_element):
        self.__teacher_element = teacher_element

    def deserialize(self):
        teacher = Teacher(
            self.__teacher_element.attrib['name'],
            self.__teacher_element.attrib['surname'],
            int(self.__teacher_element.attrib['moodleid']),
            self.__teacher_element.attrib['moodleemail']
        )

        return teacher
