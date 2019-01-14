import os.path


class ExternalFile:
    file_name: str
    file_path: str

    def __init__(self, file_path):
        self.file_name = os.path.basename(file_path)
        self.file_path = file_path
