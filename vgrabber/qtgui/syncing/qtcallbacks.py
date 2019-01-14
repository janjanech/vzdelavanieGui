from vgrabber.syncer import UiCallbacks
from .subjectselector import SubjectSelectorDialog


class QtCallbacks(UiCallbacks):
    def select_subject(self, subject_list):
        return SubjectSelectorDialog(subject_list).exec()
