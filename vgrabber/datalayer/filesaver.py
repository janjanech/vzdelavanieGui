from shutil import copyfileobj
from typing import Optional

from vgrabber.model import Subject, Student, StudentGrade, HomeWorkPoints, TestPoints
from vgrabber.model.files import FileList, InMemoryFile, StoredFile
from vgrabber.utilities.filename import correct_file_name
from .fileaccessors import FileAccessor


class FileSaver:
    def __init__(self, old_file_accessor: Optional[FileAccessor], file_accessor: FileAccessor):
        self.__old_file_accessor_root = old_file_accessor
        self.__file_accessor_root = file_accessor

    def save_subject_files(self, subject: Subject):
        self.__save_subject_files(self.__file_accessor_root, subject)

    def __save_subject_files(self, file_accessor: FileAccessor, subject: Subject):
        for student in subject.students:
            self.__save_student_files(file_accessor, student)

    def __save_student_files(self, file_accessor: FileAccessor, student: Student):
        student_dir = file_accessor.open_folder(
            correct_file_name(
                '{0}_{1}{2}'.format(student.number, student.surname, student.name)
            )
        )

        for grade in student.grades:
            self.__save_grade_files(student_dir, grade)

        for home_work_point in student.home_work_points:
            self.__save_home_work_files(student_dir, home_work_point)

        for test_points in student.test_points:
            self.__save_test_files(student_dir, test_points)

    def __save_grade_files(self, file_accessor: FileAccessor, grade: StudentGrade):
        self.__save_files(
            file_accessor.open_folder(
                'finalexams',
                '{0}_{1}'.format(grade.final_exam.id, grade.final_exam.date_time.isoformat())
            ),
            grade.files
        )

    def __save_home_work_files(self, file_accessor: FileAccessor, home_work_points: HomeWorkPoints):
        self.__save_files(
            file_accessor.open_folder(
                'homeworks',
                str(home_work_points.home_work.id)
            ),
            home_work_points.files
        )

    def __save_test_files(self, file_accessor: FileAccessor, test_points: TestPoints):
        self.__save_files(
            file_accessor.open_folder(
                'tests',
                str(test_points.test.id)
            ),
            test_points.files
        )

    def __save_files(self, file_accessor: FileAccessor, file_list: FileList):
        new_files = []

        for file in file_list:
            if isinstance(file, InMemoryFile):
                new_files.append(self.__save_in_memory_file(file_accessor, file))
            else:
                new_files.append(self.__save_stored_file(file_accessor, file))

        file_list.replace(new_files)

    def __save_in_memory_file(self, file_accessor: FileAccessor, file: InMemoryFile):
        file_accessor.ensure_exists()

        file_name = correct_file_name(file.file_name)

        with file_accessor.open_file(file_name, 'w') as f:
            f.write(file.data)

        return StoredFile(file.file_name, file_accessor.get_relative_path(file_name))

    def __save_stored_file(self, file_accessor: FileAccessor, file: StoredFile):
        if self.__old_file_accessor_root is None:
            return self

        file_accessor.ensure_exists()

        file_name = correct_file_name(file.file_name)

        with self.__old_file_accessor_root.open_file(file.file_path, 'r') as old_file:
            with file_accessor.open_file(file_name, 'w') as new_file:
                copyfileobj(old_file, new_file)

        return StoredFile(file.file_name, file_accessor.get_relative_path(file_name))
