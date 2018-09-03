from PyQt5.QtCore import QFileInfo, Qt
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QWidget, QVBoxLayout, QFileIconProvider, QSplitter

from vgrabber.model import Student
from ..guimodel import GuiModel


class StudentItem(QTreeWidgetItem):
    def __init__(self, data, student):
        super().__init__(data)
        self.student = student


class StudentsTab:
    model: GuiModel

    def __init__(self, model):
        self.__student_list = QTreeWidget()
        self.__student_list.setSortingEnabled(True)
        self.__student_list.setColumnCount(4)
        self.__student_list.setHeaderLabels(["Number", "Full Name", "Group", "Moodle email", "Moodle group"])
        self.__student_list.itemSelectionChanged.connect(self.__student_selected)

        self.__student_details = QTreeWidget()
        self.__student_details.setColumnCount(4)
        self.__student_details.setHeaderLabels(["Type", "Activity name", "Points", "Grade"])

        self.widget = QSplitter(Qt.Vertical)
        self.widget.addWidget(self.__student_list)
        self.widget.addWidget(self.__student_details)
        self.widget.setStretchFactor(0, 3)
        self.widget.setStretchFactor(1, 1)

        self.model = model
        self.__load_students()

        self.model.subject_changed.connect(self.__subject_changed)

    def __subject_changed(self):
        self.__load_students()

    def __load_students(self):
        self.__student_list.clear()

        if self.model.subject is not None:
            for student in self.model.subject.students:
                moodle_group = self.model.subject.get_group_by_moodle_id(student.moodle_group)
                moodle_group_name = ""
                if moodle_group is not None:
                    moodle_group_name = moodle_group.moodle_name

                item = StudentItem(
                    [
                        student.number,
                        f"{student.surname} {student.name}",
                        student.group,
                        student.moodle_email,
                        moodle_group_name
                    ],
                    student
                )
                self.__student_list.addTopLevelItem(item)

    def __student_selected(self):
        fip = QFileIconProvider()

        def points_or_none(points):
            if points is None:
                return "?"
            else:
                return str(points)

        def add_files(files, item: QTreeWidgetItem):
            for file in files:
                file_item = QTreeWidgetItem([file.file_name])
                file_item.setIcon(0, fip.icon(QFileInfo(file.file_name)))
                item.addChild(file_item)
                file_item.setFirstColumnSpanned(True)

        self.__student_details.clear()

        student_items = self.__student_list.selectedItems()
        if student_items:
            student: Student = student_items[0].student
            for homework_points in student.home_work_points:
                homework_item = QTreeWidgetItem([
                    "Home Work",
                    homework_points.home_work.name,
                    points_or_none(homework_points.points),
                    ""
                ])
                self.__student_details.addTopLevelItem(homework_item)
                add_files(homework_points.files, homework_item)

            for test_points in student.test_points:
                test_item = QTreeWidgetItem([
                    "Test",
                    test_points.test.name,
                    points_or_none(test_points.points),
                    ""
                ])
                self.__student_details.addTopLevelItem(test_item)
                add_files(test_points.files, test_item)

            for grade in student.grades:
                if grade.grade is not None:
                    grade_name = grade.grade.name
                else:
                    grade_name = "?"

                grade_item = QTreeWidgetItem([
                    "Final Exam",
                    grade.final_exam.date_time.strftime("%c"),
                    points_or_none(grade.points),
                    grade_name
                ])
                self.__student_details.addTopLevelItem(grade_item)
                add_files(grade.files, grade_item)

        self.__student_details.expandAll()
