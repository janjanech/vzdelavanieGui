import datetime


class FinalExam:
    date_time: datetime.datetime
    room: str
    id: int
    moodle_id: int

    def __init__(self, subject, date_time, room, id):
        self.__subject = subject
        self.date_time = date_time
        self.room = room
        self.id = id
        self.moodle_id = None

    def __str__(self):
        return "<FinalExam {0} at {1} in room {2}>".format(self.id, self.date_time.isoformat(), self.room)

    def get_submissions(self):
        for student in self.__subject.students:
            for grade in student.grades:
                if grade.final_exam is self:
                    yield grade
