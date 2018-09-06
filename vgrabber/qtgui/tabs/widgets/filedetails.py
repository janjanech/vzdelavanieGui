import zipfile
from io import BytesIO

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
        elif file.file_name.endswith('.zip'):
            self.widget.setHtml(self.__format_zip_content(file))
            self.widget.setVisible(True)
        else:
            self.widget.setVisible(False)

    def __format_zip_content(self, file):
        def format_recursive(cur: dict):
            ret = []
            for name, content in sorted(cur.items()):
                if content:
                    ret.append(f"<li>{name}{format_recursive(content)}</li>")
                else:
                    ret.append(f"<li>{name}</li>")
            return f"<ul>{''.join(ret)}</ul>"

        return format_recursive(self.__get_zip_content(file))

    def __get_zip_content(self, file):
        with zipfile.ZipFile(BytesIO(self.__get_data(file))) as f:
            ret = {}
            for path in f.namelist():
                cur = ret
                for component in path.split('/'):
                    cur = cur.setdefault(component, {})
            return ret

    def __get_string(self, file):
        return self.__get_data(file).decode('utf8')

    def __get_data(self, file):
        if isinstance(file, InMemoryFile):
            return file.data
        elif isinstance(file, StoredFile):
            with self.model.data_layer.file_accessor.open_file(file.file_path, 'r') as f:
                return f.read()
        else:
            return b''
