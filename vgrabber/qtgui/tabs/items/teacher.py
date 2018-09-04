from PyQt5.QtWidgets import QTreeWidgetItem


class TeacherItem(QTreeWidgetItem):
    def __init__(self, data, teacher):
        super().__init__(data)
        self.teacher = teacher
