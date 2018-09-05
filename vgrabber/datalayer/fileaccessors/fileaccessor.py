from abc import ABC, abstractmethod
from typing import BinaryIO


class FileAccessor(ABC):
    @abstractmethod
    def ensure_exists(self):
        pass

    @abstractmethod
    def open_file(self, name: str, mode: str) -> BinaryIO:
        pass

    @abstractmethod
    def open_file_for_external_app(self, rel_path: str) -> str:
        pass

    @abstractmethod
    def open_folder(self, *names: str) -> 'FileAccessor':
        pass

    @abstractmethod
    def get_relative_path(self, name: str) -> str:
        pass
