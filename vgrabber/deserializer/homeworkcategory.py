from vgrabber.model import HomeWorkCategory, HomeWork


class HomeWorkCategoryDeserializer:
    def __init__(self, category_element):
        self.__category_element = category_element

    def deserialize(self):
        home_work_category = HomeWorkCategory(
            self.__category_element.attrib['name']
        )

        for homework_element in self.__category_element.xpath('./homework'):
            homework = HomeWork(
                int(homework_element.attrib['id']),
                homework_element.attrib['name'],
                int(homework_element.attrib['moodleid'])
            )

            home_work_category.add_home_work(homework)

        return home_work_category
