from seleniumrequests import Chrome

from vgrabber.model import Subject, Group
from .actionexecutor import ActionExecutor


class MoodleTeacherGroupsActionExecutor(ActionExecutor):
    def __init__(self, state):
        super().__init__(state)
        self.__state = state

    def exec(self):
        browser: Chrome = self.__state.browser
        model: Subject = self.__state.model

        administration_expander = browser.find_elements_by_xpath(
            '//p[span/text()="Administratíva kurzu" and ./following-sibling::ul/@aria-hidden="true"]'
        )

        if administration_expander:
            administration_expander[0].click()

        browser.find_element_by_xpath("//span[text()='Používatelia']").click()
        browser.find_element_by_link_text("Skupiny").click()

        model.clear_teacher_groups()

        for group_option in browser.find_elements_by_css_selector('select#groups option'):
            group_name = group_option.text.split('(')[0].strip()
            moodle_id = int(group_option.get_attribute('value'))
            if '-' in group_name:
                group_number, teacher_surname, *rest = group_name.split('-')
                group_number = group_number.strip()
                teacher = model.get_teacher_by_surname(teacher_surname.strip())
            elif ' ' in group_name:
                group_number, teacher_surname, *rest = group_name.split()
                group_number = group_number.strip()
                teacher = model.get_teacher_by_surname(teacher_surname.strip())
            else:
                group_number = None
                teacher = model.get_unknown_teacher()

            group = Group(group_number, moodle_id, group_name)
            teacher.add_taught_group(group)

