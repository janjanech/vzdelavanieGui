from lxml.etree import Element

from vgrabber.model import HomeWorkCategory


class HomeWorkCategorySerializer:
    __home_work_category: HomeWorkCategory

    def __init__(self, home_work_category):
        self.__home_work_category = home_work_category

    def serialize(self):
        category_element = Element(
            'category',
            name=self.__home_work_category.name
        )
        if self.__home_work_category.max_points is not None:
            category_element.attrib['maxpoints'] = str(self.__home_work_category.max_points)

        for home_work in self.__home_work_category.home_works:
            home_work_element = Element(
                'homework',
                id = str(home_work.id),
                name = home_work.name,
                moodleid = str(home_work.moodle_id)
            )
            category_element.append(home_work_element)

        return category_element
