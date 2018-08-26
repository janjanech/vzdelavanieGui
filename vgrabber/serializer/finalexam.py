from lxml.etree import Element

from vgrabber.model import FinalExam


class FinalExamSerializer:
    __final_exam: FinalExam
    def __init__(self, final_exam):
        self.__final_exam = final_exam

    def serialize(self):
        finalexam_element = Element(
            'finalexam',
            id=str(self.__final_exam.id),
            date=self.__final_exam.date_time.date().isoformat(),
            time=self.__final_exam.date_time.time().isoformat(),
            room=self.__final_exam.room
        )

        return finalexam_element
