import datetime

from vgrabber.model import FinalExam


class FinalExamDeserializer:
    def __init__(self, subject, finalexam_element):
        self.__subject = subject
        self.__finalexam_element = finalexam_element

    def deserialize(self):
        date_time = datetime.datetime.strptime('{0}T{1}'.format(
            self.__finalexam_element.attrib['date'],
            self.__finalexam_element.attrib['time'],
        ), '%Y-%m-%dT%H:%M:%S')

        id = int(self.__finalexam_element.attrib['id'])

        room = self.__finalexam_element.attrib['room']

        final_exam = FinalExam(self.__subject, date_time, room, id)

        if 'moodleid' in self.__finalexam_element.attrib:
            final_exam.moodle_id = self.__finalexam_element.attrib['moodleid']

        return final_exam
