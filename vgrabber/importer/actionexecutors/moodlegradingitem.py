import datetime
import re
from urllib.parse import urlparse, parse_qs

from seleniumrequests import Chrome

from ..importaction import ImportAction
from vgrabber.model import Subject, Test
from vgrabber.utilities.accents import strip_accents
from .actionexecutor import ActionExecutor


class MoodleGradingItemActionExecutor(ActionExecutor):
    __re_non_number = re.compile('[^0-9]')

    def __init__(self, state):
        super().__init__(state)
        self.__state = state

        self.__import_final_exams = bool(self.__state.requested_actions & {ImportAction.moodle_final_exam_list})
        self.__import_home_works = bool(self.__state.requested_actions & {ImportAction.moodle_home_work_list})
        self.__import_tests = bool(self.__state.requested_actions & {ImportAction.moodle_test_list})

    def exec(self):
        browser: Chrome = self.__state.browser
        model: Subject = self.__state.model

        browser.find_element_by_link_text('Nastavenie hodnotenia').click()

        grade_items = []

        if self.__import_tests:
            model.clear_tests()

        for category in browser.find_elements_by_css_selector('.gradeitemheader'):
            if category.tag_name == 'a':
                href = urlparse(category.get_attribute('href'))
                href_query = parse_qs(href.query)
                item_name = category.text
                if '/quiz/' in href.path:
                    item_id = int(href_query["id"][0])
                    grade_items.append(self.__get_test(item_name, item_id))
                elif '/assign/' in href.path:
                    item_id = int(href_query["id"][0])
                    if 'skuska' in strip_accents(item_name).lower():
                        grade_items.append(self.__get_final_exam(item_name, item_id))
                    else:
                        grade_items.append((item_id, "homework", item_name))
                else:
                    grade_items.append(None)
            else:
                grade_items.append(None)

        self.__state.use_grade_items(grade_items)

    def __get_final_exam(self, item_name, item_id):
        date_time_tuple = self.__re_non_number.sub(' ', item_name).split()
        date_time_tuple = [int(i) for i in date_time_tuple]

        final_exam = self.__get_final_exam_by_date(*date_time_tuple)

        if final_exam is None:
            final_exam = self.__get_final_exam_by_date_rev(*date_time_tuple)

        if final_exam is None:
            return None

        if self.__import_final_exams:
            final_exam.moodle_id = item_id

        return final_exam

    def __get_final_exam_by_date(self, day, month, year, hour, minute):
        model: Subject = self.__state.model

        if year < 50:
            year += 2000
        elif year < 100:
            year += 1900

        date_time = datetime.datetime(year, month, day,hour, minute)

        return model.get_final_exam_by_date_time(date_time)

    def __get_final_exam_by_date_rev(self, year, month, day, hour, minute):
        return self.__get_final_exam_by_date(day, month, year, hour, minute)

    def __get_test(self, item_name, item_id):
        model: Subject = self.__state.model

        if self.__import_tests:
            test = Test(item_id, item_name, item_id)
            model.add_test(test)
            return test
        else:
            return model.get_test_by_id(item_id)
