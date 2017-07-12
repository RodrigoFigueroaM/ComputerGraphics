#!/usr/bin/env python
import ctypes

import OpenGL.GL as GL
import numpy as np
from PyQt5.Qt import Qt
from PyQt5.QtGui import QMatrix4x4, QVector3D, QVector2D
from PyQt5.QtCore import QElapsedTimer
from pyEngine.Camera import Camera
from pyEngine.Model import Model
from pyEngine.ObjLoader import ObjectLoader
from pyEngine.GLProgram import GLProgram
from pyEngine.TrackBall import TrackBall
from Widgets.GLStandardWindow3D import GLStandardWindow3D


# TODO: try to switch shaders on the go
# TODO: fix obj loader indices(texture)(normals?)
# TODO: model class : refractor and make functional model class
# TODO:                 holds images
# TODO: new window system
# TODO: refactor


IMG_FILE = '/Users/rui/Desktop/githubStuff/ComputerGraphics/ShaderToy/textures/zen.jpg'
VERT_FILE3 = './shaders/blinPhong.vert'
FRAG_FILE3 = './shaders/toon.frag'
VERT_FILE2 = './shaders/shafae_blinn_phong.vert'
FRAG_FILE2 = './shaders/shafae_blinn_phong.frag'

VERT_FILE = './shaders/blinPhong.vert'
FRAG_FILE = './shaders/blinPhong.frag'
MODEL_FILE = '/Users/rui/Desktop/githubStuff/ComputerGraphics/ShaderToy/objs/uv_sphere.obj'

GRID_VERT = './shaders/grid.vert'
GRID_FRAG = './shaders/grid.frag'


class Scene(GLStandardWindow3D):
    def __init__(self):
        super(Scene, self).__init__()
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.StrongFocus)
        self.colors = []

        self.drawingVertices = []
        self.drawingIndices = []
        self.drawingNormals = []

        self._camera = Camera(position=QVector3D(2, 1, 5),
                              direction=QVector3D(0.5, 0, 0.5),
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

        objLoader = ObjectLoader(MODEL_FILE)
        vtr = objLoader[0][:]
        self.drawingIndices = objLoader[1]
        textureCoords = objLoader[2]
        norms = objLoader[3]

        verticesAndNormals = [(a,b,c) for (a,b,c) in zip(vtr, textureCoords, norms)]
        # print(verticesAndNormals)
        # print(norms[23], norms[24], norms[25])
        for row in verticesAndNormals:
            for vector in row:
                self.drawingVertices.append(float(vector.x()))
                self.drawingVertices.append(float(vector.y()))
                try:
                    self.drawingVertices.append(float(vector.z()))
                except:
                    pass

        self.drawingVertices = Model.ListToArray(list=self.drawingVertices, type=np.float32)
        self.drawingIndices = Model.ListToArray(list=self.drawingIndices, type=np.int32)
        self.program = GLProgram(self, numAttibutesInvbo=3)


        '''SEC0ND HEAD'''
        self.drawingVertices2 = []
        # objLoader = ObjectLoader(MODEL_FILE)
        vtr2 = objLoader[0][:]
        self.drawingIndices2 = objLoader[1]
        textureCoords2 = objLoader[2]
        norms2 = objLoader[3]

        T = QMatrix4x4()
        T.translate(-2, 0, 0)
        for i in range(0, len(vtr2)):
            vtr2[i] = T * vtr2[i]

        verticesAndNormals2 = [(a, b, c) for (a, b, c) in zip(vtr2, textureCoords2, norms2)]
        for row in verticesAndNormals2:
            for vector in row:
                # print(vector)
                self.drawingVertices2.append(float(vector.x()))
                self.drawingVertices2.append(float(vector.y()))
                if hasattr(vector, 'z'):
                    self.drawingVertices2.append(float(vector.z()))

        self.drawingVertices2 = Model.ListToArray(list=self.drawingVertices2, type=np.float32)
        self.drawingIndices2 = Model.ListToArray(list=self.drawingIndices2, type=np.int32)
        self.program2 = GLProgram(self, numAttibutesInvbo=3)


        '''HEAD 3'''
        self.drawingVertices3 = []
        # objLoader = ObjectLoader(MODEL_FILE)
        vtr3 = objLoader[0][:]
        self.drawingIndices3 = objLoader[1]
        textureCoords3 = objLoader[2]
        norms3 = objLoader[3]

        T = QMatrix4x4()
        T.translate(2, 0, 0)
        for i in range(0, len(vtr3)):
            vtr3[i] = T * vtr3[i]

        verticesAndNormals3 = [(a, b, c) for (a, b, c) in zip(vtr3, textureCoords3, norms3)]
        for row in verticesAndNormals3:
            for vector in row:
                # print(vector)
                self.drawingVertices3.append(float(vector.x()))
                self.drawingVertices3.append(float(vector.y()))
                if hasattr(vector, 'z'):
                    self.drawingVertices3.append(float(vector.z()))

        self.drawingVertices3 = Model.ListToArray(list=self.drawingVertices3, type=np.float32)
        self.drawingIndices3 = Model.ListToArray(list=self.drawingIndices3, type=np.int32)
        self.program3 = GLProgram(self, numAttibutesInvbo=3)



        self.gridVertices = []
        self.gridIndices = []
        gridVtr, self.gridIndices, gridTextureCoords, normals = grid(1)
        gridVericesAndNormals = [(a, b, c) for (a, b, c) in zip(gridVtr, gridTextureCoords, normals)]
        for row in gridVericesAndNormals:
            for vector in row:
                # print(vector)
                self.gridVertices.append(float(vector.x()))
                self.gridVertices.append(float(vector.y()))
                if hasattr(vector, 'z'):
                    self.gridVertices.append(float(vector.z()))
        self.gridVertices = Model.ListToArray(list=self.gridVertices, type=np.float32)
        self.gridIndices = Model.ListToArray(list=self.gridIndices, type=np.int32)
        self.gridProgram = GLProgram(self, numAttibutesInvbo=3)

    def initializeGL(self):
        super(Scene, self).initializeGL()
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        GL.glClearColor(0.36, 0.36, 0.36, 1.0)
        # self.program.addTexture(IMG_FILE)

        self.program.initProgram(VERT_FILE,
                                 FRAG_FILE,
                                 self.drawingVertices,
                                 self.drawingIndices,
                                 attribs=[0,1,2])

        self.program2.initProgram(VERT_FILE2,
                                 FRAG_FILE2,
                                 self.drawingVertices2,
                                 self.drawingIndices2,
                                 attribs=[0, 1, 2])

        self.program3.initProgram(VERT_FILE3,
                                  FRAG_FILE3,
                                  self.drawingVertices3,
                                  self.drawingIndices3,
                                  attribs=[0, 1, 2])

        self.gridProgram.initProgram(GRID_VERT,
                                     GRID_FRAG,
                                     self.gridVertices,
                                     self.gridIndices,
                                     attribs=[0, 1, 2])

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

        self.drawProgramSubroutine(self.program, GL.GL_TRIANGLES)
        self.drawProgramSubroutine(self.program2, GL.GL_TRIANGLES)
        self.drawProgramSubroutine(self.program3, GL.GL_TRIANGLES)
        self.drawProgramSubroutine(self.gridProgram, GL.GL_LINES)
        # self.update()

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
        if QKeyEvent.key() == Qt.Key_R:
            self.showWireFrame = not self.showWireFrame
            self.update()

    @property
    def camera(self):
        return self._camera


def initTimer(interval=100):
    timer = QElapsedTimer()
    timer.start()
    return timer

def grid(scale):
    mainLine = [ QVector3D(0, 0, 0), QVector3D(1, 0, 0)]
    T = QMatrix4x4()
    vtr = mainLine[:]
    numLines = 12
    for i in range(0, numLines - 1):
        vtr.append(T * mainLine[0])
        vtr.append(T * mainLine[1])
        T.translate(0.0, 0.0, 0.1)

    T.setToIdentity()
    T.translate(0.0, 0.0, 1.0)
    T.rotate(90, 0, 1, 0)
    for i in range(0, numLines - 1):
        vtr.append(T * mainLine[0])
        vtr.append(T * mainLine[1])
        T.translate(0.0, 0.0, 0.1)

    T.setToIdentity()
    T.scale(scale)
    for i in range(0, len(vtr)):
        vtr[i] = T * vtr[i]

    drawingIndices = [i for i in range(0, len(vtr))]
    textureCoords = [QVector2D(0.0, 0.0) for  i in range(0, len(vtr))]
    normals = [QVector3D(0, 0, 0) for i in range(0, len(vtr))]
    return vtr, drawingIndices, textureCoords, normals

