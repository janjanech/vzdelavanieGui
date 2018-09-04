from vgrabber.model import Test


class TestDeserializer:
    def __init__(self, subject, test_element):
        self.__subject = subject
        self.__test_element = test_element

    def deserialize(self):
        test = Test(
            self.__subject,
            int(self.__test_element.attrib['id']),
            self.__test_element.attrib['name'],
            int(self.__test_element.attrib['moodleid'])
        )

        return test
