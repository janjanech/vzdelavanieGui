class Subject:
    def __init__(self, number, name, year):
        self.number = number
        self.name = name
        self.year = year
        self.progress = set()
        self.start_date = None
        self.students = []
        self.teachers = []
        self.homeworks = []
        self.tests = []
        self.final_exams = []

    def __str__(self):
        return "<Subject {0} {1} in year {2}>".format(self.number, self.name, self.year)

    def finish_action(self, action):
        self.progress.add(action)

    def add_final_exam(self, final_exam):
        self.final_exams.append(final_exam)

    def clear_final_exams(self):
        self.final_exams = []
