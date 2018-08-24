class Subject:
    def __init__(self, number, name, year):
        self.number = number
        self.name = name
        self.year = year
        self.__progress = set()
        self.start_date = None
        self.students = []
        self.teachers = []
        self.homeworks = []
        self.tests = []
        self.final_exams = []

    def __str__(self):
        return "<Subject {0} {1} in year {2}>".format(self.number, self.name, self.year)
