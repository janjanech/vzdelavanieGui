from lxml.etree import Element

from vgrabber.model import FinalExam


class FinalExamSerializer:
    __final_exam: FinalExam
    def __init__(self, final_exam):
        self.__final_exam = final_exam

    def serialize(self):
        optional_info = {}
        if self.__final_exam.moodle_id is not None:
            optional_info['moodleid'] = str(self.__final_exam.moodle_id)

        finalexam_element = Element(
            'finalexam',
            id=str(self.__final_exam.id),
            date=self.__final_exam.date_time.date().isoformat(),
            time=self.__final_exam.date_time.time().isoformat(),
            room=self.__final_exam.room,
            **optional_info
        )

        return finalexam_element
