import sys

from PyQt5.QtWidgets import QApplication
from lxml.etree import xmlfile

from vgrabber.importer import Importer
from vgrabber.qtgui.importselector import ImportSelectorDialog
from vgrabber.qtgui.login import LoginDialog
from vgrabber.qtgui.qtcallbacks import QtCallbacks
from vgrabber.serializer import SubjectSerializer

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
    with xmlfile(open('test/subjectinfo.xml', 'wb')) as xf:
        xf.write(SubjectSerializer(importer.model).serialize())
