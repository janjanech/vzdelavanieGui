from PyQt5.QtCore import QObject, pyqtSignal

from vgrabber.model import Subject


class GuiModel(QObject):
    subject: Subject
    saved: str

    subject_changed = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.subject = None
        self.saved_as = None

    def use_subject(self, subject, saved_as=None):
        self.subject = subject
        if saved_as is not None:
            self.saved_as = saved_as
        elif subject is None:
            self.saved_as = None
        self.subject_changed.emit()
