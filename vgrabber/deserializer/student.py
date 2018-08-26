from vgrabber.model import Student


class StudentDeserializer:
    def __init__(self, student_element):
        self.__student_element = student_element

    def deserialize(self):
        student = Student(
            self.__student_element.attrib["number"],
            self.__student_element.attrib["name"],
            self.__student_element.attrib["surname"],
            self.__student_element.attrib["group"],
        )

        return student
