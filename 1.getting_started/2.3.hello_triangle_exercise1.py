import os
import sys
sys.path.append(os.pardir)

import window
import OpenGL.GL as gl
from OpenGL.GL import shaders
from ctypes import c_float, sizeof, c_void_p


class Window(window.Window):

    def setup(self):
        vertex_shader = """
        #version 330 core

        layout (location = 0) in vec3 aPos;

        void main() {
            gl_Position = vec4(aPos, 1.0);
        }
        """

        fragment_shader = """
        #version 330 core

        out vec4 FragColor;

        void main() {
            FragColor = vec4(1.0f, 0.5f, 0.2f, 1.0f);
        }
        """
        self.shader = shaders.compileProgram(
            shaders.compileShader(vertex_shader,    gl.GL_VERTEX_SHADER),
            shaders.compileShader(fragment_shader,  gl.GL_FRAGMENT_SHADER),
        )

        vertices = [
         # first triangle
         -0.9, -0.5, 0.0,  # left
         -0.0, -0.5, 0.0,  # right
         -0.45, 0.5, 0.0,  # top

         # second triangle
         0.0, -0.5, 0.0,  # left
         0.9, -0.5, 0.0,  # right
         0.45, 0.5, 0.0   # top
        ]
        vertices = (c_float * len(vertices))(*vertices)

        self.vao = gl.glGenVertexArrays(1)
        gl.glBindVertexArray(self.vao)

        vbo = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, sizeof(vertices), vertices, gl.GL_STATIC_DRAW)

        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 3 * sizeof(c_float), c_void_p(0))
        gl.glEnableVertexAttribArray(0)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)
        gl.glBindVertexArray(0)

    def on_draw(self, time, frame_time):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        gl.glClearColor(.2, .3, .3, 1)

        gl.glUseProgram(self.shader)
        gl.glBindVertexArray(self.vao)
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, 6)

    def on_resize(self, w, h):
        gl.glViewport(0, 0, w, h)


if __name__ == '__main__':
    win = Window(800, 600, "LearnOpenGL")
    win.show()
