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

    def save(self, old_file_accessor_root, file_accessor):
        new_files = []

        for file in self.files:
            new_files.append(file.save(old_file_accessor_root, file_accessor))

        self.files = new_files
