class Test:
    id: int
    name: str
    moodle_id: int

    def __init__(self, subject, id, name, moodle_id):
        self.__subject = subject
        self.id = id
        self.name = name
        self.moodle_id = moodle_id

    def get_submissions(self):
        for student in self.__subject.students:
            for test_points in student.test_points:
                if test_points.test is self:
                    yield test_points
