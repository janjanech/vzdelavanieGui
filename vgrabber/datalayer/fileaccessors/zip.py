import os.path
from io import BytesIO
from shutil import copyfileobj, rmtree
from tempfile import mkdtemp
from typing import BinaryIO, Union, List, Iterable, T
from zipfile import ZipFile

from vgrabber.datalayer.fileaccessors import FileAccessor


class ZipFileWriter(BytesIO):
    def __init__(self, file: ZipFile, file_path: str):
        super().__init__()
        self.__file = file
        self.__file_path = file_path
        self.__closed = False

    def close(self):
        if not self.__closed:
            super().flush()
            self.__file.writestr(self.__file_path, self.getvalue())
            super().close()
            self.__closed = True


class ZipFileAccessorInfo:
    def __init__(self, file: str):
        self.file = ZipFile(file, 'a')
        self.common_prefix = self.__get_common_prefix()
        self.__temp_dirs = []

    def save_file(self, file_name, path):
        dir_name = mkdtemp()
        file_path = os.path.join(dir_name, file_name)

        if self.common_prefix:
            path = f"{self.common_prefix}/{path}"

        with open(file_path, 'wb') as new_file:
            with self.file.open(path, 'r') as old_file:
                copyfileobj(old_file, new_file)

        self.__temp_dirs.append(dir_name)

        return file_path

    def close(self):
        for dir_name in self.__temp_dirs:
            rmtree(dir_name, ignore_errors=True)

        self.file.close()

    def __get_common_prefix(self):
        return '/'.join(self.__common_list_prefix([x.split('/') for x in self.file.namelist()]))

    def __common_list_prefix(self, data: Iterable[Iterable[T]]) -> Iterable[T]:
        for components in zip(*data):
            if all(component == components[0] for component in components):
                yield components[0]
            else:
                return


class ZipFileAccessor(FileAccessor):
    def __init__(self, file: Union[str, ZipFileAccessorInfo]):
        if isinstance(file, str):
            self.__info = ZipFileAccessorInfo(file)
            self.__path = self.__info.common_prefix
        else:
            self.__info = file
            self.__path = None

    def ensure_exists(self):
        pass

    def open_file(self, name: str, mode: str) -> BinaryIO:
        if mode == 'r':
            return self.__info.file.open(self.get_relative_path(name))
        elif mode == 'w':
            return ZipFileWriter(self.__info.file, self.get_relative_path(name))

    def open_file_for_external_app(self, rel_path: str) -> str:
        name = rel_path.split('/')[-1]
        return self.__info.save_file(name, rel_path)

    def open_folder(self, *names: str) -> 'FileAccessor':
        ret = ZipFileAccessor(self.__info)
        ret.__path = self.get_relative_path(*names)
        return ret

    def get_relative_path(self, *names: str) -> str:
        if self.__path is None:
            return '/'.join(names)
        else:
            return '/'.join([self.__path, *names])

    def close(self):
        self.__info.close()
