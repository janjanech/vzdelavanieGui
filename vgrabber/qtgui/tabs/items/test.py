from PyQt5.QtWidgets import QTreeWidgetItem


class TestItem(QTreeWidgetItem):
    def __init__(self, data, test):
        super().__init__(data)
        self.test = test
