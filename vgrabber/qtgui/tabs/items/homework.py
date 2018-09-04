from PyQt5.QtWidgets import QTreeWidgetItem


class HomeWorkItem(QTreeWidgetItem):
    def __init__(self, data, home_work):
        super().__init__(data)
        self.home_work = home_work
