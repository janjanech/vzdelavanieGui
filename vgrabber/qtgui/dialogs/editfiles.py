from functools import partial

from PyQt5.QtCore import QFileInfo, Qt
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QDialogButtonBox, QComboBox, QTreeWidget, QTreeWidgetItem, QWidget, \
    QHBoxLayout, QLabel, QPushButton, QFileIconProvider, QFileDialog

from vgrabber.model.files import ExternalFile

fip = QFileIconProvider()


class EditFilesDialog:
    def __init__(self, model, owner_object):
        self.model = model
        self.__owner_object = owner_object
        
        self.__added_files = []
        
        self.__window = QDialog()
        layout = QVBoxLayout()
        self.__window.setLayout(layout)
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.__window.accept)
        button_box.rejected.connect(self.__window.reject)
        
        self.__group_widget = QComboBox()
        self.__group_widget.addItem("- all -", None)
        for teacher in model.subject.teachers:
            for group in teacher.taught_groups:
                self.__group_widget.addItem(group.moodle_name, group)
        layout.addWidget(self.__group_widget)
        
        self.__files_widget = QTreeWidget()
        self.__files_widget.setHeaderHidden(True)
        layout.addWidget(self.__files_widget)
        
        layout.addWidget(button_box)
        
        self.__refresh_students()
        self.__group_widget.currentIndexChanged.connect(lambda *args: self.__refresh_students())
    
    def __refresh_students(self):
        self.__files_widget.clear()
        
        group = self.__group_widget.itemData(self.__group_widget.currentIndex())
        if group is None:
            students = self.model.subject.students
        else:
            students = list(group.get_students())
        
        for no, student in enumerate(students):
            name_item = QTreeWidgetItem()
            self.__files_widget.addTopLevelItem(name_item)
            name_widget = QWidget()
            name_layout = QHBoxLayout()
            name_layout.setAlignment(Qt.AlignLeft)
            name_layout.setContentsMargins(0, 0, 0, 0)
            name_layout.addWidget(QLabel(f"{student.name} {student.surname}"))
            add_button = QPushButton("Add")
            add_button.clicked.connect(partial(self.__choose_and_add_file, name_item, student))
            name_layout.addWidget(add_button)
            name_widget.setLayout(name_layout)
            self.__add_files(student.get_points_for(self.__owner_object), name_item)
            self.__files_widget.setItemWidget(name_item, 0, name_widget)
        
        self.__files_widget.expandAll()
    
    def __add_files(self, points_object, parent_item):
        if points_object is None:
            return
        for file in points_object.files:
            self.__add_one_file(file, parent_item, False)
    
    def __add_one_file(self, file, parent_item, changed):
        file_item = QTreeWidgetItem([file.file_name])
        file_item.setIcon(0, fip.icon(QFileInfo(file.file_name)))
        if changed:
            file_item.setBackground(0, QBrush(QColor(255, 255, 0)))
        parent_item.addChild(file_item)
    
    def __choose_and_add_file(self, parent_item, student, *args):
        file_name, filter = QFileDialog.getOpenFileName(
            self.__window,
            caption="Add File"
        )
        
        if file_name:
            file = ExternalFile(file_name)
            self.__added_files.append((student, file))
            self.__add_one_file(file, parent_item, True)
    
    def run(self):
        if self.__window.exec() == QDialog.Accepted:
            for student, file in self.__added_files:
                student.add_file_for(self.__owner_object, file)
            self.model.data_edited()
