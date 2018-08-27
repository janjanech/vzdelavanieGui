from PyQt5.QtWidgets import QDialog, QVBoxLayout, QDialogButtonBox, QCheckBox

from vgrabber.importer import ImportAction


class ImportSelectorDialog:
    def __init__(self, finished_actions):
        self.__finished_actions = set(finished_actions)
        self.__possibilities = {}

        self.__dialog = QDialog()
        self.__dialog.setWindowTitle("Import")

        layout = QVBoxLayout()

        for action in ImportAction:
            check = QCheckBox()
            if action in self.__finished_actions:
                check.setText("{0} (finished)".format(action.name))
                check.setStyleSheet('QCheckBox { font-style: italic }')
            else:
                check.setText(action.name)
            self.__possibilities[action] = check
            check.toggled.connect(lambda *args: self.__refresh())
            layout.addWidget(check)

        for default_action in ImportAction.default:
            self.__possibilities[default_action].setChecked(True)

        self.__button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.__button_box.accepted.connect(self.__dialog.accept)
        self.__button_box.rejected.connect(self.__dialog.reject)
        layout.addWidget(self.__button_box)

        self.__refresh()

        self.__dialog.setLayout(layout)

    def __refresh(self):
        checked = self.__get_checked()

        for action, check in self.__possibilities.items():
            check.setEnabled(not action.depends - checked)

        self.__button_box.button(QDialogButtonBox.Ok).setEnabled(bool(self.__get_trully_checked()))

    def __get_checked(self):
        checked = {action
                   for action, check in self.__possibilities.items()
                   if check.isChecked() or action in self.__finished_actions}
        old_checked_cnt = len(checked)
        new_checked_cnt = -1
        while old_checked_cnt != new_checked_cnt:
            old_checked_cnt = new_checked_cnt
            checked = {action for action in checked if not (action.depends - checked)}
            new_checked_cnt = len(checked)
        return checked

    def __get_trully_checked(self):
        checked = self.__get_checked()
        return {action for action, check in self.__possibilities.items() if action in checked and check.isChecked()}

    def exec(self):
        if self.__dialog.exec() != QDialog.Accepted:
            return None

        return self.__get_trully_checked()
