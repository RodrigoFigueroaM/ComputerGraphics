#!/usr/bin/env python

from PyQt5.QtGui import QMatrix4x4, QVector3D
from PyQt5.Qt import Qt
from PyQt5.QtGui import (QOpenGLShader, QOpenGLShaderProgram)
from GLStandardWindow3D import GLStandardWindow3D
from Camera import Camera
from TrackBall import TrackBall
from OpenGL.GL import *


class DrawingWindow(GLStandardWindow3D):
    vertexShaderSource = """
    uniform highp mat4 projectionMatrix;
    uniform highp mat4 modelViewMatrix;
    uniform highp mat4 normalMatrix;
    
  
    attribute highp vec4 pos;
    attribute lowp vec4 col;
    
    varying lowp vec4 color;
    
    void main() 
    {
       color = col;
       gl_Position = projectionMatrix * modelViewMatrix * pos;
    }"""

    fragmentShaderSource = """
    uniform highp mat4 projectionMatrix;
    uniform highp mat4 modelViewMatrix;
    uniform highp mat4 normalMatrix; 

    varying lowp vec4 color;
    void main() {
       gl_FragColor = color;
    }"""

    vtr = [
        -1.0, -1.0, -1.0, #// triangle 1 : begin
        -1.0, -1.0, 1.0,
        -1.0, 1.0, 1.0, #// triangle 1 : end
        1.0, 1.0, -1.0,  # // triangle 2 : begin
        -1.0, -1.0, -1.0,
        -1.0, 1.0, -1.0,  #// triangle 2 : end
        1.0, -1.0, 1.0,
        -1.0, -1.0, -1.0,
        1.0, -1.0, -1.0,
        1.0, 1.0, -1.0,
        1.0, -1.0, -1.0,
        -1.0, -1.0, -1.0,
        -1.0, -1.0, -1.0,
        -1.0, 1.0, 1.0,
        -1.0, 1.0, -1.0,
        1.0, -1.0, 1.0,
        -1.0, -1.0, 1.0,
        -1.0, -1.0, -1.0,
        -1.0, 1.0, 1.0,
        -1.0, -1.0, 1.0,
        1.0, -1.0, 1.0,
        1.0, 1.0, 1.0,
        1.0, -1.0, -1.0,
        1.0, 1.0, -1.0,
        1.0, -1.0, -1.0,
        1.0, 1.0, 1.0,
        1.0, -1.0, 1.0,
        1.0, 1.0, 1.0,
        1.0, 1.0, -1.0,
        -1.0, 1.0, -1.0,
        1.0, 1.0, 1.0,
        -1.0, 1.0, -1.0,
        -1.0, 1.0, 1.0,
        1.0, 1.0, 1.0,
        -1.0, 1.0, 1.0,
        1.0, -1.0, 1.0]

    vertices = [float(value) for value in vtr]
    colors = [float(value) for value in vtr]

    def __init__(self):
        super(DrawingWindow, self).__init__()
        self.program = QOpenGLShaderProgram(self)
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.StrongFocus)
        self._camera = Camera(position = QVector3D(0, 0, 5),
                              direction = QVector3D(0, 0, 0),
                              up = QVector3D(0, 1, 0))
        self.trackBall = TrackBall()
        self.pressClick = QVector3D()
        self.releaseClick = QVector3D()
        self.rotation = QMatrix4x4()
        self.normalMatrix = QMatrix4x4()
        self.posAttr = 0
        self.colAttr = 0

    def initializeGL(self):
        self.printOpenGLSettings()
        glClearColor(0.2, 0.2, 0.2, 1.0)
        glEnable(GL_DEPTH_TEST)
        self.program.addShaderFromSourceCode(QOpenGLShader.Vertex, self.vertexShaderSource)
        self.program.addShaderFromSourceCode(QOpenGLShader.Fragment, self.fragmentShaderSource)
        self.program.link()

    def paintGL(self):
        self.ratio = self.width / self.height
        self.camera.setPerspective(self.fov, self.ratio, 1.0, 100.0)

        self.camera.lookAtCenter()
        self.camera.position = self.rotation * self.camera.position

        self.normalMatrix = self.camera.modelViewMatrix.inverted()[0].transposed()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glViewport(0, 0,  self.width, self.height)

        self.program.bind()
        self.posAttr = self.program.attributeLocation("pos")
        self.colAttr = self.program.attributeLocation("col")
        self.program.setAttributeValue('pos', self.posAttr)
        self.program.setAttributeValue('col', self.colAttr)

        self.program.setUniformValue('modelViewMatrix', self.camera.modelViewMatrix)
        self.program.setUniformValue('normalMatrix', self.normalMatrix)
        self.program.setUniformValue('projectionMatrix', self.camera.projectionMatrix)

        glVertexAttribPointer(self.posAttr, 3, GL_FLOAT, GL_FALSE, 0, self.vertices)
        glEnableVertexAttribArray(self.posAttr)

        glVertexAttribPointer(self.colAttr, 3, GL_FLOAT, GL_FALSE, 0, self.colors)
        glEnableVertexAttribArray(self.colAttr)

        glDrawArrays(GL_TRIANGLES, 0, (len(self.vertices)//3))

        glDisableVertexAttribArray(self.colAttr)
        glDisableVertexAttribArray(self.posAttr)

        self.program.release()

    def mousePressEvent(self, event):
        self.pressClick = QVector3D(event.x(), self.height - event.y(), 0)
        self.trackBall.clicked(event.x(), event.y(), self.width, self.height)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.releaseClick = QVector3D(event.x(), self.height - event.y(), 0)
            self.rotation = self.trackBall.move(event.x(), event.y(), self.width, self.height)
            self.update()

    def mouseReleaseEvent(self, event):
        pass

    @property
    def camera(self):
        return self._camera
