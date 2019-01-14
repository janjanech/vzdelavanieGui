from PyQt5.QtWidgets import QTreeWidgetItem


class FileItem(QTreeWidgetItem):
    def __init__(self, data, file):
        super().__init__(data)
        self.file = file
