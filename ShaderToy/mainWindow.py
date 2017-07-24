#!/usr/bin/env python

from WindowLayouts.ShaderWindowLayout import Ui_MainWindow

class MainWindow(Ui_MainWindow):
    """docstring for myWindow."""
    def __init__(self, window):
        Ui_MainWindow.__init__(self)
        self.setupUi(window)
        window.setWindowTitle("Shader Toy")

        self.compileBtn.clicked.connect(self.compileCode)

    def compileCode(self):
        vertexCode = self.VertexCode.toPlainText()
        fragmentCode = self.FragementCode.toPlainText()
        self.logTextBox.clear()
        self.logTextBox.appendPlainText(str(self.openGLWidget.program.changeVertexAndFragmentFromSourceCode(vertexCode, fragmentCode)))
