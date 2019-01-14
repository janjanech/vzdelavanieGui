from .actionexecutors import LoginActionExecutor, SelectSubjectActionExecutor, FinalExamActionExecutor, \
    StudentInfoActionExecutor, MoodleStudentListActionExecutor, SwitchToMoodleActionExecutor, \
    MoodleGradingItemActionExecutor, MoodleGradesActionExecutor, FileDownloaderActionExecutor, \
    TestDownloaderActionExecutor, MoodleTeacherGroupsActionExecutor
from vgrabber.base.importaction import ImportAction
from .syncer import Syncer


class Importer(Syncer):
    actions = (
        (ImportAction.all, LoginActionExecutor),
        (ImportAction.all, SelectSubjectActionExecutor),
        ({ImportAction.final_exam_list}, FinalExamActionExecutor),
        ({ImportAction.student_list, ImportAction.grades}, StudentInfoActionExecutor),
        (ImportAction.moodle_all, SwitchToMoodleActionExecutor),
        ({ImportAction.moodle_student_list, ImportAction.moodle_teacher_list}, MoodleStudentListActionExecutor),
        (
            {
                ImportAction.moodle_home_work_list, ImportAction.moodle_home_work_grades,
                ImportAction.moodle_test_list, ImportAction.moodle_test_grades,
                ImportAction.moodle_final_exam_list, ImportAction.moodle_final_exam_grades
            },
            MoodleGradingItemActionExecutor
        ),
        (
            {
                ImportAction.moodle_home_work_grades, ImportAction.moodle_test_grades,
                ImportAction.moodle_final_exam_grades
            },
            MoodleGradesActionExecutor
        ),
        (
            {ImportAction.moodle_home_work_details, ImportAction.moodle_final_exam_details},
            FileDownloaderActionExecutor
        ),
        ({ImportAction.moodle_test_details}, TestDownloaderActionExecutor),
        ({ImportAction.moodle_teacher_groups}, MoodleTeacherGroupsActionExecutor),
    )
