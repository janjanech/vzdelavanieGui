from vgrabber.model import Student, StudentGrade, Grade


class StudentDeserializer:
    def __init__(self, final_exams, student_element):
        self.__final_exams = {final_exam.id: final_exam for final_exam in final_exams}
        self.__student_element = student_element

    def deserialize(self):
        student = Student(
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

        for finalexam_element in self.__student_element.xpath('.//finalexam'):
            grade = StudentGrade(
                self.__final_exams[int(finalexam_element.attrib["id"])],
                Grade[finalexam_element.attrib["grade"]]
            )

            student.add_grade(grade)

        return student
