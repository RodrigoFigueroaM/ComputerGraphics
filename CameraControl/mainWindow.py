#!/usr/bin/env python

from mainwindowLayout import Ui_MainWindow
from Scene import Scene


class MainWindow(Ui_MainWindow):
    """docstring for myWindow."""
    def __init__(self, window):
        Ui_MainWindow.__init__(self)
        self.setupUi(window)
        window.setWindowTitle("Camera control")
