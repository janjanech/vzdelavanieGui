from vgrabber.importer import ImportAction


class ProgressChecker:
    __progress_xpaths = (
        (ImportAction.student_list, '//students/student'),
        (ImportAction.final_exam_list, '//finalexams/finalexam'),
        (ImportAction.grades, '//student/finalexam[@grade]'),
        (ImportAction.moodle_student_list, '//students/student[@moodleid]'),
        (ImportAction.moodle_teacher_list, '//teachers/teacher'),
        (ImportAction.moodle_final_exam_list, '//finalexams/finalexam[@moodleid]'),
        (ImportAction.moodle_test_list, '//tests/test'),
        (ImportAction.moodle_home_work_list, '//homeworks/category/homework'),
    )

    def __init__(self, subject_element):
        self.__subject_element = subject_element

    def find_out_progress(self):
        for action, xpath in self.__progress_xpaths:
            if any(True for i in self.__subject_element.xpath(xpath)):
                yield action
