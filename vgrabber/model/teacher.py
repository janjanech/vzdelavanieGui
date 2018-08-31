class Teacher:
    name: str
    surname: str
    moodle_id: int
    moodle_email: str

    def __init__(self, name, surname, moodle_id, moodle_email):
        self.name = name
        self.surname = surname
        self.moodle_id = moodle_id
        self.moodle_email = moodle_email
