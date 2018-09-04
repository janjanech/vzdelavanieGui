from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTreeWidget, QSplitter, QTreeWidgetItem

from vgrabber.model import Teacher
from ..guimodel import GuiModel


class TeacherItem(QTreeWidgetItem):
    def __init__(self, data, teacher):
        super().__init__(data)
        self.teacher = teacher


class TeachersTab:
    model: GuiModel

    def __init__(self, model):
        self.__teacher_list = QTreeWidget()
        self.__teacher_list.setSortingEnabled(True)
        self.__teacher_list.setColumnCount(2)
        self.__teacher_list.setHeaderLabels(["Full Name", "Moodle email"])
        self.__teacher_list.itemSelectionChanged.connect(self.__teacher_selected)

        self.__teacher_details = QTreeWidget()
        self.__teacher_details.setColumnCount(4)
        self.__teacher_details.setHeaderLabels(["Number", "Full Name", "Group", "Moodle email"])

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
        self.__teacher_details.clear()

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

    def __teacher_selected(self):
        self.__teacher_details.clear()

        teacher_items = self.__teacher_list.selectedItems()
        if teacher_items:
            teacher: Teacher = teacher_items[0].teacher

            for group in teacher.taught_groups:
                if group.moodle_name is None:
                    group_name = f"({group.number})"
                elif group.number is None:
                    group_name = group.moodle_name
                else:
                    group_name = f"{group.moodle_name} ({group.number})"
                group_item = QTreeWidgetItem([group_name])
                self.__teacher_details.addTopLevelItem(group_item)
                group_item.setFirstColumnSpanned(True)

                if group.moodle_id is not None:
                    for student in self.model.subject.students:
                        if student.moodle_group == group.moodle_id:
                            item = QTreeWidgetItem(
                                [
                                    student.number,
                                    f"{student.surname} {student.name}",
                                    student.group,
                                    student.moodle_email
                                ]
                            )

                            group_item.addChild(item)

        self.__teacher_details.expandAll()
