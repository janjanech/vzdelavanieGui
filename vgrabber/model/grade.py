import os.path
from enum import Enum, auto

from .files import FileList


class Grade(Enum):
    A = auto()
    B = auto()
    C = auto()
    D = auto()
    E = auto()
    FX = auto()


class StudentGrade:
    def __init__(self, final_exam, grade):
        self.final_exam = final_exam
        self.grade = grade
        self.points = None
        self.files = FileList()

    def __str__(self):
        return "<Grade {0} for final exam at {1}>".format(self.grade.name, self.final_exam.date_time.isoformat())

    def save(self, directory):
        self.files.save(
            os.path.join(
                directory,
                'finalexams',
                '{0}_{1}'.format(self.final_exam.id, self.final_exam.date_time.isoformat())
            )
        )
