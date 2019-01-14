from selenium.webdriver.common.keys import Keys
from seleniumrequests import Chrome

from vgrabber.model import Subject
from .actionexecutor import ActionExecutor


class ExportSemestralPointsActionExecutor(ActionExecutor):
    def __init__(self, state):
        super().__init__(state)
        self.__state = state
    
    def exec(self):
        browser: Chrome = self.__state.browser
        model: Subject = self.__state.model
        
        browser.find_element_by_link_text('Zabezpečované predmety').click()
        tag = browser.find_element_by_xpath(
            "//tr[starts-with(.//a/text(), {0!r})]//a[starts-with(@href, 'znpredmet')]".format(model.number)
        )
        tag.click()
        
        has_changes = False
        
        for student in model.students:
            point_inputs = browser.find_elements_by_xpath(
                '//table[@class="data"]//tr[.//td/text()="{0}"]//td[4]//input'.format(student.number))
            
            points = student.compute_semestral_grading()
            if abs(points - int(points)) < 0.1:
                points = int(points)
            
            if not any(point_inputs):
                if points:
                    print(f'{student.name} {student.surname} not found, cannot assign {points} points')
                continue

            point_input, = point_inputs
            old_points = point_input.get_attribute('value')
            
            if old_points != str(points):
                if old_points:
                    print(f'{student.name} {student.surname} should have {points}, but have {old_points}')
                else:
                    print(f'{student.name} {student.surname} should have {points}')
                point_input.send_keys(Keys.HOME)
                point_input.send_keys(Keys.SHIFT + Keys.END)
                point_input.send_keys(str(points))
                has_changes = True
        
        if has_changes:
            browser.find_element_by_xpath('//input[@id="sgn_btn2"]').click()
