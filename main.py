import sys

from PyQt5.QtWidgets import QApplication, QMessageBox

from vgrabber.importer import Importer
from vgrabber.qtgui.importselector import ImportSelectorDialog
from vgrabber.qtgui.login import LoginDialog
from vgrabber.qtgui.qtcallbacks import QtCallbacks

app = QApplication(sys.argv)

login_dlg = LoginDialog()
login, password = login_dlg.exec()

if login is None:
    sys.exit(0)

import_dlg = ImportSelectorDialog()
actions = import_dlg.exec()
if actions is None:
    sys.exit(0)

with Importer(login, password, actions, QtCallbacks()) as importer:
    importer.exec()
    dlg = QMessageBox()
    dlg.setText("Done")
    dlg.exec()
