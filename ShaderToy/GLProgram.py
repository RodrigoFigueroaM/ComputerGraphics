from PyQt5.QtGui import QOpenGLShader, QOpenGLShaderProgram, QOpenGLBuffer, QOpenGLVertexArrayObject
import OpenGL.GL as GL


class GLProgram:
    def __init__(self, context, numAttibutesInvbo = 1):
        super(GLProgram, self).__init__()
        self.num_of_elements_in_vbo = numAttibutesInvbo
        self.vertex_elements = 3
        self._program = QOpenGLShaderProgram(context)
        self._vertexBufferObject = QOpenGLBuffer(QOpenGLBuffer.VertexBuffer)
        self._indexesBufferObject = QOpenGLBuffer(QOpenGLBuffer.IndexBuffer)
        self._vertexArrayObject = QOpenGLVertexArrayObject()
        self._vertices = []
        self._indices = []
        self.attributes = []

    def initProgram(self, vertFile, fragFile, vertices, indices, attribs):
        self.vertices = vertices
        self.indices = indices
        self.initShaderProgram(vertFile, fragFile)
        self.initVertexBuffer()
        self.initIndexBuffer()
        self.initVAO()
        for i in attribs:
            self.enableAttributeArray(i)
        self.bindAttributes()
        self.indexBufferObject.bind()
        self.releaseBuffersAndProgram()

    def releaseBuffersAndProgram(self):
        self.VAO.release()
        self.vertexBufferObject.release()
        self.indexBufferObject.release()
        self.program.release()

    def unbind(self):
        self.VAO.release()
        self.program.release()

    def initShaderProgram(self, *arg):
        """ :arg
            path to .vert program
            path to .frag program"""
        # shader program
        self.program.addShaderFromSourceFile(QOpenGLShader.Vertex, arg[0])
        self.program.addShaderFromSourceFile(QOpenGLShader.Fragment, arg[1])
        self.program.link()
        self.program.bind()

    def initVertexBuffer(self):
        # vertices
        self.vertexBufferObject.create()
        self.vertexBufferObject.bind()
        self.vertexBufferObject.setUsagePattern(QOpenGLBuffer.StaticDraw)
        self.vertexBufferObject.allocate(self.vertices, self.vertices.nbytes)
        self.vertexBufferObject.release()
        self.vertexBufferObject.bind()

    def initIndexBuffer(self):
        # indices
        self.indexBufferObject.create()
        self.indexBufferObject.bind()
        self.indexBufferObject.setUsagePattern(QOpenGLBuffer.StaticDraw)
        self.indexBufferObject.allocate(self.indices, self.indices.nbytes)
        self.indexBufferObject.release()
        self.indexBufferObject.bind()

    def initVAO(self):
        # object
        self.VAO.create()
        self.VAO.bind()

    def enableAttributeArray(self, location):
        self.attributes.append(location)
        self.program.enableAttributeArray(location)

    def bindAttributes(self):
        color_offset = self.vertices[0].nbytes * self.vertex_elements
        stride = self.vertices[0].nbytes * self.vertex_elements * self.num_of_elements_in_vbo
        if self.num_of_elements_in_vbo == 1:
            self._program.setAttributeBuffer(0, GL.GL_FLOAT, 0, 3, 0)
        else:
            for i in self.attributes:
                if i == 0:
                    self._program.setAttributeBuffer(i, GL.GL_FLOAT, 0, 3, stride)
                else:
                    self._program.setAttributeBuffer(i, GL.GL_FLOAT, color_offset, 3, stride)

    def bind(self):
        self.program.bind()
        self.VAO.bind()

    def unbind(self):
        self.VAO.release()
        self.program.release()

    def setUniformValue(self, uniform, value):
        # print(uniform, value)
        self.program.setUniformValue(uniform, value)

    @property
    def program(self):
        return self._program

    @property
    def vertexBufferObject(self):
        return self._vertexBufferObject

    @property
    def VAO(self):
        return self._vertexArrayObject

    @property
    def vertices(self):
        return self._vertices

    @vertices.setter
    def vertices(self, vertices):
        self._vertices = vertices

    @property
    def indices(self):
        return self._indices

    @indices.setter
    def indices(self, indices):
        self._indices = indices

    @property
    def indexBufferObject(self):
        return self._indexesBufferObject


if __name__ == "__main__":
    program = GLProgram()