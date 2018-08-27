import datetime

from seleniumrequests import Chrome

from ..importaction import ImportAction
from vgrabber.model import Subject, Student, Grade, StudentGrade
from .actionexecutor import ActionExecutor


class StudentInfoActionExecutor(ActionExecutor):
    def __init__(self, state):
        super().__init__(state)
        self.__state = state

    def exec(self):
        browser: Chrome = self.__state.browser
        model: Subject = self.__state.model

        import_list = bool(self.__state.requested_actions & {ImportAction.student_list})
        import_grades = bool(self.__state.requested_actions & {ImportAction.grades})

        browser.find_element_by_link_text('Zabezpečované predmety').click()
        tag = browser.find_element_by_xpath(
            "//tr[starts-with(.//a/text(), {0!r})]//a[starts-with(@href, 'znpredmet')]".format(model.number)
        )
        tag.click()

        if import_list:
            model.clear_students()
            for row in browser.find_elements_by_xpath('//table[@class="data"]//tr[not(./th)]'):
                surname, name = row.find_element_by_xpath('.//td[2]//b').text.lstrip('*+-').split(None, 1)
                group = row.find_element_by_xpath('.//td[1]').text
                number = row.find_element_by_xpath('.//td[3]').text

                model.add_student(Student(number, name, surname, group))

        if import_grades:
            students = {student.number: student for student in model.students}

            for student in model.students:
                student.clear_grades()

            for final_exam in model.final_exams:
                participants_data = browser.request(
                    'GET',
                    'https://vzdelavanie.uniza.sk/vzdelavanie/znpredmet.php?act=term&trm={0}'.format(final_exam.id)
                ).json()

                if 'pole' not in participants_data:
                    continue

                for participant in participants_data['pole']:
                    student = students[participant[0]]

                    for idx in (7, 9, 11):
                        if participant[idx]:
                            parsed_date = datetime.datetime.strptime(participant[idx], "%d.%m.%Y").date()
                            if parsed_date == final_exam.date_time.date():
                                student.add_grade(StudentGrade(final_exam, Grade[participant[idx + 1]]))
                                break
                    else:
                        student.add_grade(StudentGrade(final_exam, Grade.FX))
