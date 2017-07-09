#! /usr/bin/env python
import OpenGL.GL as GL
import numpy as np

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

    @staticmethod
    def ListToArray(list, type):
        vertices = np.asarray(list, dtype=type)
        return vertices

    @staticmethod
    def cubeWithColors():
        return [-1.0, -1.0, -1.0,        0.5, 0.5, 0.5,  # // triangle 1 : begin
                -1.0, -1.0, 1.0,         0.5, 0.0, 0.5,
                -1.0, 1.0, 1.0,         0.2, 0.0, 1.0,  # // triangle 1 : end
                1.0, 1.0, -1.0,         0.0, 0.3, 1.0,  # // triangle 2 : begin
                -1.0, -1.0, -1.0,        1.0, 0.6, 0.0,
                -1.0, 1.0, -1.0,        1.0, 0.0, 1.0,  # // triangle 2 : end
                1.0, -1.0, 1.0,         0.0, 0.0, 0.0,
                -1.0, -1.0, -1.0,        0.0, 0.0, 0.0,
                1.0, -1.0, -1.0,        1.0, 1.0, 1.0,
                1.0, 1.0, -1.0,         0.8, 0.6, 0.0,
                1.0, -1.0, -1.0,         0.5, 0.9, 0.0,
                -1.0, -1.0, -1.0,        0.5, 0.0, 0.0,
                -1.0, -1.0, -1.0,       0.5, 1.0, 1.0,
                -1.0, 1.0, 1.0,      1.0, 1.0, 1.0,
                -1.0, 1.0, -1.0,         1.0, 1.0, 1.0,
                1.0, -1.0, 1.0,         0.6, 0.6, 1.0,
                -1.0, -1.0, 1.0,         0.0, 0.6, 1.0,
                -1.0, -1.0, -1.0,        0.0, 1.0, 1.0,
                -1.0, 1.0, 1.0,         0.0, 1.0, 1.0,
                -1.0, -1.0, 1.0,         0.0, 1.0, 1.0,
                1.0, -1.0, 1.0,      0.0, 0.0, 0.0,
                1.0, 1.0, 1.0,      1.0, 0.0, 1.0,
                1.0, -1.0, -1.0,        1.0, 0.0, 1.0,
                1.0, 1.0, -1.0,      0.0, 1.0, 1.0,
                1.0, -1.0, -1.0,         0.0, 1.0, 1.0,
                1.0, 1.0, 1.0,       0.0, 1.0, 1.0,
                1.0, -1.0, 1.0,         1.0, 1.0, 1.0,
                1.0, 1.0, 1.0,      1.0, 0.0, 0.0,
                1.0, 1.0, -1.0,      1.0, 0.0, 0.0,
                -1.0, 1.0, -1.0,        1.0, 0.0, 0.0,
                1.0, 1.0, 1.0,       1.0, 1.0, 0.0,
                -1.0, 1.0, -1.0,         1.0, 1.0, 0.0,
                -1.0, 1.0, 1.0,      1.0, 1.0, 0.0,
                1.0, 1.0, 1.0,       1.0, 0.0, 1.0,
                -1.0, 1.0, 1.0,      1.0, 0.0, 1.0,
                1.0, -1.0, 1.0,        1.0, 0.0, 1.0]



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