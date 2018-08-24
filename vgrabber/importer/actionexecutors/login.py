class LoginActionExecutor:
    def __init__(self, state):
        self.__state = state

    def exec(self):
        self.__state.browser.get('http://vzdelavanie.uniza.sk/vzdelavanie/login.php')
        self.__state.browser.find_element_by_name('meno').send_keys(self.__state.login)
        self.__state.browser.find_element_by_name('heslo').send_keys(self.__state.password)
        self.__state.browser.find_element_by_id('login').click()
