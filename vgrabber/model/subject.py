from .homework import HomeWorkCategory


class Subject:
    def __init__(self, number, name, year):
        self.number = number
        self.name = name
        self.year = year
        self.progress = set()
        self.start_date = None
        self.students = []
        self.teachers = []
        self.home_work_categories = []
        self.tests = []
        self.final_exams = []

    def __str__(self):
        return "<Subject {0} {1} in year {2}>".format(self.number, self.name, self.year)

    def finish_action(self, action):
        self.progress.add(action)

    def add_final_exam(self, final_exam):
        self.final_exams.append(final_exam)

    def add_student(self, student):
        self.students.append(student)

    def add_teacher(self, teacher):
        self.teachers.append(teacher)

    def add_test(self, test):
        self.tests.append(test)

    def add_home_work_to_category(self, home_work, category='unknown'):
        for found_category in self.home_work_categories:
            if found_category.name == category:
                break
        else:
            found_category = HomeWorkCategory(category)
            self.home_work_categories.append(found_category)

        found_category.add_home_work(home_work)

    def clear_final_exams(self):
        self.final_exams = []

    def clear_students(self):
        self.students.clear()

    def clear_teachers(self):
        self.teachers.clear()

    def clear_tests(self):
        self.tests.clear()

    def clear_home_works(self):
        for category in self.home_work_categories:
            category.clear_home_works()

    def get_final_exam_by_date_time(self, date_time):
        for final_exam in self.final_exams:
            if final_exam.date_time == date_time:
                return final_exam

    def get_test_by_id(self, item_id):
        for test in self.tests:
            if test.id == item_id:
                return test

    def get_home_work_by_id(self, item_id):
        for home_work_category in self.home_work_categories:
            for home_work in home_work_category.home_works:
                if home_work.id == item_id:
                    return home_work
