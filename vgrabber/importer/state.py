from selenium.webdriver.chrome.options import Options
from seleniumrequests import Chrome


class ImporterState:
    def __init__(self, login, password, requested_actions, ui_callbacks):
        self.login = login
        self.password = password

        self.requested_actions = requested_actions

        self.ui_callbacks = ui_callbacks
        browser_options = Options()
        # browser_options.add_argument('--headless')
        self.browser = Chrome(chrome_options=browser_options)

    def finish(self):
        self.browser.quit()
        del self.browser
