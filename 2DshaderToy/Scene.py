#!/usr/bin/env python
import ctypes

import OpenGL.GL as GL
import numpy as np
from PyQt5.Qt import Qt
from PyQt5.QtGui import QMatrix4x4, QVector3D, QVector2D
from PyQt5.QtCore import QElapsedTimer
from pyEngine.Camera import Camera
from pyEngine.Model import Model
from pyEngine.GLProgram import GLProgram
from Widgets.GLStandardWindow3D import GLStandardWindow3D

# todo: pan camera
# TODO: render texture infront of other texture aka heat efect
# TODO: add timer variable to shader
# TODO: new window system
# TODO: refactor

IMG_FILE = '/Users/rui/Desktop/githubStuff/ComputerGraphics/2DshaderToy/textures/strawberries.jpg'
VERT_FILE = './shaders/texture.vert'
FRAG_FILE = './shaders/strawberry.frag'


class Scene(GLStandardWindow3D):
    def __init__(self):
        super(Scene, self).__init__()
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.StrongFocus)
        self.colors = []

        self.drawingVertices = []
        self.drawingIndices = []
        self.drawingNormals = []

        self._camera = Camera(position=QVector3D(0, 0, 1.1),
                              direction=QVector3D(0, 0, 0),
                              up=QVector3D(0, 1, 0),
                              fov=90)
        self.pressClick = QVector3D()
        self.releaseClick = QVector3D()
        self.normalMatrix = QMatrix4x4()

        self.initRect()
        self.program = GLProgram(self, numAttibutesInvbo=3)

    def initializeGL(self):
        super(Scene, self).initializeGL()
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        GL.glClearColor(0.2, 0.2, 0.2, 1.0)
        self.program.addTexture(IMG_FILE)
        self.program.initProgram(VERT_FILE,
                                 FRAG_FILE,
                                 self.drawingVertices,
                                 self.drawingIndices,
                                 attribs=[0,1,2])

    def paintGL(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        GL.glViewport(0, 0, self.width, self.height)

        self.ratio = self.width / self.height
        self.camera.setPerspective(self.camera.fov, self.ratio, 0.1, 100.0)

        self.camera.lookAtCenter()
        self.drawProgramSubroutine(self.program, GL.GL_TRIANGLES)
        self.update()

    def drawProgramSubroutine(self, program, mode=GL.GL_TRIANGLE_STRIP):
        nullptr = ctypes.c_void_p(0)
        program.bind()
        program.bindTimer()
        program.setUniformValue('modelViewMatrix', self.camera.modelViewMatrix)
        program.setUniformValue('normalMatrix', self.camera.normalMatrix)
        program.setUniformValue('projectionMatrix', self.camera.projectionMatrix)
        # GL.glDrawArrays(GL.GL_TRIANGLES, 0, (len(program.vertices)//8))
        GL.glDrawElements(mode, len(program.indices), GL.GL_UNSIGNED_INT, nullptr)
        program.unbind()

    def initRect(self):
        vtr, self.drawingIndices, textureCoords = Model.testRec()
        normalsList = normalsPerTriangle(vtr, self.drawingIndices)
        norms = normalsPerVertex(normalsList, len(vtr))
        verticesAndNormals = [(a,b,c) for (a,b,c) in zip(vtr, textureCoords, norms)]
        for row in verticesAndNormals:
            for vector in row:
                # print(vector)
                self.drawingVertices.append(float(vector.x()))
                self.drawingVertices.append(float(vector.y()))
                if hasattr(vector, 'z'):
                    self.drawingVertices.append(float(vector.z()))
        self.drawingVertices = Model.listToArray(list=self.drawingVertices, type=np.float32)
        self.drawingIndices = Model.listToArray(list=self.drawingIndices, type=np.int32)

    def mousePressEvent(self, event):
        self.pressClick = QVector3D(event.x(), self.height - event.y(), 0)
        self.update()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.releaseClick = QVector3D(event.x(), self.height - event.y(), 0)
            self.update()

    def mouseReleaseEvent(self, event):
        self.key = None

    def wheelEvent(self, QWheelEvent):
        self.camera.fov -= QWheelEvent.angleDelta().y() / 40
        self.update()

    def keyPressEvent(self, QKeyEvent):
        self.key = QKeyEvent.key()
        self.update()

    @property
    def camera(self):
        return self._camera


def initTimer(interval=100):
    timer = QElapsedTimer()
    timer.start()
    return timer

'''TODO: delete'''
def testCube():
    vtr = [QVector3D(-0.5, 0.5, -0.5),
           QVector3D(-0.5, -0.5, -0.5),
           QVector3D(0.5, -0.5, -0.5),
           QVector3D(0.5, 0.5, -0.5),

           QVector3D(-0.5, 0.5, 0.5),
           QVector3D(-0.5, -0.5, 0.5),
           QVector3D(0.5, -0.5, 0.5),
           QVector3D(0.5, 0.5, 0.5),

           QVector3D(0.5, 0.5, -0.5),
           QVector3D(0.5, -0.5, -0.5),
           QVector3D(0.5, -0.5, 0.5),
           QVector3D(0.5, 0.5, 0.5),

           QVector3D(-0.5, 0.5, -0.5),
           QVector3D(-0.5, -0.5, -0.5),
           QVector3D(-0.5, -0.5, 0.5),
           QVector3D(-0.5, 0.5, 0.5),

           QVector3D(-0.5, 0.5, 0.5),
           QVector3D(-0.5, 0.5, -0.5),
           QVector3D(0.5, 0.5, -0.5),
           QVector3D(0.5, 0.5, 0.5),

           QVector3D(-0.5, -0.5, 0.5),
           QVector3D(-0.5, -0.5, -0.5),
           QVector3D(0.5, -0.5, -0.5),
           QVector3D(0.5, -0.5, 0.5),
           ]

    drawingIndices = [0, 1, 3,
                           3, 1, 2,
                           4, 5, 7,
                           7, 5, 6,
                           8, 9, 11,
                           11, 9, 10,
                           12, 13, 15,
                           15, 13, 14,
                           16, 17, 19,
                           19, 17, 18,
                           20, 21, 23,
                           23, 21, 22]

    textureCoords = [
        QVector2D(0, 0),
        QVector2D(0, 1),
        QVector2D(1, 1),
        QVector2D(1, 0),
        QVector2D(0, 0),
        QVector2D(0, 1),
        QVector2D(1, 1),
        QVector2D(1, 0),
        QVector2D(0, 0),
        QVector2D(0, 1),
        QVector2D(1, 1),
        QVector2D(1, 0),
        QVector2D(0, 0),
        QVector2D(0, 1),
        QVector2D(1, 1),
        QVector2D(1, 0),
        QVector2D(0, 0),
        QVector2D(0, 1),
        QVector2D(1, 1),
        QVector2D(1, 0),
        QVector2D(0, 0),
        QVector2D(0, 1),
        QVector2D(1, 1),
        QVector2D(1, 0)
    ]
    return vtr, drawingIndices, textureCoords

def testRec():
    vtr = [QVector3D(-1.0, 1.0, 0.0),
           QVector3D(-1.0, -1.0, 0.0),
           QVector3D(1.0, -1.0, 0.0),
           QVector3D(1.0, 1.0, 0.0)]

    drawingIndices=[0, 1, 3, 3, 1, 2]

    textureCoords = [ QVector2D(0, 0),
                    QVector2D(1, 0),
                    QVector2D(1, 1),
                    QVector2D(1, 0) ]
    return vtr, drawingIndices, textureCoords

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
        verticesNormals.append(normalsAvg)
    return verticesNormals


def normalsPerTriangle(vertices=None, indices=None):
    triangleNormals = []
    i = 0
    for index in range(0, len(indices) - 2, 1):
        if indices[index] != indices[index - 1] and indices[index] != indices[index + 1] and indices[index - 1] != \
                indices[index + 1]:
            a = (vertices[indices[index - 1]] - vertices[indices[index]])
            b = (vertices[indices[index + 1]] - vertices[indices[index]])
            # if index % 2 == 0:
            normal = QVector3D.crossProduct(b, a)
            # else:
            #     normal = QVector3D.crossProduct(a, b)
            triangleNormals.append([i, (indices[index], indices[index - 1], indices[index + 2]), normal])
            i += 1
    return triangleNormals
