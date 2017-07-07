#!/usr/bin/env python
import sys
from ctypes import c_void_p, c_float, sizeof, c_uint
import ctypes
from PyQt5.QtGui import QMatrix4x4, QVector3D, QWheelEvent , QOpenGLShader, QOpenGLShaderProgram, QOpenGLBuffer , QOpenGLVertexArrayObject
from PyQt5.Qt import Qt
from GLStandardWindow3D import GLStandardWindow3D
from Camera import Camera
from ObjectLoader import ObjectLoader
from TrackBall import TrackBall
import OpenGL.GL as GL
from Model import Model
import numpy as np
import numpy as np

# TODO: create loader class
# TODO: new window system
# TODO: fix obj loader class
# TODO:

class Scene(GLStandardWindow3D):
    vertexShaderSource = """
    #version 330

    layout(location = 0) in vec4 pos;
    out vec4 vertex;

    void main() 
    {
        vertex = pos;
        gl_Position = pos;
    }"""

    fragmentShaderSource = """
    # version 330
    in vec4 vertex;
    out vec4 FragColor;
    void main() 
{
     FragColor = vec4(1.0,1.0,1.0,1.0);
}
"""
  
    def __init__(self):
        super(Scene, self).__init__()
        # self.program = QOpenGLShaderProgram(self)
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.StrongFocus)
        self.colors = []

        self.drawingVertices = []
        self.drawingIndices = []
        self.drawingNormals = []

        # objLoader = ObjectLoader("Cube.obj")
        # objLoader = ObjectLoader("sphere.obj")
        # self.vtr = objLoader[0]

        # for value in self.vtr:
        #     self.drawingVertices.append(float(value.x()))
        #     self.drawingVertices.append(float(value.y()))
        #     self.drawingVertices.append(float(value.z()))

        # self.drawingIndices = objLoader[1]
        # normalsList = normalsPerTriangle(self.vtr, self.drawingIndices)
        # self.normals = normalsPerVertex(normalsList, len(self.vtr))
        # self.normals = [PyQt5.QtGui.QVector3D(0.0, 0.0, -1.0), PyQt5.QtGui.QVector3D(-1.0, -0.0, -0.0), PyQt5.QtGui.QVector3D(-0.0, -0.0, 1.0), PyQt5.QtGui.QVector3D(-9.999999974752427e-07, 0.0, 1.0), PyQt5.QtGui.QVector3D(1.0, -0.0, 0.0), PyQt5.QtGui.QVector3D(1.0, 0.0, 9.999999974752427e-07), PyQt5.QtGui.QVector3D(0.0, 1.0, -0.0), PyQt5.QtGui.QVector3D(-0.0, -1.0, 0.0)]
        # self.normals = objLoader[3]
        # for value in self.normals:
        #     self.drawingNormals.append(float(value.x()))
        #     self.drawingNormals.append(float(value.y()))
        #     self.drawingNormals.append(float(value.z()))
        # print(self.normals)

        self._camera = Camera(position=QVector3D(2, 2, 5),
                              direction=QVector3D(0, 0, 0),
                              up=QVector3D(0, 1, 0),
                              fov=90)
        self.trackBall = TrackBall()
        self.pressClick = QVector3D()
        self.releaseClick = QVector3D()
        self.rotation = QMatrix4x4()
        self.normalMatrix = QMatrix4x4()
        self.posAttr = 0
        self.colAttr = 0
        # interaction
        self.key = None
        self.th = 0
        self.showWireFrame = True

        #:/
        self.program = QOpenGLShaderProgram(self)
        self.vertex = QOpenGLBuffer()
        self.object = QOpenGLVertexArrayObject()

        self.drawingVertices = [-0.5, 0.5, 0.0,
                           -0.5, -0.5, 0.0,
                           0.5, -0.5, 0.0,

                           0.5, -0.5, 0,
                           0.5, 0.5, 0,
                           -0.5, 0.5, 0]
        self.drawingVertices = np.asarray(self.drawingVertices, dtype=np.float32)

    def initializeGL(self):
        self.printOpenGLSettings()

        GL.glClearColor(0.2, 0.2, 0.2, 1.0)
        #shader program
        self.program.addShaderFromSourceCode(QOpenGLShader.Vertex, self.vertexShaderSource)
        self.program.addShaderFromSourceCode(QOpenGLShader.Fragment, self.fragmentShaderSource)
        self.program.link()
        self.program.bind()

        #vertices
        self.vertex.create()
        self.vertex.bind()
        self.vertex.usagePattern()
        self.vertex.allocate(self.drawingVertices, self.drawingVertices.nbytes)

        #object
        self.object.create()
        self.object.bind()
        self.program.enableAttributeArray(0)

        self.program.setAttributeBuffer(0, GL.GL_FLOAT, 0, 3, 0)
        # self.program.setAttributeArray(0, GL.GL_FLOAT, 0, len(self.drawingVertices), 0)

        self.object.release()
        self.vertex.release()
        self.program.release()


    def paintGL(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        self.program.bind()
        self.object.bind()
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, len(self.drawingVertices)//3)
        self.object.release()
        self.program.release()

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
