from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTreeWidget, QSplitter

from vgrabber.model import FinalExam
from vgrabber.qtgui.tabs.widgets.filedetails import FileDetailsWidget
from .helpers.childfileitems import add_file_items, file_double_clicked
from .helpers.stringify import points_or_none, grade_or_none
from ..guimodel import GuiModel
from .items import FinalExamItem, StudentItem


class FinalExamsTab:
    model: GuiModel

    def __init__(self, model):
        self.__final_exam_list = QTreeWidget()
        self.__final_exam_list.setHeaderLabels(["Date and time", "Room"])
        self.__final_exam_list.setHeaderLabels(["Date", "Time", "Day", "Room"])
        self.__final_exam_list.itemSelectionChanged.connect(self.__final_exam_selected)

        self.__final_exam_details = QTreeWidget()
        self.__final_exam_details.setColumnCount(3)
        self.__final_exam_details.setHeaderLabels(["Student", "Points", "Grade"])
        self.__final_exam_details.itemActivated.connect(
            lambda item, column: file_double_clicked(self.model, item)
        )
        self.__final_exam_details.itemSelectionChanged.connect(self.__final_exam_file_selected)

        self.__final_exam_file_details = FileDetailsWidget(model)

        details_splitter = QSplitter(Qt.Horizontal)
        details_splitter.addWidget(self.__final_exam_details)
        details_splitter.addWidget(self.__final_exam_file_details.widget)

        self.widget = QSplitter(Qt.Vertical)
        self.widget.addWidget(self.__final_exam_list)
        self.widget.addWidget(details_splitter)
        self.widget.setStretchFactor(0, 3)
        self.widget.setStretchFactor(1, 1)

        self.model = model
        self.__load_final_exam()

        self.model.subject_changed.connect(self.__subject_changed)

    def __subject_changed(self):
        self.__load_final_exam()

    def __load_final_exam(self):
        self.__final_exam_list.clear()
        self.__final_exam_details.clear()

        if self.model.subject is not None:
            for final_exam in self.model.subject.final_exams:
                final_exam_item = FinalExamItem(
                    [
                        final_exam.date_time.strftime("%d.%m.%Y"),
                        final_exam.date_time.strftime("%H:%M"),
                        final_exam.date_time.strftime("%A"),
                        final_exam.room
                    ],
                    final_exam
                )
                self.__final_exam_list.addTopLevelItem(final_exam_item)

    def __final_exam_selected(self):
        self.__final_exam_details.clear()

        final_exam_items = self.__final_exam_list.selectedItems()
        if final_exam_items:
            final_exam: FinalExam = final_exam_items[0].final_exam

            for grade in final_exam.get_submissions():
                student_item = StudentItem(
                    [
                        f"{grade.student.surname} {grade.student.name}",
                        points_or_none(grade.points),
                        grade_or_none(grade.grade)
                    ],
                    grade.student
                )

                self.__final_exam_details.addTopLevelItem(student_item)
                add_file_items(grade.files, student_item)

            self.__final_exam_details.expandAll()

    def __final_exam_file_selected(self):
        self.__final_exam_file_details.master_selection_changed(
            self.__final_exam_details.selectedItems()
        )
