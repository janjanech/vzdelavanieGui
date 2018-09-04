from typing import List

from .group import Group


class Teacher:
    name: str
    surname: str
    moodle_id: int
    moodle_email: str
    taught_groups: List[Group]

    def __init__(self, subject, name, surname, moodle_id, moodle_email):
        self.__subject = subject
        self.name = name
        self.surname = surname
        self.moodle_id = moodle_id
        self.moodle_email = moodle_email
        self.taught_groups = []

    def add_taught_group(self, group):
        self.taught_groups.append(group)

    def clear_groups(self):
        self.taught_groups.clear()
