from selenium.webdriver.support.select import Select
from seleniumrequests import Chrome

from vgrabber.model import Subject
from ..uicallbacks import UiCallbacks
from .actionexecutor import ActionExecutor


class SelectSubjectActionExecutor(ActionExecutor):
    def __init__(self, state):
        super().__init__(state)
        self.__state = state

    def condition(self):
        return self.__state.model is None

    def exec(self):
        browser: Chrome = self.__state.browser

        browser.find_element_by_link_text('Zabezpečované predmety').click()
        subjects = []
        for name in browser.find_elements_by_xpath('//a[contains(@href, "planinfo.php")][not(img)]'):
            number, name = name.text.split(None, 1)
            subjects.append(UiCallbacks.subject_info(number=number, name=name))

        selected_subject = self.__state.ui_callbacks.select_subject(subjects)

        year_combo = Select(browser.find_element_by_name('ra'))
        year = year_combo.first_selected_option.text.replace(' ', '')

        self.__state.model = Subject(selected_subject.number, selected_subject.name, year)
