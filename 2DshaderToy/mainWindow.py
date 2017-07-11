#!/usr/bin/env python

from WindowLayouts.SimpleOpenGWindowLayout import Ui_MainWindow


class MainWindow(Ui_MainWindow):
    """docstring for myWindow."""
    def __init__(self, window):
        Ui_MainWindow.__init__(self)
        self.setupUi(window)
        window.setWindowTitle("Shader Toy")
