from typing import Optional

from lxml.etree import parse, xmlfile

from vgrabber.datalayer.filesaver import FileSaver
from vgrabber.model import Subject
from .deserializer import SubjectDeserializer
from .fileaccessors import FileAccessor
from .serializer import SubjectSerializer


class DataLayer:
    file_accessor: Optional[FileAccessor]

    SUBJECT_INFO_NAME = 'subjectinfo.xml'

    def __init__(self):
        self.file_accessor = None

    def load(self, file_accessor: FileAccessor) -> Subject:
        self.file_accessor = file_accessor
        with self.file_accessor.open_file(self.SUBJECT_INFO_NAME, 'r') as xf:
            return SubjectDeserializer(parse(xf).getroot()).deserialize()

    @property
    def can_save(self):
        return self.file_accessor is not None

    def save(self, subject: Subject):
        FileSaver(None, self.file_accessor).save_subject_files(subject)

        self.__save(subject)

    def save_as(self, file_accessor: FileAccessor, subject: Subject):
        old_file_accessor = self.file_accessor
        self.file_accessor = file_accessor

        FileSaver(old_file_accessor, self.file_accessor).save_subject_files(subject)

        self.__save(subject)

    def __save(self, subject: Subject):
        root_element = SubjectSerializer(subject).serialize()

        with self.file_accessor.open_file(self.SUBJECT_INFO_NAME, 'w') as f:
            with xmlfile(f, encoding='utf-8') as xf:
                xf.write_declaration()
                xf.write(
                    root_element,
                    pretty_print=True
                )

    def open_file_for_external_app(self, rel_path: str) -> str:
        return self.file_accessor.open_file_for_external_app(rel_path)

    def close(self):
        self.file_accessor = None
