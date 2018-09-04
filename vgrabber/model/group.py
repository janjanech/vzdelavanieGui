class Group:
    number: str
    moodle_id: int
    moodle_name: str

    def __init__(self, subject, number, moodle_id, moodle_name):
        self.__subject = subject
        self.number = number
        self.moodle_id = moodle_id
        self.moodle_name = moodle_name

    def get_students(self):
        if self.moodle_id is None:
            return

        for student in self.__subject.students:
            if student.moodle_group_id == self.moodle_id:
                yield student
