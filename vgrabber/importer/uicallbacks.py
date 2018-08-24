from abc import ABC, abstractmethod
from collections import namedtuple


class UiCallbacks(ABC):
    subject_info = namedtuple('subject_info', ['number', 'name'])

    @abstractmethod
    def select_subject(self, subject_list):
        pass
