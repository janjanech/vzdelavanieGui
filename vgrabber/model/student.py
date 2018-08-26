class Student:
    def __init__(self, number, name, surname, group):
        self.number = number
        self.name = name
        self.surname = surname
        self.group = group
        self.grades = []

    def __str__(self):
        graded = ""
        if self.grades:
            graded = ", graded {0}".format(self.grades[-1])
        return "<Student {0} {1} in group {2}, number {3}{4}>".format(
            self.name,
            self.surname,
            self.group,
            self.number,
            graded
        )

    def add_grade(self, grade):
        self.grades.append(grade)

    def clear_grades(self):
        pass
