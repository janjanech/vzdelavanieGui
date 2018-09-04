import os.path

from .files import FileList
from .homework import HomeWork


class HomeWorkPoints:
    home_work: HomeWork
    points: float
    files: FileList

    def __init__(self, subject, home_work, points):
        self.__subject = subject
        self.home_work = home_work
        self.points = points
        self.files = FileList()

    def clear_files(self):
        self.files.clear()

    def save(self, directory):
        self.files.save(
            os.path.join(
                directory,
                'homeworks',
                str(self.home_work.id)
            )
        )
