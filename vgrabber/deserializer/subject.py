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

        return subject
