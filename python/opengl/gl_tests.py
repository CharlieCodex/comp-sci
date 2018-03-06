import numpy as np
import ModernGL
from PyQt5 import QtOpenGL, QtWidgets, QtCore
from cl_utils import init_cl, compute_n
import time


def translation_mat(x, y, z=0):
    return ((1, 0, 0, x),
            (0, 1, 0, y),
            (0, 0, 1, z),
            (0, 0, 0, 1),)


def window_transformation(win_x, win_y, win_w, win_h):
    translation = np.array(translation_mat(-win_x, -win_y))
    scale = np.array(
                    ((1 / win_w, 0, 0, 0),
                     (0, 1 / win_h, 0, 0),
                     (0, 0, 1, 0),
                     (0, 0, 0, 1)))
    return np.matmul(scale, translation).flatten()


class QGLControllerWidget(QtOpenGL.QGLWidget):
    def __init__(self):
        fmt = QtOpenGL.QGLFormat()
        fmt.setVersion(3, 3)
        fmt.setProfile(QtOpenGL.QGLFormat.CoreProfile)
        super().__init__(fmt, None)
        pts = np.random.rand(2, 100000).astype(np.float32) * 20 - 10
        self.x, self.y = pts

    def initializeGL(self):
        self.ctx = ModernGL.create_context()
        self.ctx.enable(ModernGL.BLEND)
        prog = self.ctx.program([
            self.ctx.vertex_shader('''
                    #version 330
                    in vec2 vert;
                    uniform mat4 transformation;
                    uniform vec2 offset;
                    void main() {
                        vec4 tmp = transformation * vec4(vert+offset, 0, 1.0);
                        gl_Position = tmp;
                    }
            '''),
            self.ctx.fragment_shader('''
                    #version 330
                    out vec4 color;
                    void main() {
                            color = vec4(1.0, 1.0, 1.0, 0.01);
                    }
            '''),
        ])
        buf_size = self.x.nbytes + self.y.nbytes
        self.vbo = self.ctx.buffer(reserve=buf_size)
        self.win_x = 0
        self.win_y = 0
        self.win_size = 50
        self.vao = self.ctx.simple_vertex_array(prog,
                                                self.vbo,
                                                ['vert'])
        self.update_window()
        self.clear_gray = 0.9
        self.n = 0
        self.clear = False
        init_cl()

    def update_window(self):
        print('window updated')
        self.vao.program.uniforms['transformation'].write(
            np.array((1 / self.win_size, 0, 0, 0,
                      0, 1 / self.win_size * 2560 / 1600, 0, 0,
                      0, 0, 1, 0,
                      0, 0, 0, 1)).astype(np.float32)
        )
        self.vao.program.uniforms['offset'].write(
            np.array((self.win_x, self.win_y)).astype(np.float32)
        )
        self.clear = True

    def paintGL(self):
        self.n += 1
        self.ctx.viewport = (0, 0, self.width() * 2, self.height() * 2)
        if self.clear:
            self.clear = False
            print('cleared')
        st = time.time()
        x, y = compute_n(self.x, self.y, 10)
        et1 = time.time()
        pts = np.column_stack((x, y)).astype(np.float32)
        self.vbo.write(pts.tobytes())
        self.vao.render(ModernGL.POINTS)
        et2 = time.time()
        print('Compute: ', (et1 - st) * 1000)
        print('Render: ', (et2 - et1) * 1000)
        print('Depth: ', self.n)
        self.x, self.y = x, y
        self.vbo.orphan()

    def keyPressEvent(self, e):
        key = e.key()
        if key == QtCore.Qt.Key_1:
            self.win_size *= 1.1
            self.update_window()
        elif key == QtCore.Qt.Key_2:
            self.win_size /= 1.1
            self.update_window()


app = QtWidgets.QApplication([])
window = QGLControllerWidget()
window.resize(2560, 1280)
window.showFullScreen()
timer = QtCore.QTimer()
timer.timeout.connect(window.update)
timer.start(0)
app.exec_()
