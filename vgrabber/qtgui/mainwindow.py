from os.path import dirname
from traceback import format_exc, print_exc

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QMenuBar, QTabWidget, QApplication, QFileDialog, QMessageBox

from vgrabber.datalayer.fileaccessors import DirectoryFileAccessor
from .guimodel import GuiModel
from .tabs import StudentsTab, TeachersTab, HomeWorksTab, TestsTab, FinalExamsTab

try:
    from vgrabber.importer import Importer
    from vgrabber.qtgui.importing import LoginDialog, ImportSelectorDialog, QtCallbacks

    ALLOW_IMPORT = True
except ImportError:
    print_exc()
    ALLOW_IMPORT = False


class MainWindow:
    def __init__(self):
        self.model = GuiModel()
        self.__tabs = []  # keeps references to tab instances

        self.__window = QMainWindow()
        self.__set_title()
        self.__window.setMinimumSize(600, 600)
        self.__build_menu()
        self.__build_tabs()

        self.model.subject_changed.connect(self.__subject_changed)

    def __build_menu(self):
        menu_bar = QMenuBar()
        file_menu = menu_bar.addMenu("File")
        self.__import_action = file_menu.addAction("Import...")
        self.__import_action.triggered.connect(self.__import_clicked)
        self.__import_action.setEnabled(ALLOW_IMPORT)
        file_menu.addSeparator()
        self.__open_action = file_menu.addAction("Open...")
        self.__open_action.triggered.connect(self.__open_clicked)
        self.__save_action = file_menu.addAction("Save")
        self.__save_action.triggered.connect(self.__save_clicked)
        self.__save_action.setEnabled(False)
        self.__save_as_action = file_menu.addAction("Save as...")
        self.__save_as_action.triggered.connect(self.__save_as_clicked)
        self.__save_as_action.setEnabled(False)
        self.__close_action = file_menu.addAction("Close")
        self.__close_action.triggered.connect(self.__close_clicked)
        self.__close_action.setEnabled(False)
        file_menu.addSeparator()
        self.__exit_action = file_menu.addAction("Exit")
        self.__exit_action.triggered.connect(self.__exit_clicked)
        self.__window.setMenuBar(menu_bar)

    def __build_tabs(self):
        def add_tab(tab_class, label):
            tab = tab_class(self.model)
            self.__tabs.append(tab)
            self.__tabWidget.addTab(tab.widget, label)

        self.__tabWidget = QTabWidget()
        self.__tabWidget.setEnabled(False)

        add_tab(StudentsTab, "Students")
        add_tab(TeachersTab, "Teachers")
        add_tab(HomeWorksTab, "Home works")
        add_tab(TestsTab, "Tests")
        add_tab(FinalExamsTab, "Final exams")

        self.__window.setCentralWidget(self.__tabWidget)

    def __subject_changed(self):
        self.__set_title()

        has_model = self.model.subject is not None
        self.__save_action.setEnabled(has_model and self.model.data_layer.can_save)
        self.__save_as_action.setEnabled(has_model)
        self.__close_action.setEnabled(has_model)
        self.__tabWidget.setEnabled(has_model)

    def __set_title(self):
        if self.model.subject is None:
            self.__window.setWindowTitle("Vzdelavanie GUI")
        else:
            self.__window.setWindowTitle("Vzdelavanie GUI ({0} {1} {2})".format(
                self.model.subject.number,
                self.model.subject.name,
                self.model.subject.year
            ))

    def __import_clicked(self, *args):
        login_dlg = LoginDialog()
        login, password = login_dlg.exec()

        if login is None:
            return

        if self.model.subject is not None:
            finished_actions = self.model.subject.progress
        else:
            finished_actions = []

        import_dlg = ImportSelectorDialog(finished_actions)
        actions = import_dlg.exec()
        if actions is None:
            return

        with Importer(login, password, actions, QtCallbacks(), self.model.subject) as importer:
            importer.exec()
            self.model.use_subject(importer.model)

    def __open_clicked(self, *args):
        file_name, filter = QFileDialog.getOpenFileName(
            self.__window,
            caption="Open Data",
            filter="Imported data (subjectinfo.xml)"
        )

        if file_name:
            try:
                self.model.load(DirectoryFileAccessor(dirname(file_name)))
            except Exception:
                print_exc()
                exc = format_exc()
                message_box = QMessageBox(self.__window)
                message_box.setWindowModality(Qt.WindowModal)
                message_box.setIcon(QMessageBox.Critical)
                message_box.setWindowTitle("Error deserializing")
                message_box.setText(exc)
                message_box.exec()

    def __save_clicked(self, *args):
        self.model.save()

    def __save_as_clicked(self, *args):
        file_name, filter = QFileDialog.getSaveFileName(
            self.__window,
            caption="Save Data",
            filter="Imported data (subjectinfo.xml)"
        )

        if file_name:
            self.model.save_as(DirectoryFileAccessor(dirname(file_name)))

    def __close_clicked(self, *args):
        self.model.use_subject(None)

    def __exit_clicked(self, *args):
        QApplication.exit(0)

    def show(self):
        self.__window.showMaximized()
