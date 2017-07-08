#!/usr/bin/env python
import sys
from ctypes import c_void_p, c_float, sizeof, c_uint
import ctypes
from PyQt5.QtGui import QMatrix4x4, QVector3D, QWheelEvent , QOpenGLShader, QOpenGLShaderProgram, QOpenGLBuffer , QOpenGLVertexArrayObject
from PyQt5.Qt import Qt
from GLStandardWindow3D import GLStandardWindow3D
from Camera import Camera
from ObjLoader import ObjectLoader
from GLProgram import GLProgram
from TrackBall import TrackBall
import OpenGL.GL as GL
from Model import Model
from Model import Model
import numpy as np

# TODO: new window system
# TODO: fix obj loader class


class Scene(GLStandardWindow3D):
    def __init__(self):
        super(Scene, self).__init__()
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.StrongFocus)
        self.colors = []

        self.drawingVertices = []
        self.drawingIndices = []
        self.drawingNormals = []

        self._camera = Camera(position=QVector3D(0, 0,3),
                              direction=QVector3D(0, 0, 0),
                              up=QVector3D(0, 1, 0),
                              fov=90)

        self.trackBall = TrackBall()
        self.pressClick = QVector3D()
        self.releaseClick = QVector3D()
        self.rotation = QMatrix4x4()
        self.normalMatrix = QMatrix4x4()

        # interaction
        self.key = None
        self.th = 0
        self.showWireFrame = True

        # objLoader = ObjectLoader("./objs/sphere.obj")
        objLoader = ObjectLoader("./objs/Cerberus.obj")
        vtr = objLoader[0]
        norms = objLoader[3]
        verticesAndNormals = [j for i in zip(vtr, norms) for j in i]

        for vector in verticesAndNormals:
            self.drawingVertices.append(float(vector.x()))
            self.drawingVertices.append(float(vector.y()))
            self.drawingVertices.append(float(vector.z()))

        print(len(vtr))
        print(len(norms))
        print(len(verticesAndNormals))

        self.drawingIndices = objLoader[1]
        # self.drawingVertices = Model.cubeWithColors()

        self.drawingVertices = Model.ListToArray(list=self.drawingVertices, type=np.float32)
        self.drawingIndices = Model.ListToArray(list=self.drawingIndices, type=np.int32)
        self.program = GLProgram(self, numAttibutesInvbo=2)

    def initializeGL(self):
        super(Scene, self).initializeGL()
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        GL.glClearColor(0.2, 0.2, 0.2, 1.0)
        self.program.initProgram('./shaders/blinPhong.vert', './shaders/toon.frag',
                                 self.drawingVertices, self.drawingIndices, attribs=[0,1])
        print(self.drawingVertices)
        print(len(self.drawingVertices))

    def paintGL(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        GL.glViewport(0, 0, self.width, self.height)

        self.ratio = self.width / self.height
        self.camera.setPerspective(self.camera.fov, self.ratio, 0.1, 100.0)

        self.camera.lookAtCenter()
        self.camera.position = self.rotation * self.camera.position

        if self.showWireFrame:
            GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL)
        else:
            GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_LINE)

        self.drawProgramSubrutine(self.program,GL.GL_TRIANGLES)

    def drawProgramSubrutine(self, program, mode=GL.GL_TRIANGLES):
        Nullptr = ctypes.c_void_p(0)
        program.bind()
        program.setUniformValue('modelViewMatrix', self.camera.modelViewMatrix)
        self.program.setUniformValue('normalMatrix', self.camera.normalMatrix)
        program.setUniformValue('projectionMatrix', self.camera.projectionMatrix)
        GL.glDrawElements(mode, len(program.indices), GL.GL_UNSIGNED_INT, Nullptr)
        program.unbind()

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

    def wheelEvent(self, QWheelEvent):
        self.camera.fov -= QWheelEvent.angleDelta().y() / 40
        self.update()

    def keyPressEvent(self, QKeyEvent):
        self.key = QKeyEvent.key()
        if QKeyEvent.key() == Qt.Key_W:
            self.showWireFrame = not self.showWireFrame
        self.update()

    @property
    def camera(self):
        return self._camera

def normalsPerVertex(faces = None, numberOfVertices = 0):
    # make sublist of vertices and triangles tahta affect the
    li =[]
    for index in range(0, numberOfVertices, 1):
        inli = []
        for face in faces:
            if index == face[1][0]:
                inli.append(face[0])
            if index == face[1][1]:
                 inli.append(face[0])
            if index == face[1][2]:
                 inli.append(face[0])
        li.append([index, inli])

    verticesNormals = []
    for row in li:
        normalsAvg = QVector3D(0,0,0)
        for index in row[1]:
            normalsAvg += faces[index][2]
        normalsAvg = normalsAvg / len(row[1])
        normalsAvg = normalsAvg.normalized()
        verticesNormals.append( normalsAvg )
    return verticesNormals

def normalsPerTriangle(vertices = None, indices = None):
        triangleNormals = []
        i = 0
        for index in range( 0, len(indices) - 2 , 1):
            if indices[ index ] != indices[ index - 1] and  indices[ index ] != indices[ index + 1] and indices[ index - 1 ] != indices[ index + 1]:
                a = (vertices[indices[ index - 1 ]] - vertices[indices[ index ]])
                b = (vertices[indices[ index + 1 ]] - vertices[indices[ index ]])
                normal = QVector3D.crossProduct(b, a)
                triangleNormals.append([ i ,(indices[ index],indices[ index - 1],indices[ index + 2 ]), normal])
                i += 1
        return triangleNormals
