from shutil import copyfileobj

from vgrabber.utilities.filename import correct_file_name


class StoredFile:
    def __init__(self, file_name, file_path):
        self.file_name = file_name
        self.file_path = file_path

    def save(self, old_file_accessor_root, file_accessor):
        if old_file_accessor_root is None:
            return self

        file_accessor.ensure_exists()

        file_name = correct_file_name(self.file_name)

        with old_file_accessor_root.open_file(self.file_path, 'r') as old_file:
            with file_accessor.open_file(file_name, 'w') as new_file:
                copyfileobj(old_file, new_file)

        return StoredFile(self.file_name, file_accessor.get_relative_path(file_name))
