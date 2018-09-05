class InMemoryFile:
    file_name: str
    data: bytes

    def __init__(self, file_name, data):
        self.file_name = file_name
        self.data = data
