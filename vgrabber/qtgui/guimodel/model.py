from PyQt5.QtCore import QObject, pyqtSignal

from vgrabber.datalayer import DataLayer
from vgrabber.model import Subject


class GuiModel(QObject):
    subject: Subject
    data_layer: DataLayer

    subject_changed = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.subject = None
        self.data_layer = DataLayer()

    def close(self):
        self.data_layer.close()
        self.subject = None
        self.subject_changed.emit()

    def load(self, file_accessor):
        self.subject = self.data_layer.load(file_accessor)
        self.subject_changed.emit()

    def save_as(self, file_accessor):
        self.data_layer.save_as(file_accessor, self.subject)
        self.subject_changed.emit()

    def save(self):
        self.data_layer.save(self.subject)
        self.subject_changed.emit()

    def use_subject(self, subject):
        self.subject = subject
        self.subject_changed.emit()

    def quit(self):
        self.data_layer.close()
