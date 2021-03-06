#!/usr/bin/env python
import ctypes

import OpenGL.GL as GL
from PyQt5.Qt import Qt
from PyQt5.QtCore import QElapsedTimer
from PyQt5.QtGui import QMatrix4x4, QVector3D , QOpenGLFramebufferObject

from Widgets.GLStandardWindow3D import GLStandardWindow3D
from pyEngine.Camera import Camera
from pyEngine.GLProgram import GLProgram
from pyEngine.Geometry.Grid import Grid
from pyEngine.Model import Model
from pyEngine.TrackBall import TrackBall

# TODO: fix obj loader indices(texture)(normals?)
# TODO: model class :- refractor and make functional model class
# TODO: new window system
# TODO: refactor


IMG_FILE = '/Users/rui/Desktop/githubStuff/ComputerGraphics/ShaderToy/textures/cc.jpg'

VERT_FILE = '/Users/rui/Desktop/githubStuff/ComputerGraphics/ShaderToy/shaders/matte.vert'
FRAG_FILE = '/Users/rui/Desktop/githubStuff/ComputerGraphics/ShaderToy/shaders/matte.frag'

# VERT_FILE2 = '/Users/rui/Desktop/githubStuff/ComputerGraphics/ShaderToy/shaders/blinPhong.vert'
# FRAG_FILE2 = '/Users/rui/Desktop/githubStuff/ComputerGraphics/ShaderToy/shaders/blinPhong.frag'
MODEL_FILE = '/Users/rui/Desktop/githubStuff/ComputerGraphics/ShaderToy/objs/Cerberus.obj'

GRID_VERT = '/Users/rui/Desktop/githubStuff/ComputerGraphics/ShaderToy/shaders/grid.vert'
GRID_FRAG = '/Users/rui/Desktop/githubStuff/ComputerGraphics/ShaderToy/shaders/grid.frag'


class Scene(GLStandardWindow3D):
    def __init__(self):
        super(Scene, self).__init__()
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.StrongFocus)

        self._camera = Camera()

        # properties
        self.trackBall = TrackBall()
        self.rotation = QMatrix4x4()
        self.normalMatrix = QMatrix4x4()

        # properties interaction
        self.key = None
        self.showWireFrame = True

        # methods
        self.initCamera()
        self.model = Model(MODEL_FILE)

        #grid lists
        self.grid = Grid()

        # GLPROGRAMS
        self._program = GLProgram(self, numAttibutesInvbo=3)
        self.gridProgram = GLProgram(self, numAttibutesInvbo=3)

        # FBO
        self.fbo = None

    def initializeGL(self):
        super(Scene, self).initializeGL()
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        GL.glClearColor(0.3, 0.3, 0.3, 1.0)



        # self.fbo = QOpenGLFramebufferObject(100, 100, QOpenGLFramebufferObject.CombinedDepthStencil, GL.GL_TEXTURE_2D)
        # self.fbo.bind()
        # self.fbo.release()

        self.program.addTexture(IMG_FILE)
        self.program.initProgram(VERT_FILE,
                                 FRAG_FILE,
                                 self.model.drawingVertices,
                                 self.model.verticesIndices,
                                 attribs=[0, 1, 2])

        self.gridProgram.initProgram(GRID_VERT,
                                     GRID_FRAG,
                                     self.grid.drawingVertices,
                                     self.grid.verticesIndices,
                                     attribs=[0, 1, 2])

    def paintGL(self):
        # self.fbo.bind()
        # print(self.fbo.toImage())

        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        GL.glViewport(0, 0, self.width, self.height)
        self.ratio = self.width / self.height
        self.camera.setPerspective(self.camera.fov, self.ratio, 0.1, 100.0)
        self.camera.lookAtCenter()

        if self.showWireFrame:
            GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL)
        else:
            GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_LINE)

        self.drawProgramSubroutine(self.program, GL.GL_TRIANGLES)
        self.update()
        # self.drawProgramSubroutine(self.gridProgram, GL.GL_LINES)
        # self.fbo.release()


    def initCamera(self):
        self._camera = Camera(position=QVector3D(0, 0, 3),
                              direction=QVector3D(0.0, 0, 0.0),
                              up=QVector3D(0, 1, 0),
                              fov=90)

    def drawProgramSubroutine(self, program, mode=GL.GL_TRIANGLE_STRIP):
        nullptr = ctypes.c_void_p(0)
        program.bind()
        program.bindTimer()
        program.setUniformValue('modelViewMatrix', self.camera.modelViewMatrix)
        program.setUniformValue('normalMatrix', self.camera.normalMatrix)
        program.setUniformValue('projectionMatrix', self.camera.projectionMatrix)
        program.setUniformValue('modelTransformationMatrix', self.model.transformationMatrix)
        GL.glDrawElements(mode, len(program.indices), GL.GL_UNSIGNED_INT, nullptr)
        program.unbind()

    def mousePressEvent(self, event):
        self.pressClick = QVector3D(event.x(), self.height - event.y(), 0)
        self.trackBall.clicked(event.x(), event.y(), self.width, self.height)
        self.update()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.releaseClick = QVector3D(event.x(), self.height - event.y(), 0)
            self.rotation = self.trackBall.move(event.x(), event.y(), self.width, self.height)
            self.camera.position = self.rotation * self.camera.position
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
            # self.update()

    @property
    def camera(self):
        return self._camera

    @property
    def program(self):
        return self._program


def initTimer(interval=100):
    timer = QElapsedTimer()
    timer.start()
    return timer