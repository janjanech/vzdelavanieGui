from selenium.webdriver import ChromeOptions
from seleniumrequests import Chrome


class SyncerState:
    def __init__(self, login, password, requested_actions, ui_callbacks, model):
        self.login = login
        self.password = password

        self.requested_actions = requested_actions

        self.model = model
        self.grade_items = ()

        self.ui_callbacks = ui_callbacks

        browser_options = ChromeOptions()
        browser_options.add_argument('--headless')
        self.browser = Chrome(chrome_options=browser_options)

    def finish(self):
        self.browser.quit()
        del self.browser

    def use_grade_items(self, grade_items):
        self.grade_items = tuple(grade_items)
