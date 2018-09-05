import os.path

from vgrabber.utilities.filename import correct_file_name
from .stored import StoredFile


class InMemoryFile:
    def __init__(self, file_name, data):
        self.file_name = file_name
        self.__data = data

    def save(self, old_file_accessor_root, file_accessor):
        file_accessor.ensure_exists()

        file_name = correct_file_name(self.file_name)

        with file_accessor.open_file(file_name, 'w') as f:
            f.write(self.__data)

        return StoredFile(self.file_name, file_accessor.get_relative_path(file_name))
