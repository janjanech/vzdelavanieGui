from lxml.etree import Element

from vgrabber.model import Test


class TestSerializer:
    __test: Test

    def __init__(self, test):
        self.__test = test

    def serialize(self):
        test_element = Element(
            'test',
            id=str(self.__test.id),
            name=self.__test.name,
            moodleid=str(self.__test.moodle_id)
        )

        return test_element
