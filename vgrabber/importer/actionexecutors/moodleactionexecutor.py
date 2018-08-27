from abc import ABC, abstractmethod

from seleniumrequests import Chrome

from vgrabber.model import Subject
from .actionexecutor import ActionExecutor


class MoodleActionExecutor(ActionExecutor, ABC):
    def __init__(self, state):
        super().__init__(state)
        self.__state = state

    def exec(self):
        browser: Chrome = self.__state.browser
        model: Subject = self.__state.model

        if '/moodle3/' not in browser.current_url:
            browser.find_element_by_link_text('Zabezpečované predmety').click()

            tag = browser.find_element_by_xpath(
                "//tr[starts-with(.//a/text(), {0!r})]//a[contains(@href, 'moodle')]".format(model.number)
            )
            tag.click()

            browser.close()
            browser.switch_to.window(browser.window_handles[-1])

        self.exec_in_moodle()

    @abstractmethod
    def exec_in_moodle(self):
        pass
