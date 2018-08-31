import csv
import logging
from collections import OrderedDict
from itertools import islice

from seleniumrequests import Chrome

from ..importaction import ImportAction
from vgrabber.model import Subject, Test, HomeWork, FinalExam
from .actionexecutor import ActionExecutor


class MoodleGradesActionExecutor(ActionExecutor):
    __force_data = {
        'export_onlyactive': '1',
        'display[real]': '1',
        'decimals': '2',
        'separator': 'comma',
        'id_checkbox_controller1': '1'
    }

    def __init__(self, state):
        super().__init__(state)
        self.__state = state

        self.__import_final_exams = bool(self.__state.requested_actions & {ImportAction.moodle_final_exam_grades})
        self.__import_home_works = bool(self.__state.requested_actions & {ImportAction.moodle_home_work_grades})
        self.__import_tests = bool(self.__state.requested_actions & {ImportAction.moodle_test_grades})

    def exec(self):
        browser: Chrome = self.__state.browser
        model: Subject = self.__state.model

        if self.__import_final_exams:
            model.clear_final_exam_points()

        if self.__import_home_works:
            model.clear_home_work_points()

        if self.__import_tests:
            model.clear_test_points()

        browser.find_element_by_xpath("//span[text()='Export']").click()
        browser.find_element_by_link_text('Čistý textový súbor (TXT)').click()

        to_send = OrderedDict()

        for input_element in browser.find_elements_by_xpath("//form[@id='mform1']//input[@type='hidden']"):
            input_name = input_element.get_attribute('name')
            input_value = input_element.get_attribute('value')
            if input_name not in self.__force_data and not input_name.startswith('itemids['):
                to_send[input_name] = input_value

        to_send.update(self.__force_data)

        exported_csv = browser.request(
            'POST',
            'https://vzdelavanie.uniza.sk/moodle3/grade/export/txt/export.php',
            data = to_send
        ).text

        for row in islice(csv.reader(exported_csv.splitlines()), 1, None):
            student_email = row[5]
            student = model.get_student_by_email(student_email)

            grades = []
            for grade in row[6:-1]:
                if grade == '-' or not grade:
                    grades.append(0)
                else:
                    try:
                        grades.append(float(grade))
                    except:
                        grades.append(0)

            if not any(grades):
                continue

            if student is None:
                logging.log(
                    logging.WARN,
                    "Student {0} {1} with email {2} not found".format(row[0], row[1], student_email)
                )
                continue

            for grade_item, grade in zip(self.__state.grade_items, grades):
                if grade_item is None or grade == 0:
                    continue
                if isinstance(grade_item, Test) and self.__import_tests:
                    student.add_test_points(grade_item, grade)
                if isinstance(grade_item, HomeWork) and self.__import_home_works:
                    student.add_home_work_points(grade_item, grade)
                if isinstance(grade_item, FinalExam) and self.__import_final_exams:
                    student.add_final_exam_points(grade_item, grade)
