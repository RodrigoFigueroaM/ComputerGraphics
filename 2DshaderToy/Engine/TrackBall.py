import math

from PyQt5.QtGui import (QVector3D, QQuaternion)

from Engine.Camera import Camera

# //assuming IEEE-754(GLfloat), which i believe has max precision of 7 bits
EPSILON = 1.0e-5


class TrackBall:
    def __init__(self):
        super(TrackBall, self).__init__()
        self._target = QVector3D(0, 0, 0)
        self._lastPos = QVector3D()
        self._currentPos = QVector3D()
        self._axis = QVector3D(0, 1, 0)
        self.angle = 0

    def __str__(self):
        return 'Target @: {}\nlastPos @: {}\ncurrentPos @:{}\n'.format(self._target, self.lastPos, self.currentPos)

    def mapToSphere(self, x, y, width, height):
        x, y, z = Camera.devicePortCoordinates(x, y, width, height)
        length = QVector3D.dotProduct(QVector3D(x, y, 0), QVector3D(x, y, 0))
        z = 0
        if length <= 1.0:
            z = math.sqrt(1.0 - length)  # 1.0 is teh radius of the ball
            pos = QVector3D(-x, y, z)
        else:
            pos = QVector3D(-x, y, z).normalized()
        return pos

    def clicked(self, x, y, width, height):
        self.lastPos = self.mapToSphere(x, y, width, height)

    def move(self, x, y, width, height):
        self.currentPos = self.mapToSphere(x, y, width, height)
        self._axis = QVector3D.crossProduct(self.lastPos, self.currentPos)
        length = math.sqrt(QVector3D.dotProduct(self.axis, self.axis))
        self.angle = QVector3D.dotProduct(self.lastPos, self.currentPos)
        self.lastPos = self.currentPos
        if length > EPSILON:
            return QQuaternion.fromAxisAndAngle(self._axis, self.angle)
        return QQuaternion.fromAxisAndAngle(0, 0, 0, 0)

    @property
    def axis(self):
        return self._axis

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, target):
        self._target = target

    @property
    def lastPos(self):
        return self._lastPos

    @lastPos.setter
    def lastPos(self, lastPos):
        self._lastPos = lastPos

    @property
    def currentPos(self):
        return self._currentPos

    @currentPos.setter
    def currentPos(self, currentPos):
        self._currentPos = currentPos

if __name__ == '__main__':
    tb = TrackBall()
    print(tb)
    tb.clicked(100, 200, 250, 500)
    tb.move(150, 220, 250, 500)
    print(tb.move(0, 6, 250, 500))
    tb.clicked(100, 200, 250, 500)
    tb.move(5, 6, 250, 500)
    print(tb.move(0, 6, 250, 500).scalar())







