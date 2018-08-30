import os.path

from .files import InMemoryFile


class TestPoints:
    def __init__(self, test, points):
        self.test = test
        self.points = points
        self.file = None

    def save(self, directory):
        if isinstance(self.file, InMemoryFile):
            self.file = self.file.save(
                os.path.join(
                    directory,
                    'tests',
                    str(self.test.id)
                )
            )
