from PyQt5.QtWidgets import QTreeWidgetItem


class StudentItem(QTreeWidgetItem):
    def __init__(self, data, student):
        super().__init__(data)
        self.student = student
    
    def __lt__(self, other):
        column = self.treeWidget().sortColumn()
        try:
            return float(self.text(column)) > float(other.text(column))
        except ValueError:
            return self.text(column) > other.text(column)
