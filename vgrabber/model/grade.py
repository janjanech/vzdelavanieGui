from enum import Enum, auto


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

    def __str__(self):
        return "<Grade {0} for final exam at {1}>".format(self.grade.name, self.final_exam.date_time.isoformat())
