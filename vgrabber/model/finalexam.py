class FinalExam:
    def __init__(self, date_time, room, id):
        self.date_time = date_time
        self.room = room
        self.id = id

    def __str__(self):
        return "<FinalExam {0} at {1} in room {2}>".format(self.id, self.date_time.isoformat(), self.room)
