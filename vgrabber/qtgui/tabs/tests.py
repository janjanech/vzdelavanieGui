from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTreeWidget, QSplitter

from vgrabber.model import Test
from vgrabber.qtgui.tabs.widgets.filedetails import FileDetailsWidget
from ..guimodel import GuiModel
from .helpers.childfileitems import add_file_items, file_double_clicked
from .helpers.stringify import points_or_none
from .items import StudentItem, TestItem


class TestsTab:
    model: GuiModel

    def __init__(self, model):
        self.__test_list = QTreeWidget()
        self.__test_list.setHeaderLabel("Name")
        self.__test_list.itemSelectionChanged.connect(self.__test_selected)

        self.__test_details = QTreeWidget()
        self.__test_details.setColumnCount(2)
        self.__test_details.setHeaderLabels(["Student", "Points"])
        self.__test_details.itemDoubleClicked.connect(
            lambda item, column: file_double_clicked(self.model, item)
        )
        self.__test_details.itemSelectionChanged.connect(self.__test_file_selected)

        self.__test_file_details = FileDetailsWidget(model)

        details_splitter = QSplitter(Qt.Horizontal)
        details_splitter.addWidget(self.__test_details)
        details_splitter.addWidget(self.__test_file_details.widget)

        self.widget = QSplitter(Qt.Vertical)
        self.widget.addWidget(self.__test_list)
        self.widget.addWidget(details_splitter)
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
                add_file_items(test_points.files, student_item)

            self.__test_details.expandAll()

    def __test_file_selected(self):
        self.__test_file_details.master_selection_changed(
            self.__test_details.selectedItems()
        )
