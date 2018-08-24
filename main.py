import sys

from PyQt5.QtWidgets import QApplication

from vgrabber.qtgui.importselector import ImportSelectorDialog
from vgrabber.qtgui.login import LoginDialog

app = QApplication(sys.argv)

login = LoginDialog()
print(login.exec())

import_ = ImportSelectorDialog()
print(import_.exec())
