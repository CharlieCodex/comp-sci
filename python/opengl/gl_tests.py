import struct
import numpy as np
import ModernGL
from PyQt5 import QtOpenGL, QtWidgets
from cl_utils import init_cl, compute_n
import time


def translation_mat(x, y, z=0):
    return (1, 0, 0, x,
            0, 1, 0, y,
            0, 0, 1, z,
            0, 0, 0, 1)


def window_transformation(win_x, win_y, win_w, win_h):
    translation = np.array(translation_mat(-win_x, -win_y))
    translation.resize(4, 4)
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
                fmt.setSampleBuffers(True)
                super(QGLControllerWidget, self).__init__(fmt, None)
                pts = np.random.rand(2, 1000).astype(np.float32) * 10 - 5
                self.x, self.y = pts

        def initializeGL(self):
                self.ctx = ModernGL.create_context()

                prog = self.ctx.program([
                    self.ctx.vertex_shader('''
                            #version 330
                            in vec2 vert;
                            uniform mat4 transformation;
                            void main() {
                                vec4 tmp = transformation * vec4(vert, 0, 1.0);
                                gl_Position = tmp;
                            }
                    '''),
                    self.ctx.fragment_shader('''
                            #version 330
                            out vec4 color;
                            void main() {
                                    color = vec4(1.0, 0.5, 1.0, 1.0);
                            }
                    '''),
                ])
                buf_size = self.x.nbytes + self.y.nbytes
                self.vbo = self.ctx.buffer(reserve=buf_size)
                mat = window_transformation(0, 0, 10, 10 / 2560 * 1600)
                prog.uniforms['transformation'].value = tuple(mat)
                self.vao = self.ctx.simple_vertex_array(prog,
                                                        self.vbo,
                                                        ['vert'])
                init_cl()

        def paintGL(self):
            st = time.time()
            self.x, self.y = compute_n(self.x, self.y, 10)
            et1 = time.time()
            self.ctx.viewport = (0, 0, self.width() * 2, self.height() * 2)
            self.ctx.clear(0.1, 0.1, 0.1)
            pts = np.column_stack((self.x, self.y)).astype(np.float32)
            self.vbo.orphan()
            self.vbo.write(pts.tobytes())
            self.vao.render(ModernGL.POINTS)
            et2 = time.time()
            print('Compute: ', (et1 - st) * 1000)
            print('Render: ', (et2 - et1) * 1000)


app = QtWidgets.QApplication([])
window = QGLControllerWidget()
window.resize(2560, 1280)
window.showFullScreen()
app.exec_()
