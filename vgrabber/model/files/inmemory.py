import os.path

from vgrabber.utilities.filename import correct_file_name
from .stored import StoredFile


class InMemoryFile:
    def __init__(self, file_name, data):
        self.file_name = file_name
        self.__data = data

    def save(self, directory):
        file_path = os.path.join(directory, correct_file_name(self.file_name))

        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(file_path, 'wb') as f:
            f.write(self.__data)

        return StoredFile(self.file_name, file_path)
