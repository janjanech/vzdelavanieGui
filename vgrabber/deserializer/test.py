from vgrabber.model import Test


class TestDeserializer:
    def __init__(self, test_element):
        self.__test_element = test_element

    def deserialize(self):
        test = Test(
            int(self.__test_element.attrib['id']),
            self.__test_element.attrib['name'],
            int(self.__test_element.attrib['moodleid'])
        )

        return test
