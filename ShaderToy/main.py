#! /usr/bin/env python
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QSurfaceFormat
from mainWindow import *

if __name__ == "__main__":
    glFormat = QSurfaceFormat()
    glFormat.setVersion(3,3)
    glFormat.setProfile(QSurfaceFormat.CoreProfile)
    QSurfaceFormat.setDefaultFormat(glFormat)
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QDialog()
    window = QtWidgets.QMainWindow()
    ui = MainWindow(window)
    window.show()
    sys.exit(app.exec_())

