from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QWidget, QDialogButtonBox, QVBoxLayout


class LoginDialog:
    def __init__(self):
        form_layout = QFormLayout()

        self.__login = QLineEdit()
        form_layout.addRow("Login", self.__login)
        self.__login.textChanged.connect(lambda *args: self.__refresh())
        self.__password = QLineEdit()
        self.__password.setEchoMode(QLineEdit.Password)
        form_layout.addRow("Password", self.__password)

        self.__dialog = QDialog()
        self.__dialog.setWindowTitle("LogIn to Vzdelavanie:")

        layout = QVBoxLayout()
        layout.addLayout(form_layout)
        self.__button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.__button_box.accepted.connect(self.__dialog.accept)
        self.__button_box.rejected.connect(self.__dialog.reject)
        layout.addWidget(self.__button_box)

        self.__refresh()

        self.__dialog.setLayout(layout)

    def __refresh(self):
        self.__button_box.button(QDialogButtonBox.Ok).setEnabled(self.__login.text().strip() != '')

    def exec(self):
        if self.__dialog.exec() != QDialog.Accepted:
            return None, None

        return self.__login.text().strip(), self.__password.text().strip()
