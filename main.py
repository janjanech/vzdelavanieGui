import os.path
import sys
from traceback import print_exc

from PyQt5.QtWidgets import QApplication
from lxml.etree import xmlfile, parse

from vgrabber.deserializer import SubjectDeserializer
from vgrabber.importer import Importer
from vgrabber.qtgui.importselector import ImportSelectorDialog
from vgrabber.qtgui.login import LoginDialog
from vgrabber.qtgui.qtcallbacks import QtCallbacks
from vgrabber.serializer import SubjectSerializer

app = QApplication(sys.argv)

try:
    with open('test/subjectinfo.xml', 'rb') as xf:
        model = SubjectDeserializer(parse(xf).getroot()).deserialize()
except:
    print_exc()
    model = None

login_dlg = LoginDialog()
login, password = login_dlg.exec()

if login is None:
    sys.exit(0)

if model is not None:
    finished_actions = model.progress
else:
    finished_actions = []

import_dlg = ImportSelectorDialog(finished_actions)
actions = import_dlg.exec()
if actions is None:
    sys.exit(0)

with Importer(login, password, actions, QtCallbacks(), model) as importer:
    importer.exec()

    importer.model.save('test')

    with xmlfile(open('test/subjectinfo.xml', 'wb'), encoding='utf-8') as xf:
        xf.write_declaration()
        xf.write(
            SubjectSerializer(importer.model).serialize(),
            pretty_print=True
        )
