from seleniumrequests import Chrome

from ..importaction import ImportAction
from vgrabber.model import Subject, Student
from .actionexecutor import ActionExecutor


class StudentInfoActionExecutor(ActionExecutor):
    def __init__(self, state):
        super().__init__(state)
        self.__state = state

    def exec(self):
        browser: Chrome = self.__state.browser
        model: Subject = self.__state.model

        import_list = bool(self.__state.requested_actions & {ImportAction.student_list})
        import_grades = bool(self.__state.requested_actions & {ImportAction.grades})

        browser.find_element_by_link_text('Zabezpečované predmety').click()
        tag = browser.find_element_by_xpath(
            "//tr[starts-with(.//a/text(), {0!r})]//a[starts-with(@href, 'znpredmet')]".format(model.number)
        )
        tag.click()

        if import_list:
            model.clear_students()
            for row in browser.find_elements_by_xpath('//table[@class="data"]//tr[not(./th)]'):
                name, surname = row.find_element_by_xpath('.//td[2]//b').text.lstrip('*+-').split(None, 1)
                group = row.find_element_by_xpath('.//td[1]').text
                number = row.find_element_by_xpath('.//td[3]').text

                model.add_student(Student(number, name, surname, group))

        if import_grades:
            pass
