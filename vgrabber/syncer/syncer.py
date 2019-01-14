from abc import ABC, abstractmethod

from .state import SyncerState


class Syncer(ABC):
    @property
    @abstractmethod
    def actions(self):
        pass

    def __init__(self, login, password, actions, ui_callbacks, model=None):
        self.__requested_actions = actions
        self.__state = SyncerState(login, password, actions, ui_callbacks, model)
        self.model = model

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__state.finish()

    def exec(self):
        for for_actions, executor in self.actions:
            if for_actions & self.__requested_actions:
                e = executor(self.__state)
                if e.condition():
                    e.exec()

        self.model = self.__state.model
