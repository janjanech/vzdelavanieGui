import os.path

from .files import FileList
from .homework import HomeWork


class HomeWorkPoints:
    home_work: HomeWork
    points: float
    files: FileList

    def __init__(self, subject, student, home_work, points):
        self.__subject = subject
        self.home_work = home_work
        self.points = points
        self.files = FileList()

        self.student = student

    def clear_files(self):
        self.files.clear()

    def save(self, old_file_accessor_root, file_accessor):
        self.files.save(
            old_file_accessor_root,
            file_accessor.open_folder(
                'homeworks',
                str(self.home_work.id)
            )
        )
