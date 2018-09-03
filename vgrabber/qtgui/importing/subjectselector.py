from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QListWidget, QDialogButtonBox


class SubjectSelectorDialog:
    def __init__(self, subjects):
        self.__subjects = subjects

        self.__dialog = QDialog()
        self.__dialog.setWindowTitle("Select subject")

        layout = QVBoxLayout()

        self.__list_widget = QListWidget()
        layout.addWidget(self.__list_widget)

        for subject in subjects:
            self.__list_widget.addItem("{0} {1}".format(subject.number, subject.name))

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.__dialog.accept)
        button_box.rejected.connect(self.__dialog.reject)
        layout.addWidget(button_box)

        self.__dialog.setLayout(layout)

    def exec(self):
        while self.__list_widget.currentItem() is None:
            if self.__dialog.exec() != QDialog.Accepted:
                return None

        text = self.__list_widget.currentItem().text()

        for subject in self.__subjects:
            if text.startswith(subject.number):
                return subject

        raise Exception("WTF?")
