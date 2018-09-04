from PyQt5.QtWidgets import QTreeWidgetItem


class StudentItem(QTreeWidgetItem):
    def __init__(self, data, student):
        super().__init__(data)
        self.student = student
