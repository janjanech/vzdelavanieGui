class Group:
    number: str
    moodle_id: int
    moodle_name: str

    def __init__(self, number, moodle_id, moodle_name):
        self.number = number
        self.moodle_id = moodle_id
        self.moodle_name = moodle_name
