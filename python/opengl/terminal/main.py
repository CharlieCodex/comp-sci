import numpy as np
import ModernGL
from PyQt5 import QtOpenGL, QtWidgets, QtCore
import utils


class QGLControllerWidget(QtOpenGL.QGLWidget):
    def __init__(self):
        fmt = QtOpenGL.QGLFormat()
        fmt.setVersion(3, 3)
        fmt.setProfile(QtOpenGL.QGLFormat.CoreProfile)
        super().__init__(fmt, None)

    def initializeGL(self):
        self.ctx = ModernGL.create_context()
        prog = utils.create_program_from_file(self.ctx, 'shaders.json')
        pts = np.array((-0.5, -0.5,
                        0.0, 0.8,
                        0.5, -0.5)).astype(np.float32)
        self.vbo = self.ctx.buffer(pts.tobytes())
        self.vao = self.ctx.simple_vertex_array(prog,
                                                self.vbo,
                                                ['vert'])
        self.clear_gray = 0.9
        self.n = 0

    def paintGL(self):
        self.n += 1
        self.ctx.viewport = (0, 0, self.width() * 2, self.height() * 2)
        self.vao.render()
        self.ctx.finish()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = QGLControllerWidget()
    window.resize(2560, 1600)
    window.showNormal()
    timer = QtCore.QTimer()
    timer.timeout.connect(window.update)
    timer.start(0)
    app.exec_()
