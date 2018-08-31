from .inmemory import InMemoryFile


class FileList:
    def __init__(self):
        self.files = []

    def __iter__(self):
        return iter(self.files)

    def clear(self):
        self.files.clear()

    def add_file(self, file):
        self.files.append(file)

    def save(self, directory):
        new_files = []

        for file in self.files:
            if isinstance(file, InMemoryFile):
                new_files.append(file.save(directory))
            else:
                new_files.append(file)

        self.files = new_files
