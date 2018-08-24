from PyQt5.QtWidgets import QDialog, QVBoxLayout, QDialogButtonBox, QCheckBox

from vgrabber.importer import ImportAction


class ImportSelectorDialog:
    def __init__(self):
        self.__possibilities = {}

        self.__dialog = QDialog()
        self.__dialog.setWindowTitle("Import")

        layout = QVBoxLayout()

        for action in ImportAction:
            check = QCheckBox()
            check.setText(action.name)
            self.__possibilities[action] = check
            check.toggled.connect(lambda *args: self.__refresh())
            layout.addWidget(check)

        for default_action in ImportAction.default:
            self.__possibilities[default_action].setChecked(True)

        self.__refresh()

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.__dialog.accept)
        button_box.rejected.connect(self.__dialog.reject)
        layout.addWidget(button_box)

        self.__dialog.setLayout(layout)

    def __refresh(self):
        for action, check in self.__possibilities.items():
            enabled = True
            for dep in action.depends:
                if not self.__possibilities[dep].isChecked():
                    enabled = False
            check.setEnabled(enabled)

    def exec(self):
        if self.__dialog.exec() != QDialog.Accepted:
            return None
        while not any(check.isChecked() for check in self.__possibilities.values()):
            if self.__dialog.exec() != QDialog.Accepted:
                return None

        return {action for action, check in self.__possibilities.items() if check.isChecked() and check.isEnabled()}
