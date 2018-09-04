import base64
import datetime

from seleniumrequests import Chrome

from vgrabber.model import Subject, FinalExam
from .actionexecutor import ActionExecutor


class FinalExamActionExecutor(ActionExecutor):
    def __init__(self, state):
        super().__init__(state)
        self.__state = state

    def exec(self):
        browser: Chrome = self.__state.browser
        model: Subject = self.__state.model

        browser.find_element_by_link_text('Zabezpečované predmety').click()

        tag = browser.find_element_by_xpath(
            "//tr[starts-with(.//a/text(), {0!r})]//a[starts-with(@href, 'terminy')]".format(model.number)
        )
        tag.click()

        model.clear_final_exams()

        for row in browser.find_elements_by_xpath("//tr[not(.//tr) and .//td[text()='riadny termín']]"):
            date, time = row.find_element_by_xpath(".//td[2]").text.replace('/', ' ').split(None, 1)

            date_time = datetime.datetime.strptime("{0} {1}".format(date, time), "%d.%m.%Y %H:%M")

            room = row.find_element_by_xpath(".//td[3]").text
            id_href = row.find_element_by_xpath(".//td//a[starts-with(@href, 'terminy')]") \
                .get_attribute("href")
            id_base64 = id_href.split('pid=')[1]

            id = int(base64.b64decode(id_base64).decode('ascii').split('-')[3])

            model.add_final_exam(FinalExam(model, date_time, room, id))
