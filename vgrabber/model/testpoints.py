import os.path

from .files import FileList


class TestPoints:
    def __init__(self, test, points):
        self.test = test
        self.points = points
        self.files = FileList()

    def save(self, directory):
        self.files.save(
            os.path.join(
                directory,
                'tests',
                str(self.test.id)
            )
        )
