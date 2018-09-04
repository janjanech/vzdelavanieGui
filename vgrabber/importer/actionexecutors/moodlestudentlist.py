from urllib.parse import urlparse, parse_qs

import logging
from seleniumrequests import Chrome

from vgrabber.utilities.accents import strip_accents
from .actionexecutor import ActionExecutor
from vgrabber.base.importaction import ImportAction
from vgrabber.model import Subject, Student, Teacher


class MoodleStudentListActionExecutor(ActionExecutor):
    def __init__(self, state):
        super().__init__(state)
        self.__state = state

    def exec(self):
        browser: Chrome = self.__state.browser
        model: Subject = self.__state.model

        import_students = bool(self.__state.requested_actions & {ImportAction.moodle_student_list})
        import_teachers = bool(self.__state.requested_actions & {ImportAction.moodle_teacher_list})

        browser.find_element_by_xpath("//span[text()='Používatelia']").click()
        browser.find_element_by_link_text("Zapísaní do kurzu").click()

        if import_students:
            students = [
                (strip_accents(student.surname), strip_accents(student.name), student)
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

                    moodle_group = None
                    for group in row.find_elements_by_css_selector("div.group"):
                        moodle_group = int(group.get_attribute('rel'))
                        break

                    name, surname = row.find_element_by_css_selector('div.subfield_userfullnamedisplay').text.rsplit(None, 1)
                    name_s, surname_s = strip_accents(name), strip_accents(surname)

                    email = row.find_element_by_css_selector('div.subfield_email').text

                    if (surname_s, name_s) in students_fullname_index:
                        student = students_fullname_index[(surname_s, name_s)]
                    elif (name_s, surname_s) in students_fullname_index:
                        student = students_fullname_index[(name_s, surname_s)]
                    else:
                        if moodle_group is None:
                            # don't create students if they are not in any group
                            continue

                        student = Student(model, None, name, surname, None)
                        model.add_student(student)
                        logging.log(logging.WARN, "Student {0} not found in the student list".format(student))

                    student.moodle_id = moodle_id
                    student.moodle_group_id = moodle_group
                    student.moodle_email = email

                if not any(browser.find_elements_by_link_text("Ďalší")):
                    break
                browser.find_element_by_link_text("Ďalší").click()

        if import_teachers:
            browser.find_element_by_xpath("//select[@name='role']/option[text()='Učiteľ']").click()
            browser.find_element_by_css_selector("input#id_submitbutton").click()

            model.clear_teachers()

            while True:
                for row in browser.find_elements_by_css_selector('tr.userinforow'):
                    img_link = row.find_element_by_xpath(".//a[contains(img/@class, 'userpicture')]")
                    img_link_parsed = urlparse(img_link.get_attribute('href'))

                    moodle_id = int(parse_qs(img_link_parsed.query)['id'][0])

                    name, surname = row.find_element_by_css_selector('div.subfield_userfullnamedisplay').text.rsplit(None, 1)

                    email = row.find_element_by_css_selector('div.subfield_email').text

                    teacher = Teacher(model, name, surname, moodle_id, email)
                    model.add_teacher(teacher)

                if not any(browser.find_elements_by_link_text("Ďalší")):
                    break
                browser.find_element_by_link_text("Ďalší").click()

