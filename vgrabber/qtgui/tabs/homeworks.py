from PyQt5.QtCore import Qt, QFileInfo, QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QTreeWidget, QSplitter, QTreeWidgetItem, QFileIconProvider

from vgrabber.model import HomeWork
from vgrabber.model.files import StoredFile
from vgrabber.qtgui.guimodel import GuiModel


class HomeWorkItem(QTreeWidgetItem):
    def __init__(self, data, home_work):
        super().__init__(data)
        self.home_work = home_work


class StudentItem(QTreeWidgetItem):
    def __init__(self, data, student):
        super().__init__(data)
        self.student = student


class FileItem(QTreeWidgetItem):
    file: StoredFile

    def __init__(self, data, file):
        super().__init__(data)
        self.file = file


class HomeWorksTab:
    model: GuiModel

    def __init__(self, model):
        self.__home_work_list = QTreeWidget()
        self.__home_work_list.setHeaderLabel("Name")
        self.__home_work_list.itemSelectionChanged.connect(self.__home_work_selected)

        self.__home_work_details = QTreeWidget()
        self.__home_work_details.setColumnCount(2)
        self.__home_work_details.setHeaderLabels(["Student", "Points"])
        self.__home_work_details.itemDoubleClicked.connect(self.__detail_double_clicked)

        self.widget = QSplitter(Qt.Vertical)
        self.widget.addWidget(self.__home_work_list)
        self.widget.addWidget(self.__home_work_details)
        self.widget.setStretchFactor(0, 3)
        self.widget.setStretchFactor(1, 1)

        self.model = model
        self.__load_home_works()

        self.model.subject_changed.connect(self.__subject_changed)

    def __subject_changed(self):
        self.__load_home_works()

    def __load_home_works(self):
        self.__home_work_list.clear()
        self.__home_work_details.clear()

        if self.model.subject is not None:
            for category in self.model.subject.home_work_categories:
                category_item = QTreeWidgetItem([category.name])
                self.__home_work_list.addTopLevelItem(category_item)

                for home_work in category.home_works:
                    home_work_item = HomeWorkItem(
                        [home_work.name],
                        home_work
                    )
                    category_item.addChild(home_work_item)

        self.__home_work_list.expandAll()

    def __home_work_selected(self):
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

        self.__home_work_details.clear()

        home_work_items = self.__home_work_list.selectedItems()
        if home_work_items and isinstance(home_work_items[0], HomeWorkItem):
            home_work: HomeWork = home_work_items[0].home_work

            for student in self.model.subject.students:
                for home_work_points in student.home_work_points:
                    if home_work_points.home_work is home_work:
                        student_item = StudentItem(
                            [
                                f"{student.surname} {student.name}",
                                points_or_none(home_work_points.points)
                            ],
                            student
                        )

                        self.__home_work_details.addTopLevelItem(student_item)
                        add_files(home_work_points.files, student_item)

            self.__home_work_details.expandAll()

    def __detail_double_clicked(self, item, column):
        if isinstance(item, FileItem):
            QDesktopServices.openUrl(QUrl.fromLocalFile(item.file.file_path))
