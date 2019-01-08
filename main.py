#!/usr/bin/env python3
import sys

from PyQt5.QtWidgets import QApplication

from vgrabber.qtgui.guimodel import GuiModel
from vgrabber.qtgui.mainwindow import MainWindow

app = QApplication(sys.argv)

app.setOrganizationName("Jan Janech")
app.setApplicationName("vzdelavanieGui")

model = GuiModel()

main_window = MainWindow(model)
main_window.show()

ret = app.exec()

model.quit()

sys.exit(ret)
