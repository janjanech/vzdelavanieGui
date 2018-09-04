class Test:
    id: int
    name: str
    moodle_id: int

    def __init__(self, subject, id, name, moodle_id):
        self.__subject = subject
        self.id = id
        self.name = name
        self.moodle_id = moodle_id
