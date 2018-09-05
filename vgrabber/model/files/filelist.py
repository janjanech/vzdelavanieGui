class FileList:
    def __init__(self):
        self.files = []

    def __iter__(self):
        return iter(self.files)

    def clear(self):
        self.files.clear()

    def add_file(self, file):
        self.files.append(file)

    def replace(self, new_files):
        self.files = list(new_files)
