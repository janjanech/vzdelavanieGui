from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTreeWidget, QSplitter, QTreeWidgetItem, QMenu

from vgrabber.model import HomeWork
from .widgets.filedetails import FileDetailsWidget
from .helpers.childfileitems import add_file_items, file_double_clicked
from .helpers.stringify import points_or_none
from ..guimodel import GuiModel
from .items import HomeWorkItem, StudentItem
from ..dialogs.editpointswindow import EditPointsWindow


class HomeWorksTab:
    model: GuiModel

    def __init__(self, model):
        self.__home_work_list = QTreeWidget()
        self.__home_work_list.setHeaderLabel("Name")
        self.__home_work_list.itemSelectionChanged.connect(self.__home_work_selected)
        self.__home_work_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.__home_work_list.customContextMenuRequested.connect(self.__home_work_context_menu)

        self.__home_work_details = QTreeWidget()
        self.__home_work_details.setColumnCount(2)
        self.__home_work_details.setHeaderLabels(["Student", "Points"])
        self.__home_work_details.itemActivated.connect(
            lambda item, column: file_double_clicked(self.model, item)
        )
        self.__home_work_details.itemSelectionChanged.connect(self.__home_work_file_selected)

        self.__home_work_file_details = FileDetailsWidget(model)

        details_splitter = QSplitter(Qt.Horizontal)
        details_splitter.addWidget(self.__home_work_details)
        details_splitter.addWidget(self.__home_work_file_details.widget)

        self.widget = QSplitter(Qt.Vertical)
        self.widget.addWidget(self.__home_work_list)
        self.widget.addWidget(details_splitter)
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
        self.__home_work_file_details.master_selection_changed([])

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
        self.__home_work_details.clear()
        self.__home_work_file_details.master_selection_changed([])

        home_work_items = self.__home_work_list.selectedItems()
        if home_work_items and isinstance(home_work_items[0], HomeWorkItem):
            home_work: HomeWork = home_work_items[0].home_work

            for home_work_points in home_work.get_submissions():
                student_item = StudentItem(
                    [
                        f"{home_work_points.student.surname} {home_work_points.student.name}",
                        points_or_none(home_work_points.points)
                    ],
                    home_work_points.student
                )

                self.__home_work_details.addTopLevelItem(student_item)
                add_file_items(home_work_points.files, student_item)

            self.__home_work_details.expandAll()

    def __home_work_file_selected(self):
        self.__home_work_file_details.master_selection_changed(
            self.__home_work_details.selectedItems()
        )
    
    def __home_work_context_menu(self, pos):
        item = self.__home_work_list.itemAt(pos)
        
        if isinstance(item, HomeWorkItem):
            menu = QMenu()
            menu.addAction("Edit points").triggered.connect(
                lambda *args: EditPointsWindow(self.model, item.home_work).run()
            )
            menu.exec(self.__home_work_list.viewport().mapToGlobal(pos))
