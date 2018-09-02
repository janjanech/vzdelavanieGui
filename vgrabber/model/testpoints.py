import os.path

from .files import FileList
from .test import Test


class TestPoints:
    test: Test
    points: float
    files: FileList

    def __init__(self, test, points):
        self.test = test
        self.points = points
        self.files = FileList()

    def clear_files(self):
        self.files.clear()

    def save(self, directory):
        self.files.save(
            os.path.join(
                directory,
                'tests',
                str(self.test.id)
            )
        )
