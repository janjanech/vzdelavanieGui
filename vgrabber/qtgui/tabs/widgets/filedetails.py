from PyQt5.QtWidgets import QTextEdit

from vgrabber.model.files import InMemoryFile, StoredFile
from vgrabber.qtgui.guimodel import GuiModel
from vgrabber.qtgui.tabs.items import FileItem


class FileDetailsWidget:
    model: GuiModel

    def __init__(self, model):
        super().__init__()

        self.model = model

        self.widget = QTextEdit()
        self.widget.setReadOnly(True)
        self.widget.setVisible(False)

    def master_selection_changed(self, selected_items):
        if not selected_items:
            self.widget.setVisible(False)
            return

        selected_item = selected_items[0]

        if not isinstance(selected_item, FileItem):
            self.widget.setVisible(False)
            return

        file = selected_item.file

        if file.file_name.endswith('.txt'):
            self.widget.setText(self.__get_string(file))
            self.widget.setVisible(True)
        elif file.file_name.endswith(('.html', '.htm')):
            self.widget.setHtml(self.__get_string(file))
            self.widget.setVisible(True)
        else:
            self.widget.setVisible(False)

    def __get_string(self, file):
        if isinstance(file, InMemoryFile):
            return file.data.decode('utf8')
        elif isinstance(file, StoredFile):
            with self.model.data_layer.file_accessor.open_file(file.file_path, 'r') as f:
                return f.read().decode('utf8')
        else:
            return ''
