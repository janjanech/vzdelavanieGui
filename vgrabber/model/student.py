class Student:
    def __init__(self, number, name, surname, group):
        self.number = number
        self.name = name
        self.surname = surname
        self.group = group

    def __str__(self):
        return "<Student {0} {1} in group {2}, number {3}>".format(self.name, self.surname, self.group, self.number)
