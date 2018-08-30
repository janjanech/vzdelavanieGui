from time import sleep
from urllib.parse import urlparse, parse_qs

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumrequests import Chrome

from vgrabber.model.files import InMemoryFile
from ..importaction import ImportAction
from vgrabber.model import Subject
from .actionexecutor import ActionExecutor


class FileDownloaderActionExecutor(ActionExecutor):
    __html_envelope = '''
    <html>
        <head>
            <meta charset="UTF-8">
        </head>
        <body>
            {0}
        </body>
    </html>
    '''

    def __init__(self, state):
        super().__init__(state)
        self.__state = state

        self.__import_final_exams = bool(self.__state.requested_actions & {ImportAction.moodle_final_exam_details})
        self.__import_home_works = bool(self.__state.requested_actions & {ImportAction.moodle_home_work_details})
        self.__import_tests = bool(self.__state.requested_actions & {ImportAction.moodle_test_details})

    def exec(self):
        browser: Chrome = self.__state.browser
        model: Subject = self.__state.model

        if self.__import_final_exams:
            for final_exam in model.final_exams:
                for student, assignment_file in self.__download_assignment_files(final_exam.moodle_id):
                    student.add_final_exam_file(final_exam, assignment_file)

    def __download_assignment_files(self, moodle_id):
        browser: Chrome = self.__state.browser
        model: Subject = self.__state.model

        browser.get(
            'https://vzdelavanie.uniza.sk/moodle3/mod/assign/view.php?id={0}&action=grading'.format(
                moodle_id
            )
        )

        while True:
            all_file_links = browser.find_elements_by_xpath('//div[contains(@id, "assign_files_tree")]//a[@target]')

            for file_link in all_file_links:
                email_element = file_link.find_element_by_xpath('./ancestor::tr//td[contains(@class, "email")]')
                student = model.get_student_by_email(email_element.text)
                file_href = file_link.get_attribute('href')
                file_content = browser.request('GET', file_href).content

                yield student, InMemoryFile(file_link.text, file_content)

            if not any(browser.find_elements_by_link_text("Ďalší")):
                break
            browser.find_element_by_link_text("Ďalší").click()
