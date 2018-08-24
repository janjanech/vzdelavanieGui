from seleniumrequests import Chrome
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from .actionexecutor import ActionExecutor


class LoginActionExecutor(ActionExecutor):
    def __init__(self, state):
        super().__init__(state)

        self.__state = state

    def condition(self):
        return True

    def exec(self):
        browser: Chrome = self.__state.browser

        browser.get('http://vzdelavanie.uniza.sk/vzdelavanie/login.php')
        browser.find_element_by_name('meno').send_keys(self.__state.login)
        browser.find_element_by_name('heslo').send_keys(self.__state.password)
        browser.find_element_by_id('login').click()

        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.LINK_TEXT, 'Zmena hesla')))
