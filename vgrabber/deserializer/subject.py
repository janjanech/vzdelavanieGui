from .finalexam import FinalExamDeserializer
from vgrabber.importer import ImportAction
from vgrabber.model import Subject


class SubjectDeserializer:
    def __init__(self, subject_element):
        self.__subject_element = subject_element

    def deserialize(self):
        subject = Subject(
            self.__subject_element.attrib['number'],
            self.__subject_element.attrib['name'],
            self.__subject_element.attrib['year']
        )

        for action_element in self.__subject_element.xpath('//progress/finished'):
            subject.finish_action(ImportAction[action_element.attrib['action']])

        for finalexam_element in self.__subject_element.xpath('//finalexams/finalexam'):
            final_exam = FinalExamDeserializer(finalexam_element).deserialize()
            subject.add_final_exam(final_exam)

        return subject
