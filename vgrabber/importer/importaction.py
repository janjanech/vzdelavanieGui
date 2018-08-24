from enum import Enum, auto


class ImportAction(Enum):
    student_list = auto()
    final_exam_list = auto()
    grades = auto()
    moodle_student_list = auto()
    moodle_home_work_list = auto()
    moodle_home_work_grades = auto()
    moodle_home_work_details = auto()
    moodle_final_exam_list = auto()
    moodle_final_exam_details = auto()


ImportAction.student_list.depends = ()
ImportAction.final_exam_list.depends = ()
ImportAction.grades.depends = (ImportAction.final_exam_list, ImportAction.student_list)
ImportAction.moodle_student_list.depends = (ImportAction.student_list, )
ImportAction.moodle_home_work_list.depends = (ImportAction.moodle_student_list, )
ImportAction.moodle_home_work_grades.depends = (ImportAction.moodle_home_work_list, )
ImportAction.moodle_home_work_details.depends = (ImportAction.moodle_home_work_grades, )
ImportAction.moodle_final_exam_list.depends = (ImportAction.moodle_student_list, ImportAction.final_exam_list)
ImportAction.moodle_final_exam_details.depends = (ImportAction.moodle_final_exam_list, )

ImportAction.default = ()
ImportAction.all = frozenset(ImportAction)
