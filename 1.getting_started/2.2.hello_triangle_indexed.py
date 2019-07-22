import os
import sys
sys.path.append(os.pardir)

import window
import OpenGL.GL as gl
from OpenGL.GL import shaders
from ctypes import c_uint, c_float, sizeof, c_void_p


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
         0.5,  0.5, 0.0,  # top right
         0.5, -0.5, 0.0,  # bottom right
        -0.5, -0.5, 0.0,  # bottom left
        -0.5,  0.5, 0.0   # top left
        ]
        vertices = (c_float * len(vertices))(*vertices)

        indices = [
            0, 1, 3,
            1, 2, 3
        ]
        indices = (c_uint * len(indices))(*indices)

        self.vao = gl.glGenVertexArrays(1)
        gl.glBindVertexArray(self.vao)

        vbo = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, sizeof(vertices), vertices, gl.GL_STATIC_DRAW)

        ebo = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, ebo)
        gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, sizeof(indices), indices, gl.GL_STATIC_DRAW)

        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 3 * sizeof(c_float), c_void_p(0))
        gl.glEnableVertexAttribArray(0)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)
        gl.glBindVertexArray(0)

        # -- uncomment to draw wireframe
        # gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)

    def on_draw(self, time, frame_time):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        gl.glClearColor(.2, .3, .3, 1)

        gl.glUseProgram(self.shader)
        gl.glBindVertexArray(self.vao)
        gl.glDrawElements(gl.GL_TRIANGLES, 6, gl.GL_UNSIGNED_INT, c_void_p(0))

    def on_resize(self, w, h):
        gl.glViewport(0, 0, w, h)


if __name__ == '__main__':
    win = Window(800, 600, "LearnOpenGL")
    win.show()
