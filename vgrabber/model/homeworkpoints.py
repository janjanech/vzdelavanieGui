import os.path

from .files import FileList


class HomeWorkPoints:
    def __init__(self, home_work, points):
        self.home_work = home_work
        self.points = points
        self.files = FileList()

    def save(self, directory):
        self.files.save(
            os.path.join(
                directory,
                'homeworks',
                str(self.home_work.id)
            )
        )
