from typing import List


class HomeWork:
    def __init__(self, id, name, moodle_id):
        self.id = id
        self.name = name
        self.moodle_id = moodle_id


class HomeWorkCategory:
    name: str
    home_works: List[HomeWork]

    def __init__(self, name):
        self.name = name
        self.home_works = []

    def clear_home_works(self):
        self.home_works.clear()

    def add_home_work(self, home_work):
        self.home_works.append(home_work)
