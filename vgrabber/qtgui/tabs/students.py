from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QSplitter

from vgrabber.model import Student
from .helpers.childfileitems import add_file_items, file_double_clicked
from .helpers.stringify import points_or_none, grade_or_none
from .items import StudentItem
from ..guimodel import GuiModel


class StudentsTab:
    model: GuiModel

    def __init__(self, model):
        self.__student_list = QTreeWidget()
        self.__student_list.setSortingEnabled(True)
        self.__student_list.setColumnCount(5)
        self.__student_list.setHeaderLabels(["Number", "Full Name", "Group", "Moodle email", "Moodle group"])
        self.__student_list.itemSelectionChanged.connect(self.__student_selected)

        self.__student_details = QTreeWidget()
        self.__student_details.setColumnCount(4)
        self.__student_details.setHeaderLabels(["Type", "Activity name", "Points", "Grade"])
        self.__student_details.itemDoubleClicked.connect(file_double_clicked)

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
        self.__student_details.clear()

        if self.model.subject is not None:
            for student in self.model.subject.students:
                moodle_group = student.get_moodle_group()
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
                add_file_items(homework_points.files, homework_item)

            for test_points in student.test_points:
                test_item = QTreeWidgetItem([
                    "Test",
                    test_points.test.name,
                    points_or_none(test_points.points),
                    ""
                ])
                self.__student_details.addTopLevelItem(test_item)
                add_file_items(test_points.files, test_item)

            for grade in student.grades:
                grade_item = QTreeWidgetItem([
                    "Final Exam",
                    grade.final_exam.date_time.strftime("%c"),
                    points_or_none(grade.points),
                    grade_or_none(grade.grade)
                ])
                self.__student_details.addTopLevelItem(grade_item)
                add_file_items(grade.files, grade_item)

        self.__student_details.expandAll()
