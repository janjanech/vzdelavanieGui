import datetime

from vgrabber.model import FinalExam


class FinalExamDeserializer:
    def __init__(self, finalexam_element):
        self.__finalexam_element = finalexam_element

    def deserialize(self):
        date_time = datetime.datetime.strptime('{0}T{1}'.format(
            self.__finalexam_element.attrib['date'],
            self.__finalexam_element.attrib['time'],
        ), '%Y-%m-%dT%H:%M:%S')

        id = int(self.__finalexam_element.attrib['id'])

        room = self.__finalexam_element.attrib['room']

        return FinalExam(date_time, room, id)
