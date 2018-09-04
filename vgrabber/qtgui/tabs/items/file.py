from PyQt5.QtWidgets import QTreeWidgetItem

from vgrabber.model.files import StoredFile


class FileItem(QTreeWidgetItem):
    file: StoredFile

    def __init__(self, data, file):
        super().__init__(data)
        self.file = file
