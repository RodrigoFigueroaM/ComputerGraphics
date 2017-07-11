#! /usr/bin/env python
from PyQt5.QtGui import QVector3D, QVector2D


def ObjectLoader(fileName = None):
    vertices = []
    uvs = []
    normals = []
    faces = []
    file = open(fileName, "r")
    data = file.readlines()
    file.close()
    for line in data:
        values = line.split()
        if len(values) > 0:
            if values[0] == 'v':
                vertex = QVector3D(float(values[1]), float(values[2]),float(values[3]))
                vertices.append(vertex)
            elif values[0] == 'vn':
                normal = QVector3D(float(values[1]), float(values[2]), float(values[3]))
                normals.append(normal)
            elif values[0] == 'vt':
                texture = QVector2D(float(values[1]), float(values[2]))
                uvs.append(texture)
            elif values[0] == 'f':
                faces.append(values[1])
                faces.append(values[2])
                faces.append(values[3])
            else:
                pass
    # print(faces[9*3])
    triangleVerticesIndex, trianglesTextureIndex, trianglesNormalIndex = parseFaces(faces)

    print('triangleVerticesIndex', triangleVerticesIndex)

    print('trianglesNormalIndex',trianglesTextureIndex)

    textureCoords = [0 for i in range(0,len(trianglesTextureIndex))]
    for coord in trianglesTextureIndex:
        textureCoords[coord] = uvs[coord]
    # triangles = []
    # for i in range(0,len(triangleVerticesIndex) //3):
    #     triangles.append(vertices[triangleVerticesIndex[i*3]])
    #     triangles.append(vertices[triangleVerticesIndex[i * 3 + 1]])
    #     triangles.append(vertices[triangleVerticesIndex[i * 3 + 2]])

    # vertexNormals = []
    # for index in trianglesNormalIndex:
        # vertexNormals.append(normals[index])
    # print(correctedDrawingIndices)
    # print(triangleVertices[9*3], triangleVertices[9*3 + 1], triangleVertices[9*3 + 2])
    # print(vertices[triangleVertices[9*3] - 1 ], vertices[triangleVertices[9*3 + 1] - 1 ], vertices[triangleVertices[9*3 + 2] - 1])
    # print(triangles[27], triangles[28], triangles[29])

    return vertices, triangleVerticesIndex, textureCoords, normals

def parseFaces(facesList):
    trianglesIndex = []
    trianglesNormalIndex = []
    trianglesTextureIndex = []
    for face in facesList:
        values = face.split('/')
        trianglesIndex.append(int(values[0]) - 1)
        trianglesTextureIndex.append(int(values[1]) - 1)
        trianglesNormalIndex.append(int(values[2]) - 1)
    return trianglesIndex, trianglesTextureIndex, trianglesNormalIndex


if __name__ == "__main__":
    objLoader = ObjectLoader("./objs/Cube.obj")
    # drawingVertices = objLoader[0]
    # drawingIndices = objLoader[1]
    # drawingNormals = objLoader[3]
    #
    # print(len(drawingVertices), len(drawingIndices), len(drawingNormals))
    # print(drawingVertices)
    # print(drawingNormals)
    # print((drawingIndices))
    # print()
    # print(drawingVertices[4])
    # print(drawingVertices[0])
    # print(drawingVertices[3])
    #
    # print(drawingNormals[0])
    # print(drawingNormals[0])
    # print(drawingNormals[0])