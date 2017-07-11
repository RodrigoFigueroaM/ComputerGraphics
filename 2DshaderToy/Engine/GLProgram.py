from PyQt5.QtGui import QOpenGLShader, QOpenGLShaderProgram, QOpenGLBuffer, QOpenGLVertexArrayObject, QOpenGLTexture, QImage
import OpenGL.GL as GL


class GLProgram:
    def __init__(self, context, numAttibutesInvbo = 1):
        super(GLProgram, self).__init__()
        self._fakeTimer = 0
        self.num_of_elements_in_vbo = numAttibutesInvbo
        self.vertex_elements = 3
        self._program = QOpenGLShaderProgram(context)
        self._textures = []
        self._images = []
        self._vertexBufferObject = QOpenGLBuffer(QOpenGLBuffer.VertexBuffer)
        self._indexesBufferObject = QOpenGLBuffer(QOpenGLBuffer.IndexBuffer)
        self._vertexArrayObject = QOpenGLVertexArrayObject()
        self._vertices = []
        self._indices = []
        self.attributes = []

    def addTexture(self, imgfile):
        self._images.append(QImage(imgfile).mirrored())
        self._textures.append(QOpenGLTexture(QOpenGLTexture.Target2D))


    def initProgram(self, vertFile, fragFile, vertices, indices, attribs):
        for texture, image in zip(self._textures, self._images):
            self.initTexture(texture, image)
        self.num_of_elements_in_vbo = len(attribs)
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

    def initTexture(self, texture, image):
        texture.create()
        texture.setFormat(QOpenGLTexture.RGBA8_UNorm)
        texture.setSize(256, 256)
        texture.setMinificationFilter(QOpenGLTexture.Linear)
        texture.setMagnificationFilter(QOpenGLTexture.Linear)
        texture.setWrapMode(QOpenGLTexture.Repeat)
        texture.setData(image, QOpenGLTexture.DontGenerateMipMaps)
        texture.allocateStorage()
        texture.bind()

    def releaseBuffersAndProgram(self):
        self.VAO.release()
        self.vertexBufferObject.release()
        self.indexBufferObject.release()
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
        normal_offset = self.vertices[0].nbytes * 5
        tex_offset = self.vertices[0].nbytes * 3
        stride = self.vertices[0].nbytes * 8
        self._program.setAttributeBuffer(0, GL.GL_FLOAT, 0, 3, stride)
        self._program.setAttributeBuffer(1, GL.GL_FLOAT, tex_offset, 2, stride)
        self._program.setAttributeBuffer(2, GL.GL_FLOAT, normal_offset, 3, stride)

    def bind(self):
        self.program.bind()
        for texture in self._textures:
            texture.bind()
        self.VAO.bind()

    def unbind(self):
        self.VAO.release()
        for texture in self._textures:
            texture.release()
        self.program.release()

    def setUniformValue(self, uniform, value):
        # print(uniform, value)
        self.program.setUniformValue(uniform, value)

    def bindTimer(self):
        self.program.setUniformValue('time', float(self.timer))
        self._fakeTimer += 0.001

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

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, filename):
        print(filename)
        self._image.load(filename)
        self._image = self.image.mirrored()

    @property
    def timer(self):
        return self._fakeTimer


if __name__ == "__main__":
    program = GLProgram()