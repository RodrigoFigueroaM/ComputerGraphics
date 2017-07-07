#!/usr/bin/env python
'''
GLStandardDrawingWindow
----------
**GLStandardDrawingWindow** creates a QGLWidget of my thinking of a
standard window to draw. it handles the minimumSizeHint,sizeHint, initializeGL,
and resizeGLstandard
attributes
----------
        * standard width = 550
        * standard height = 500
        * history a Stack to kep track of the objects drawn on it
        * black background
        * white foreground
'''
import sys
import math

from OpenGL.GL import *
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QOpenGLWidget


class GLStandardWindow3D(QOpenGLWidget):
    def __init__(self, parent = None):
        super(QOpenGLWidget, self).__init__(parent)
        self.width, self.height = 100.0, 100.0
        self.move(100, 100)
        self.fov = 90
        self.ratio = 0

    def minimumSizeHint(self):
        return QSize(self.width, self.height)

    def sizeHint(self):
        return QSize(self.width, self.height)

    def initializeGL(self):
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHTING)
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glFlush()

    def resizeGL(self, w, h):
        self.width, self.height = w,h
        glViewport(-w, -h, w, h)
        # glMatrixMode(GL_PROJECTION)
        self.ratio = w // h
        # glMatrixMode(GL_MODELVIEW)
        # glLoadIdentity()

    @staticmethod
    def printOpenGLSettings():
        # print("OPENGL EXTENSIONS", glGetString(GL_EXTENSIONS))
        print("OPENGL VERSION", glGetString(GL_VERSION))
        print("OPENGL VENDOR", glGetString(GL_VENDOR))
        print("OPENGL RENDERER", glGetString(GL_RENDERER))
        print("OPENGL GLSL VERSION", glGetString(GL_SHADING_LANGUAGE_VERSION))
