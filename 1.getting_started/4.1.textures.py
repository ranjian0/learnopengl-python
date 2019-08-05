import os
import sys
sys.path.append(os.pardir)

import window
import shader
import OpenGL.GL as gl
from PIL import Image
from ctypes import c_uint, c_uint8, c_float, sizeof, c_void_p

RESOURCES_DIR = os.path.join(os.path.abspath(os.pardir), 'resources')
get_texture = lambda filename : os.path.join(RESOURCES_DIR, 'textures', filename)


class Window(window.Window):

    def setup(self):
        self.shader = shader.Shader('shaders/4.1.texture.vs', 'shaders/4.1.texture.fs')
        self.shader_mix = shader.Shader('shaders/4.1.texture.vs', 'shaders/4.1.texture_mix.fs')

        vertices = [
         # positions         colors          tex_coords
         0.5,  0.5, 0.0,  1.0, 0.0, 0.0,  1.0, 1.0,  # top right
         0.5, -0.5, 0.0,  0.0, 1.0, 0.0,  1.0, 0.0,  # bottom right
        -0.5, -0.5, 0.0,  0.0, 0.0, 1.0,  0.0, 0.0,  # bottom left
        -0.5,  0.5, 0.0,  1.0, 1.0, 0.0,  0.0, 1.0,  # top left
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

        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 8 * sizeof(c_float), c_void_p(0))
        gl.glEnableVertexAttribArray(0)

        gl.glVertexAttribPointer(1, 3, gl.GL_FLOAT, gl.GL_FALSE, 8 * sizeof(c_float), c_void_p(3 * sizeof(c_float)))
        gl.glEnableVertexAttribArray(1)

        gl.glVertexAttribPointer(2, 2, gl.GL_FLOAT, gl.GL_FALSE, 8 * sizeof(c_float), c_void_p(6 * sizeof(c_float)))
        gl.glEnableVertexAttribArray(2)

        # -- load texture
        self.texture = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.texture)
        # -- texture wrapping
        gl.glTexParameter(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_REPEAT)
        gl.glTexParameter(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_REPEAT)
        # -- texture filterting
        gl.glTexParameter(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
        gl.glTexParameter(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)

        img = Image.open(get_texture('container.jpg'))
        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGB, img.width, img.height, 0, gl.GL_RGB, gl.GL_UNSIGNED_BYTE, img.tobytes())
        gl.glGenerateMipmap(gl.GL_TEXTURE_2D)

    def on_draw(self, time, frame_time):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        gl.glClearColor(.2, .3, .3, 1)

        gl.glBindTexture(gl.GL_TEXTURE_2D, self.texture)
        self.shader.use()
        # -- uncomment to see mixture of vertex color and texture color
        # self.shader_mix.use()
        gl.glBindVertexArray(self.vao)
        gl.glDrawElements(gl.GL_TRIANGLES, 6, gl.GL_UNSIGNED_INT, c_void_p(0))

    def on_resize(self, w, h):
        gl.glViewport(0, 0, w, h)


if __name__ == '__main__':
    win = Window(800, 600, "LearnOpenGL")
    win.show()
