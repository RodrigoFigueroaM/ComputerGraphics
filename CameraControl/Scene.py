#!/usr/bin/env python
import sys
from ctypes import c_void_p, c_float
from PyQt5.QtGui import QMatrix4x4, QVector3D, QWheelEvent
from PyQt5.Qt import Qt
from PyQt5.QtGui import (QOpenGLShader, QOpenGLShaderProgram)
from GLStandardWindow3D import GLStandardWindow3D
from Camera import Camera
from TrackBall import TrackBall
from OpenGL.GL import *


class Scene(GLStandardWindow3D):
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

    # vtr = [
    #     -1.0, -1.0, -1.0,   0.0, 1.0, 1.0, #// triangle 1 : begin
    #     -1.0, -1.0, 1.0,    0.0, 1.0, 1.0,
    #     -1.0, 1.0, 1.0,     0.0, 1.0, 1.0,#// triangle 1 : end
    #     1.0, 1.0, -1.0,     0.0, 1.0, 1.0,# // triangle 2 : begin
    #     -1.0, -1.0, -1.0,   0.0, 1.0, 1.0,
    #     -1.0, 1.0, -1.0,    0.0, 1.0, 1.0,#// triangle 2 : end
    #     1.0, -1.0, 1.0,     0.0, 1.0, 1.0,
    #     -1.0, -1.0, -1.0,   0.0, 1.0, 1.0,
    #     1.0, -1.0, -1.0,    0.0, 1.0, 1.0,
    #     1.0, 1.0, -1.0,     0.0, 1.0, 1.0,
    #     1.0, -1.0, -1.0,    0.0, 1.0, 1.0,
    #     -1.0, -1.0, -1.0,   0.0, 1.0, 1.0,
    #     -1.0, -1.0, -1.0,   0.0, 1.0, 1.0,
    #     -1.0, 1.0, 1.0,     0.0, 1.0, 1.0,
    #     -1.0, 1.0, -1.0,    0.0, 1.0, 1.0,
    #     1.0, -1.0, 1.0,     0.0, 1.0, 1.0,
    #     -1.0, -1.0, 1.0,    0.0, 1.0, 1.0,
    #     -1.0, -1.0, -1.0,   0.0, 1.0, 1.0,
    #     -1.0, 1.0, 1.0,     0.0, 1.0, 1.0,
    #     -1.0, -1.0, 1.0,    0.0, 1.0, 1.0,
    #     1.0, -1.0, 1.0,     0.0, 1.0, 1.0,
    #     1.0, 1.0, 1.0,      0.0, 1.0, 1.0,
    #     1.0, -1.0, -1.0,    0.0, 1.0, 1.0,
    #     1.0, 1.0, -1.0,     0.0, 1.0, 1.0,
    #     1.0, -1.0, -1.0,    0.0, 1.0, 1.0,
    #     1.0, 1.0, 1.0,      0.0, 1.0, 1.0,
    #     1.0, -1.0, 1.0,     0.0, 1.0, 1.0,
    #     1.0, 1.0, 1.0,      0.0, 1.0, 1.0,
    #     1.0, 1.0, -1.0,     0.0, 1.0, 1.0,
    #     -1.0, 1.0, -1.0,    0.0, 1.0, 1.0,
    #     1.0, 1.0, 1.0,      0.0, 1.0, 1.0,
    #     -1.0, 1.0, -1.0,    0.0, 1.0, 1.0,
    #     -1.0, 1.0, 1.0,     0.0, 1.0, 1.0,
    #     1.0, 1.0, 1.0,      0.0, 1.0, 1.0,
    #     -1.0, 1.0, 1.0,     0.0, 1.0, 1.0,
    #     1.0, -1.0, 1.0,     0.0, 1.0, 1.0
    # ]

    vtr = [
        -1.0, -1.0, -1.0,
        -1.0, -1.0, 1.0,
        -1.0, 1.0, 1.0,
        1.0, 1.0, -1.0,
        -1.0, -1.0, -1.0,
        -1.0, 1.0, -1.0,
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
        1.0, -1.0, 1.0,
    ]

    drawingVertices = [float(value) for value in vtr]
    colors =[
        1.0, 0.0, 0.0,
        1.0, 0.0, 0.0,
        1.0, 0.0, 0.0,

        0.0, 0.0, 0.0,
        0.0, 0.0, 0.0,
        0.0, 0.0, 0.0,

        0.0, 1.0, 1.0,
        0.0, 1.0, 1.0,
        0.0, 1.0, 1.0,

        0.0, 0.0, 0.0,
        0.0, 0.0, 0.0,
        0.0, 0.0, 0.0,

        1.0, 0.0, 0.0,
        1.0, 0.0, 0.0,
        1.0, 0.0, 0.0,

        0.0, 1.0, 1.0,
        0.0, 1.0, 1.0,
        0.0, 1.0, 1.0,

        1.0, 0.0, 1.0,
        1.0, 0.0, 1.0,
        1.0, 0.0, 1.0,

        0.0, 1.0, 0.0,
        0.0, 1.0, 0.0,
        0.0, 1.0, 0.0,

        0.0, 1.0, 0.0,
        0.0, 1.0, 0.0,
        0.0, 1.0, 0.0,

        0.0, 0.0, 1.0,
        0.0, 0.0, 1.0,
        0.0, 0.0, 1.0,

        0.0, 0.0, 1.0,
        0.0, 0.0, 1.0,
        0.0, 0.0, 1.0,

        1.0, 0.0, 1.0,
        1.0, 0.0, 1.0,
        1.0, 0.0, 1.0,
    ]

    drawingIndices = [i for i in range(0, len(drawingVertices)//3)]

    def __init__(self):
        super(Scene, self).__init__()
        self.program = QOpenGLShaderProgram(self)
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.StrongFocus)
        self._camera = Camera(position = QVector3D(2, 2, 5),
                              direction = QVector3D(0, 0, 0),
                              up = QVector3D(0, 1, 0),
                              fov = 90)
        self.trackBall = TrackBall()
        self.pressClick = QVector3D()
        self.releaseClick = QVector3D()
        self.rotation = QMatrix4x4()
        self.normalMatrix = QMatrix4x4()
        self.posAttr = 0
        self.colAttr = 0
        #interaction
        self.key = None
        self.th = 0


    def initializeGL(self):
        self.buffer = glGenBuffers(1)

        self.printOpenGLSettings()
        glClearColor(0.2, 0.2, 0.2, 1.0)
        glEnable(GL_DEPTH_TEST)
        self.program.addShaderFromSourceCode(QOpenGLShader.Vertex, self.vertexShaderSource)
        self.program.addShaderFromSourceCode(QOpenGLShader.Fragment, self.fragmentShaderSource)
        self.program.link()


    def paintGL(self):
        self.ratio = self.width / self.height
        self.camera.setPerspective(self.camera.fov, self.ratio, 1.0, 100.0)
        if self.key == Qt.Key_Alt:
            self.camera.lookAt(QVector3D(0, 0, 0))
            self.camera.rotate(self.rotation)
            print(self.rotation)

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

        glEnableVertexAttribArray(self.posAttr)
        glEnableVertexAttribArray(self.colAttr)

        glVertexAttribPointer(self.posAttr, 3, GL_FLOAT, GL_FALSE, sizeof(c_float) * 0, self.drawingVertices)

        glVertexAttribPointer(self.colAttr, 3, GL_FLOAT, GL_FALSE, sizeof(c_float) * 0, self.colors)

        glDrawElements(GL_TRIANGLES, len(self.drawingIndices), GL_UNSIGNED_BYTE, self.drawingIndices)

        glDisableVertexAttribArray(self.colAttr)
        glDisableVertexAttribArray(self.posAttr)
        self.program.release()
        print(self.camera.fov)

    def mousePressEvent(self, event):
        self.th += 1
        self.pressClick = QVector3D(event.x(), self.height - event.y(), 0)
        self.trackBall.clicked(event.x(), event.y(), self.width, self.height)
        self.update()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.releaseClick = QVector3D(event.x(), self.height - event.y(), 0)
            self.rotation = self.trackBall.move(event.x(), event.y(), self.width, self.height)
            self.update()

    def mouseReleaseEvent(self, event):
        self.key = None
        # self.th += 1
        # self.update()

    def wheelEvent(self, QWheelEvent):
        self.camera.fov -= QWheelEvent.angleDelta().y()/40
        self.update()

    def keyPressEvent(self, QKeyEvent):
        self.key = QKeyEvent.key()

    @property
    def camera(self):
        return self._camera
