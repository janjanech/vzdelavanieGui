from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QComboBox, QTableWidget, QDialogButtonBox, QTableWidgetItem


class PointsTableItem(QTableWidgetItem):
    def __init__(self, student, points=None):
        if points is None:
            super().__init__("")
        else:
            super().__init__(str(points).rstrip('.0'))
        self.student = student
    
    @property
    def points(self):
        if self.text().strip():
            try:
                return float(self.text())
            except ValueError:
                return None
        return None

class EditPointsWindow:
    def __init__(self, model, owner_object):
        self.model = model
        self.__owner_object = owner_object
        
        self.__changes = {}
        
        self.__window = QDialog()
        layout = QVBoxLayout()
        self.__window.setLayout(layout)
        
        self.__group_widget = QComboBox()
        self.__group_widget.addItem("- all -", None)
        for teacher in model.subject.teachers:
            for group in teacher.taught_groups:
                self.__group_widget.addItem(group.moodle_name, group)
        layout.addWidget(self.__group_widget)
        
        self.__points_widget = QTableWidget()
        self.__points_widget.setColumnCount(2)
        self.__points_widget.setHorizontalHeaderLabels(["Name", "Points"])
        layout.addWidget(self.__points_widget)
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.__window.accept)
        button_box.rejected.connect(self.__window.reject)
        
        layout.addWidget(button_box)
        
        self.__refresh_students()
        self.__group_widget.currentIndexChanged.connect(lambda *args: self.__refresh_students())
        self.__points_widget.itemChanged.connect(self.__cell_changed)

    def __refresh_students(self):
        self.__highlight_edit = False
        group = self.__group_widget.itemData(self.__group_widget.currentIndex())
        if group is None:
            students = self.model.subject.students
        else:
            students = list(group.get_students())
        
        self.__points_widget.setRowCount(len(students))
        for no, student in enumerate(students):
            name_cell = QTableWidgetItem(f"{student.name} {student.surname}")
            name_cell.setFlags(name_cell.flags() ^ Qt.ItemIsEditable)
            self.__points_widget.setItem(no, 0, name_cell)
            points = student.get_points_for(self.__owner_object)
            if points is not None:
                self.__points_widget.setItem(no, 1, PointsTableItem(student, points.points))
            else:
                self.__points_widget.setItem(no, 1, PointsTableItem(student))
        self.__highlight_edit = True
    
    def __cell_changed(self, cell):
        if self.__highlight_edit and isinstance(cell, PointsTableItem):
            cell.setBackground(QBrush(QColor(255, 255, 0)))
            self.__group_widget.setEnabled(False)
            
            self.__changes[cell.student] = cell.points
    
    def run(self):
        if self.__window.exec() == QDialog.Accepted:
            for student, points in self.__changes.items():
                student.set_points_for(self.__owner_object, points)
