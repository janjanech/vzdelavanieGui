from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTreeWidget, QSplitter, QTreeWidgetItem


class TeacherItem(QTreeWidgetItem):
    def __init__(self, data, teacher):
        super().__init__(data)
        self.teacher = teacher


class TeachersTab:
    def __init__(self, model):
        self.__teacher_list = QTreeWidget()
        self.__teacher_list.setSortingEnabled(True)
        self.__teacher_list.setColumnCount(2)
        self.__teacher_list.setHeaderLabels(["Full Name", "Moodle email"])

        self.__teacher_details = QTreeWidget()

        self.widget = QSplitter(Qt.Vertical)
        self.widget.addWidget(self.__teacher_list)
        self.widget.addWidget(self.__teacher_details)
        self.widget.setStretchFactor(0, 3)
        self.widget.setStretchFactor(1, 1)

        self.model = model
        self.__load_teachers()

        self.model.subject_changed.connect(self.__subject_changed)

    def __subject_changed(self):
        self.__load_teachers()

    def __load_teachers(self):
        self.__teacher_list.clear()

        if self.model.subject is not None:
            for teacher in self.model.subject.teachers:
                item = TeacherItem(
                    [
                        f"{teacher.surname} {teacher.name}",
                        teacher.moodle_email
                    ],
                    teacher
                )
                self.__teacher_list.addTopLevelItem(item)
