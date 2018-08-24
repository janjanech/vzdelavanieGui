from .actionexecutors import LoginActionExecutor
from .importaction import ImportAction
from .state import ImporterState


class Importer:
    __actions = (
        (ImportAction.all, LoginActionExecutor),
    )

    def __init__(self, login, password, actions, ui_callbacks):
        self.__requested_actions = actions
        self.__state = ImporterState(login, password, actions, ui_callbacks)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__state.finish()

    def exec(self):
        for for_actions, executor in self.__actions:
            if for_actions & self.__requested_actions:
                executor(self.__state).exec()
