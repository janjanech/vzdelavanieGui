import os.path
from typing import BinaryIO

from .fileaccessor import FileAccessor


class DirectoryFileAccessor(FileAccessor):
    def __init__(self, path: str):
        self.__path = path
        self.__intern_path = None

    def ensure_exists(self):
        if not os.path.exists(self.__path):
            os.makedirs(self.__path)

    def open_file(self, name: str, mode: str) -> BinaryIO:
        ret: BinaryIO = open(os.path.join(self.__path, name.replace('/', os.path.sep)), mode + 'b')
        return ret

    def open_file_for_external_app(self, rel_path: str) -> str:
        return os.path.abspath(os.path.join(self.__path, rel_path.replace('/', os.path.sep)))

    def open_folder(self, *names: str) -> 'FileAccessor':
        ret = DirectoryFileAccessor(os.path.join(self.__path, *names))
        ret.__intern_path = self.get_relative_path(*names)
        return ret

    def get_relative_path(self, *names: str) -> str:
        if self.__intern_path is None:
            return '/'.join(names)
        else:
            return '/'.join([self.__intern_path, *names])
