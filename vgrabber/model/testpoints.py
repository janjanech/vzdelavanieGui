import os.path

from .files import FileList
from .test import Test


class TestPoints:
    test: Test
    points: float
    files: FileList

    def __init__(self, subject, student, test, points):
        self.__subject = subject
        self.test = test
        self.points = points
        self.files = FileList()

        self.student = student

    def clear_files(self):
        self.files.clear()

    def save(self, old_file_accessor_root, file_accessor):
        self.files.save(
            old_file_accessor_root,
            file_accessor.open_folder(
                'tests',
                str(self.test.id)
            )
        )
