from abc import ABC, abstractmethod


class ActionExecutor(ABC):
    @abstractmethod
    def __init__(self, state):
        pass

    @abstractmethod
    def condition(self):
        return True

    @abstractmethod
    def exec(self):
        pass
