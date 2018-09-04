from PyQt5.QtCore import Qt, QFileInfo, QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QTreeWidget, QSplitter, QTreeWidgetItem, QFileIconProvider

from vgrabber.model import FinalExam
from vgrabber.model.files import StoredFile
from vgrabber.qtgui.guimodel import GuiModel


class FinalExamItem(QTreeWidgetItem):
    def __init__(self, data, final_exam):
        super().__init__(data)
        self.final_exam = final_exam


class StudentItem(QTreeWidgetItem):
    def __init__(self, data, student):
        super().__init__(data)
        self.student = student


class FileItem(QTreeWidgetItem):
    file: StoredFile

    def __init__(self, data, file):
        super().__init__(data)
        self.file = file


class FinalExamsTab:
    model: GuiModel

    def __init__(self, model):
        self.__final_exam_list = QTreeWidget()
        self.__final_exam_list.setHeaderLabels(["Date and time", "Room"])
        self.__final_exam_list.itemSelectionChanged.connect(self.__final_exam_selected)

        self.__final_exam_details = QTreeWidget()
        self.__final_exam_details.setColumnCount(3)
        self.__final_exam_details.setHeaderLabels(["Student", "Points", "Grade"])
        self.__final_exam_details.itemDoubleClicked.connect(self.__detail_double_clicked)

        self.widget = QSplitter(Qt.Vertical)
        self.widget.addWidget(self.__final_exam_list)
        self.widget.addWidget(self.__final_exam_details)
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
                    [final_exam.date_time.strftime("%c"), final_exam.room],
                    final_exam
                )
                self.__final_exam_list.addTopLevelItem(final_exam_item)

    def __final_exam_selected(self):
        fip = QFileIconProvider()

        def points_or_none(points):
            if points is None:
                return "?"
            else:
                return str(points)

        def add_files(files, item: QTreeWidgetItem):
            for file in files:
                if isinstance(file, StoredFile):
                    file_item = FileItem([file.file_name], file)
                else:
                    file_item = QTreeWidgetItem([file.file_name])
                file_item.setIcon(0, fip.icon(QFileInfo(file.file_name)))
                item.addChild(file_item)
                file_item.setFirstColumnSpanned(True)

        self.__final_exam_details.clear()

        final_exam_items = self.__final_exam_list.selectedItems()
        if final_exam_items:
            final_exam: FinalExam = final_exam_items[0].final_exam

            for grade in final_exam.get_submissions():
                if grade.grade is not None:
                    grade_name = grade.grade.name
                else:
                    grade_name = "?"

                student_item = StudentItem(
                    [
                        f"{grade.student.surname} {grade.student.name}",
                        points_or_none(grade.points),
                        grade_name
                    ],
                    grade.student
                )

                self.__final_exam_details.addTopLevelItem(student_item)
                add_files(grade.files, student_item)

            self.__final_exam_details.expandAll()

    def __detail_double_clicked(self, item, column):
        if isinstance(item, FileItem):
            QDesktopServices.openUrl(QUrl.fromLocalFile(item.file.file_path))
