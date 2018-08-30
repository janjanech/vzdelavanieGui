import os.path

from .files import InMemoryFile


class HomeWorkPoints:
    def __init__(self, home_work, points):
        self.home_work = home_work
        self.points = points
        self.file = None

    def save(self, directory):
        if isinstance(self.file, InMemoryFile):
            self.file = self.file.save(
                os.path.join(
                    directory,
                    'homeworks',
                    str(self.home_work.id)
                )
            )
