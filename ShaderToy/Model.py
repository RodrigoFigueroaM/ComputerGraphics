#! /usr/bin/env python
import sys
import OpenGL.GL as GL
from ObjectLoader import ObjectLoader

class Model:
    def __init__(self, vaoID, vertices):
        super(Model, self).__init__()
        self._vaoID = vaoID
        self._vertices = vertices
        self._vertexCount = len(vertices)
        self._generateVao()

    def _generateVao(self):
        tempVao = GL.GLuint(0)
        GL.glGenVertexArrays(1, tempVao)
        GL.glBindVertexArray(tempVao)
        return self.vaoID

    @property
    def vaoID(self):
        return self._vaoID

    @vaoID.setter
    def vaoID(self, vaoID):
        self._vaoID = vaoID

if __name__ == "__main__":
    print(bool(GL.glGenFramebuffers()))
    tempVao = GL.GLuint(0)
    GL.glGenVertexArrays(1, tempVao)
    GL.glBindVertexArray(tempVao)
    # objLoader = ObjectLoader("Cube.obj")
    # # objLoader = ObjectLoader("sphere.obj")
    # vtr = objLoader[0]
    # drawingVertices = []
    # for value in vtr:
    #     drawingVertices.append(float(value.x()))
    #     drawingVertices.append(float(value.y()))
    #     drawingVertices.append(float(value.z()))
    #
    # model = Model(0, drawingVertices)
    # print(model.vaoID)