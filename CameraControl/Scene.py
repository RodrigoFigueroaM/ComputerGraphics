#!/usr/bin/env python
import sys
from ctypes import c_void_p, c_float
from PyQt5.QtGui import QMatrix4x4, QVector3D, QWheelEvent
from PyQt5.Qt import Qt
from PyQt5.QtGui import (QOpenGLShader, QOpenGLShaderProgram)
from GLStandardWindow3D import GLStandardWindow3D
from pyEngine.Camera import Camera
from pyEngine.TrackBall import TrackBall
from OpenGL.GL import *


class Scene(GLStandardWindow3D):
    vertexShaderSource = """
    uniform highp mat4 projectionMatrix;
    uniform highp mat4 modelViewMatrix;
    uniform highp mat4 normalMatrix;
    
    
    attribute highp vec4 pos;
    attribute lowp vec4 col;
    attribute vec3 normalAttr; // .normals
    
    varying vec3 normal;
    varying lowp vec4 color;
    varying vec4 vertex;
    
    void main() 
    {
       color = col;
    normal = normalAttr;
     vertex = pos;
       gl_Position = projectionMatrix * modelViewMatrix * pos;
    }"""

    fragmentShaderSource = """
   #version 120\n
    
    uniform highp mat4 projectionMatrix;
    uniform highp mat4 modelViewMatrix;
    uniform highp mat4 normalMatrix; 
    
    
    varying vec3 normal;
    varying vec4 vertex;
    
    const vec3 lightPos = vec3(2.0, 0.0, 2.0);
    const vec3 lightColor = vec3(1.0, 1.0, 1.0);
    
    const vec3 ambientColor = vec3(0.3, 0.0, 0.3);
    const vec3 diffuseColor = vec3(0.5, 0.5, 0.5);
    const vec3 specularColor = vec3(1.0, 1.0, 1.0);
    const vec3 emitColor = vec3(0.5, 0.0, 0.5);
    
    const float shininess = 160.0;
    
    const vec3 eyePos = vec3 (0,0,0);
    
    
    void main() 
    {
        vec4 tempVertex = modelViewMatrix * vertex;
        vec3 vrtx = tempVertex.xyz / tempVertex.w;
    
        vec4 tempNormal = normalMatrix * vec4(normal,0.0);
        vec3 nrml =  normalize(tempNormal.xyz);
    
    
    
        vec3 eyeDir = normalize(eyePos - vrtx); // V
        vec3 lightDir = normalize(lightPos - vrtx); //L
        vec3 halfVector = normalize(lightDir + eyeDir); //H
    
        //DIFFUSE 
        float NdotL = dot(nrml, lightDir );
        vec3 lambert = NdotL * diffuseColor * lightColor * max(NdotL ,0.0);
    
        //SPECULAR
        float NdotH = dot(nrml, halfVector);
        vec3  blinnPhong = lightColor * specularColor * pow( max(NdotH,0.0 ), shininess );
    
    
        gl_FragColor = vec4(lambert  + ambientColor , 1.0);
    }"""


    vtr = [
        1.0, -1.0, -1.0, 1.0, -1.0, 1.0, -1.0, -1.0, 1.0, -1.0, -1.0, -1.0, 1.0, 1.0, -1.0, 0.999999, 1.0, 1.000001,
        -1.0, 1.0, 1.0, -1.0, 1.0, -1.0
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

    drawingIndices = [4, 0, 3, 4, 3, 7, 2, 6, 7, 2, 7, 3, 1, 5, 2, 5, 6, 2, 0, 4, 1, 4, 5, 1, 4, 7, 5, 7, 6, 5, 0, 1, 2, 0, 2, 3]
    drawingNormals = [0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1e-06, 0.0, 1.0, 1.0, 0.0, 0.0, 1.0,
                           0.0, 1e-06, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0]

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
        self.camera.lookAt(QVector3D(0, 0, 0))
        if self.key == Qt.Key_Alt: 
            self.camera.rotate(self.rotation)

        self.normalMatrix = self.camera.modelViewMatrix.inverted()[0].transposed()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glViewport(0, 0,  self.width, self.height)

        self.program.bind()
        self.posAttr = self.program.attributeLocation("pos")
        self.colAttr = self.program.attributeLocation("col")
        self.normalAttr = self.program.attributeLocation("normalAttr")
        self.program.setAttributeValue('pos', self.posAttr)
        self.program.setAttributeValue('col', self.colAttr)
        self.program.setAttributeValue('normalAttr', self.normalAttr)

        self.program.setUniformValue('modelViewMatrix', self.camera.modelViewMatrix)
        self.program.setUniformValue('normalMatrix', self.normalMatrix)
        self.program.setUniformValue('projectionMatrix', self.camera.projectionMatrix)

        glEnableVertexAttribArray(self.posAttr)
        glEnableVertexAttribArray(self.colAttr)
        glEnableVertexAttribArray(self.normalAttr)

        glVertexAttribPointer(self.posAttr, 3, GL_FLOAT, GL_FALSE, sizeof(c_float) * 0, self.drawingVertices)
        glVertexAttribPointer(self.normalAttr, 3, GL_FLOAT, GL_FALSE, sizeof(c_float) * 0, self.drawingNormals)
        glVertexAttribPointer(self.colAttr, 3, GL_FLOAT, GL_FALSE, sizeof(c_float) * 0, self.colors)

        glDrawElements(GL_TRIANGLES, len(self.drawingIndices), GL_UNSIGNED_BYTE, self.drawingIndices)

        # glDisableVertexAttribArray(self.normalAttr)
        glDisableVertexAttribArray(self.posAttr)
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
        # self.update()

    def wheelEvent(self, QWheelEvent):
        self.camera.fov -= QWheelEvent.angleDelta().y()/40
        self.update()

    def keyPressEvent(self, QKeyEvent):
        self.key = QKeyEvent.key()

    @property
    def camera(self):
        return self._camera
