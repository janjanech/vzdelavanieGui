from PyQt5.QtCore import Qt, QFileInfo, QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QTreeWidget, QSplitter, QTreeWidgetItem, QFileIconProvider

from vgrabber.model import Test
from vgrabber.model.files import StoredFile
from vgrabber.qtgui.guimodel import GuiModel


class TestItem(QTreeWidgetItem):
    def __init__(self, data, test):
        super().__init__(data)
        self.test = test


class StudentItem(QTreeWidgetItem):
    def __init__(self, data, student):
        super().__init__(data)
        self.student = student


class FileItem(QTreeWidgetItem):
    file: StoredFile

    def __init__(self, data, file):
        super().__init__(data)
        self.file = file


class TestsTab:
    model: GuiModel

    def __init__(self, model):
        self.__test_list = QTreeWidget()
        self.__test_list.setHeaderLabel("Name")
        self.__test_list.itemSelectionChanged.connect(self.__test_selected)

        self.__test_details = QTreeWidget()
        self.__test_details.setColumnCount(2)
        self.__test_details.setHeaderLabels(["Student", "Points"])
        self.__test_details.itemDoubleClicked.connect(self.__detail_double_clicked)

        self.widget = QSplitter(Qt.Vertical)
        self.widget.addWidget(self.__test_list)
        self.widget.addWidget(self.__test_details)
        self.widget.setStretchFactor(0, 3)
        self.widget.setStretchFactor(1, 1)

        self.model = model
        self.__load_tests()

        self.model.subject_changed.connect(self.__subject_changed)

    def __subject_changed(self):
        self.__load_tests()

    def __load_tests(self):
        self.__test_list.clear()
        self.__test_details.clear()

        if self.model.subject is not None:
            for test in self.model.subject.tests:
                test_item = TestItem(
                    [test.name],
                    test
                )
                self.__test_list.addTopLevelItem(test_item)

    def __test_selected(self):
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

        self.__test_details.clear()

        home_work_items = self.__test_list.selectedItems()
        if home_work_items:
            test: Test = home_work_items[0].test

            for test_points in test.get_submissions():
                student_item = StudentItem(
                    [
                        f"{test_points.student.surname} {test_points.student.name}",
                        points_or_none(test_points.points)
                    ],
                    test_points.student
                )

                self.__test_details.addTopLevelItem(student_item)
                add_files(test_points.files, student_item)

            self.__test_details.expandAll()

    def __detail_double_clicked(self, item, column):
        if isinstance(item, FileItem):
            QDesktopServices.openUrl(QUrl.fromLocalFile(item.file.file_path))
