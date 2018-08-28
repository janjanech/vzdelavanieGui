from .actionexecutors import LoginActionExecutor, SelectSubjectActionExecutor, FinalExamActionExecutor,\
    StudentInfoActionExecutor, MoodleStudentListActionExecutor, SwitchToMoodleActionExecutor
from .importaction import ImportAction
from .state import ImporterState


class Importer:
    __actions = (
        (ImportAction.all, LoginActionExecutor),
        (ImportAction.all, SelectSubjectActionExecutor),
        ({ImportAction.final_exam_list}, FinalExamActionExecutor),
        ({ImportAction.student_list, ImportAction.grades}, StudentInfoActionExecutor),
        (ImportAction.moodle_all, SwitchToMoodleActionExecutor),
        ({ImportAction.moodle_student_list, ImportAction.moodle_teacher_list}, MoodleStudentListActionExecutor)
    )

    def __init__(self, login, password, actions, ui_callbacks, model=None):
        self.__requested_actions = actions
        self.__state = ImporterState(login, password, actions, ui_callbacks, model)
        self.model = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__state.finish()

    def exec(self):
        for for_actions, executor in self.__actions:
            if for_actions & self.__requested_actions:
                e = executor(self.__state)
                if e.condition():
                    e.exec()

        self.__state.finish_actions()

        self.model = self.__state.model
