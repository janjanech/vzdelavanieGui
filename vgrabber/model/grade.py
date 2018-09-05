from enum import Enum, auto

from .files import FileList
from .finalexam import FinalExam


class Grade(Enum):
    A = auto()
    B = auto()
    C = auto()
    D = auto()
    E = auto()
    FX = auto()


class StudentGrade:
    final_exam: FinalExam
    grade: Grade
    points: float
    files: FileList

    def __init__(self, subject, student, final_exam, grade):
        self.__subject = subject
        self.final_exam = final_exam
        self.grade = grade
        self.points = None
        self.files = FileList()

        self.student = student

    def __str__(self):
        return "<Grade {0} for final exam at {1}>".format(self.grade.name, self.final_exam.date_time.isoformat())

    def clear_files(self):
        self.files.clear()
