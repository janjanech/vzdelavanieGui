from typing import List


class HomeWork:
    category: "HomeWorkCategory"
    
    def __init__(self, subject, id, name, moodle_id):
        self.__subject = subject
        self.id = id
        self.name = name
        self.moodle_id = moodle_id
        self.category = None

    def get_submissions(self):
        for student in self.__subject.students:
            for home_work_points in student.home_work_points:
                if home_work_points.home_work is self:
                    yield home_work_points


class HomeWorkCategory:
    name: str
    home_works: List[HomeWork]

    def __init__(self, subject, name):
        self.__subject = subject
        self.name = name
        self.home_works = []

    def clear_home_works(self):
        self.home_works.clear()

    def add_home_work(self, home_work):
        self.home_works.append(home_work)
        home_work.category = self
