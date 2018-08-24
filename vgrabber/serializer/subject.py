from lxml.etree import Element


class SubjectSerializer:
    def __init__(self, subject):
        self.__subject = subject

    def serialize(self):
        subject_element = Element(
            'subject',
            number=self.__subject.number,
            name=self.__subject.name,
            year=self.__subject.year
        )

        progress_element = Element('progress')

        for action in self.__subject.progress:
            action_element = Element('finished', action=action.name)
            progress_element.append(action_element)

        subject_element.append(progress_element)

        return subject_element
