from enum import Enum, auto


class ImportAction(Enum):
    student_list = auto()
    final_exam_list = auto()
    grades = auto()
    moodle_teacher_list = auto()
    moodle_student_list = auto()
    moodle_teacher_groups = auto()
    moodle_home_work_list = auto()
    moodle_home_work_grades = auto()
    moodle_home_work_details = auto()
    moodle_test_list = auto()
    moodle_test_grades = auto()
    moodle_test_details = auto()
    moodle_final_exam_list = auto()
    moodle_final_exam_grades = auto()
    moodle_final_exam_details = auto()


ImportAction.student_list.depends = set()
ImportAction.final_exam_list.depends = set()
ImportAction.grades.depends = {ImportAction.final_exam_list, ImportAction.student_list}
ImportAction.moodle_teacher_list.depends = set()
ImportAction.moodle_teacher_groups.depends = {ImportAction.moodle_teacher_list}
ImportAction.moodle_student_list.depends = {ImportAction.student_list}
ImportAction.moodle_home_work_list.depends = set()
ImportAction.moodle_home_work_grades.depends = {ImportAction.moodle_home_work_list, ImportAction.moodle_student_list}
ImportAction.moodle_home_work_details.depends = {ImportAction.moodle_home_work_grades}
ImportAction.moodle_test_list.depends = set()
ImportAction.moodle_test_grades.depends = {ImportAction.moodle_test_list, ImportAction.moodle_student_list}
ImportAction.moodle_test_details.depends = {ImportAction.moodle_test_grades}
ImportAction.moodle_final_exam_list.depends = {ImportAction.final_exam_list}
ImportAction.moodle_final_exam_grades.depends = {ImportAction.moodle_final_exam_list, ImportAction.moodle_student_list}
ImportAction.moodle_final_exam_details.depends = {ImportAction.moodle_final_exam_grades}

ImportAction.default = ()
ImportAction.all = frozenset(ImportAction)
ImportAction.moodle_all = frozenset(x for x in ImportAction if x.name.startswith('moodle_'))
