from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem

from ..guimodel import GuiModel


class StudentsTab:
    model: GuiModel

    def __init__(self, model):
        self.widget = QTreeWidget()
        self.widget.setColumnCount(4)
        self.widget.setHeaderLabels(["Number", "Full Name", "Group", "Moodle email"])

        self.model = model
        self.__load_students()

        self.model.subject_changed.connect(self.__subject_changed)

    def __subject_changed(self):
        self.__load_students()

    def __load_students(self):
        self.widget.clear()

        if self.model.subject is not None:
            for student in self.model.subject.students:
                item = QTreeWidgetItem([
                    student.number,
                    f"{student.name} {student.surname}",
                    student.group,
                    student.moodle_email
                ])
                self.widget.addTopLevelItem(item)
