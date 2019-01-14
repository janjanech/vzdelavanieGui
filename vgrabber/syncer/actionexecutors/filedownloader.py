from io import BytesIO

import lxml.html

from seleniumrequests import Chrome

from vgrabber.model.files import InMemoryFile
from vgrabber.base.importaction import ImportAction
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

    def exec(self):
        browser: Chrome = self.__state.browser
        model: Subject = self.__state.model

        if self.__import_final_exams:
            model.clear_final_exam_files()
            for final_exam in model.final_exams:
                for student, assignment_file in self.__download_assignment_files(final_exam.moodle_id):
                    student.add_final_exam_file(final_exam, assignment_file)

        if self.__import_home_works:
            model.clear_home_work_files()
            for home_work_category in model.home_work_categories:
                for home_work in home_work_category.home_works:
                    for student, assignment_file in self.__download_assignment_files(home_work.moodle_id):
                        student.add_home_work_file(home_work, assignment_file)

    def __download_assignment_files(self, moodle_id):
        browser: Chrome = self.__state.browser
        model: Subject = self.__state.model

        base_url = browser.find_element_by_link_text('Domov').get_attribute('href')

        browser.get(
            base_url + 'mod/assign/view.php?id={0}&action=grading'.format(
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

            all_online_text_links = browser.find_elements_by_xpath(
                '//a[contains(@href, "plugin=onlinetext")][following-sibling::div[@class="no-overflow"]]'
            )

            for online_text_link in all_online_text_links:
                email_element = online_text_link.find_element_by_xpath('./ancestor::tr//td[contains(@class, "email")]')
                student = model.get_student_by_email(email_element.text)
                file_href = online_text_link.get_attribute('href')
                file_content = browser.request('GET', file_href).content
                online_text_html = lxml.html.parse(BytesIO(file_content))
                online_text_element = online_text_html.xpath('//div[contains(@class, "submissionfull")]')
                if online_text_element:
                    html_element = lxml.html.Element('html')
                    body_element = lxml.html.Element('body')
                    html_element.append(body_element)
                    body_element.append(online_text_element[0])
                    serialized_text = lxml.html.tostring(html_element)
                    yield student, InMemoryFile('onlinetext.html', serialized_text)

            if not any(browser.find_elements_by_link_text("Ďalší")):
                break
            browser.find_element_by_link_text("Ďalší").click()
