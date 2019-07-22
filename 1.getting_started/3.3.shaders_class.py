import os
import sys
sys.path.append(os.pardir)

import window
import shader
import OpenGL.GL as gl
from ctypes import c_float, sizeof, c_void_p


class Window(window.Window):

    def setup(self):
        self.shader = shader.Shader('shaders/3.3.shader.vs', 'shaders/3.3.shader.fs')

        data = [
            -0.5, -0.5, 0.0, 1.0, 0.0, 0.0,
             0.5, -0.5, 0.0, 0.0, 1.0, 0.0,
             0.0,  0.5, 0.0, 0.0, 0.0, 1.0,
        ]
        data = (c_float * len(data))(*data)

        self.vao = gl.glGenVertexArrays(1)
        gl.glBindVertexArray(self.vao)

        vbo = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, sizeof(data), data, gl.GL_STATIC_DRAW)

        # -- vertices
        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 6 * sizeof(c_float), c_void_p(0))
        gl.glEnableVertexAttribArray(0)

        # -- color
        gl.glVertexAttribPointer(1, 3, gl.GL_FLOAT, gl.GL_FALSE, 6 * sizeof(c_float), c_void_p(3 * sizeof(c_float)))
        gl.glEnableVertexAttribArray(1)

    def on_draw(self, time, frame_time):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        gl.glClearColor(.2, .3, .3, 1)

        self.shader.use()
        gl.glBindVertexArray(self.vao)
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, 3)

    def on_resize(self, w, h):
        gl.glViewport(0, 0, w, h)


if __name__ == '__main__':
    win = Window(800, 600, "LearnOpenGL")
    win.show()
