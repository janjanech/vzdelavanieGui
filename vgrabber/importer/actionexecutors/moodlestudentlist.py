import unicodedata
from urllib.parse import urlparse, parse_qs

import logging
from seleniumrequests import Chrome

from ..importaction import ImportAction
from vgrabber.model import Subject, Student
from .moodleactionexecutor import MoodleActionExecutor


class MoodleStudentListActionExecutor(MoodleActionExecutor):
    def __init__(self, state):
        super().__init__(state)
        self.__state = state

    @staticmethod
    def __strip_accents(s):
        return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

    def exec_in_moodle(self):
        browser: Chrome = self.__state.browser
        model: Subject = self.__state.model

        import_students = bool(self.__state.requested_actions & {ImportAction.moodle_student_list})
        import_teachers = bool(self.__state.requested_actions & {ImportAction.moodle_teacher_list})

        browser.find_element_by_xpath("//span[text()='Používatelia']").click()
        browser.find_element_by_link_text("Zapísaní do kurzu").click()

        if import_students:
            students = [
                (self.__strip_accents(student.surname), self.__strip_accents(student.name), student)
                    for student in model.students
            ]

            students_fullname_index = {(student[1], student[0]): student[2] for student in students}
            students_fullname_index.update({(student[0], student[1]): student[2] for student in students})

            browser.find_element_by_xpath("//select[@name='role']/option[text()='Študent']").click()
            browser.find_element_by_css_selector("input#id_submitbutton").click()

            while True:
                for row in browser.find_elements_by_css_selector('tr.userinforow'):
                    img_link = row.find_element_by_xpath(".//a[contains(img/@class, 'userpicture')]")
                    img_link_parsed = urlparse(img_link.get_attribute('href'))
                    moodle_id = int(parse_qs(img_link_parsed.query)['id'][0])

                    for group in row.find_elements_by_css_selector("div.group"):
                        moodle_group = int(group.get_attribute('rel'))
                        break
                    else:
                        # skip students with no group
                        continue

                    name, surname = row.find_element_by_css_selector('div.subfield_userfullnamedisplay').text.rsplit(None, 1)
                    name_s, surname_s = self.__strip_accents(name), self.__strip_accents(surname)

                    email = row.find_element_by_css_selector('div.subfield_email').text

                    if (surname_s, name_s) in students_fullname_index:
                        student = students_fullname_index[(surname_s, name_s)]
                    elif (name_s, surname_s) in students_fullname_index:
                        student = students_fullname_index[(name_s, surname_s)]
                    else:
                        student = Student(None, name, surname, None)
                        model.add_student(student)
                        logging.log(logging.WARN, "Student {0} not found in the student list".format(student))

                    student.moodle_id = moodle_id
                    student.moodle_group = moodle_group
                    student.moodle_email = email

                if not any(browser.find_elements_by_link_text("Ďalší")):
                    break
                browser.find_element_by_link_text("Ďalší").click()
