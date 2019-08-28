import os
import sys
import math
import glfw
sys.path.append(os.pardir)

import window
import shader
import camera
import OpenGL.GL as gl
from PIL import Image
from camera import CameraMovement
from pyrr import Matrix44, matrix44, Vector3
from ctypes import c_float, sizeof, c_void_p

RESOURCES_DIR = os.path.join(os.path.abspath(os.pardir), 'resources')
get_texture = lambda filename : os.path.join(RESOURCES_DIR, 'textures', filename)


class Window(window.Window):

    def setup(self):

        self.camera = camera.Camera(position=Vector3([0.0, 0.0, 3.0]))
        self.first_mouse = True
        self.last_x = 800 / 2
        self.last_y = 300 / 2

        self.delta_time = 0.0
        self.last_frame = 0.0

        gl.glEnable(gl.GL_DEPTH_TEST)
        self.shader = shader.Shader('shaders/7.1.camera.vs', 'shaders/7.1.camera.fs')

        vertices = [
             # positions      tex_coords
            -0.5, -0.5, -0.5,  0.0, 0.0,
             0.5, -0.5, -0.5,  1.0, 0.0,
             0.5,  0.5, -0.5,  1.0, 1.0,
             0.5,  0.5, -0.5,  1.0, 1.0,
            -0.5,  0.5, -0.5,  0.0, 1.0,
            -0.5, -0.5, -0.5,  0.0, 0.0,

            -0.5, -0.5,  0.5,  0.0, 0.0,
             0.5, -0.5,  0.5,  1.0, 0.0,
             0.5,  0.5,  0.5,  1.0, 1.0,
             0.5,  0.5,  0.5,  1.0, 1.0,
            -0.5,  0.5,  0.5,  0.0, 1.0,
            -0.5, -0.5,  0.5,  0.0, 0.0,

            -0.5,  0.5,  0.5,  1.0, 0.0,
            -0.5,  0.5, -0.5,  1.0, 1.0,
            -0.5, -0.5, -0.5,  0.0, 1.0,
            -0.5, -0.5, -0.5,  0.0, 1.0,
            -0.5, -0.5,  0.5,  0.0, 0.0,
            -0.5,  0.5,  0.5,  1.0, 0.0,

             0.5,  0.5,  0.5,  1.0, 0.0,
             0.5,  0.5, -0.5,  1.0, 1.0,
             0.5, -0.5, -0.5,  0.0, 1.0,
             0.5, -0.5, -0.5,  0.0, 1.0,
             0.5, -0.5,  0.5,  0.0, 0.0,
             0.5,  0.5,  0.5,  1.0, 0.0,

            -0.5, -0.5, -0.5,  0.0, 1.0,
             0.5, -0.5, -0.5,  1.0, 1.0,
             0.5, -0.5,  0.5,  1.0, 0.0,
             0.5, -0.5,  0.5,  1.0, 0.0,
            -0.5, -0.5,  0.5,  0.0, 0.0,
            -0.5, -0.5, -0.5,  0.0, 1.0,

            -0.5,  0.5, -0.5,  0.0, 1.0,
             0.5,  0.5, -0.5,  1.0, 1.0,
             0.5,  0.5,  0.5,  1.0, 0.0,
             0.5,  0.5,  0.5,  1.0, 0.0,
            -0.5,  0.5,  0.5,  0.0, 0.0,
            -0.5,  0.5, -0.5,  0.0, 1.0
        ]
        vertices = (c_float * len(vertices))(*vertices)

        self.cube_positions = [
            ( 0.0,  0.0,  0.0),
            ( 2.0,  5.0, -15.0),
            (-1.5, -2.2, -2.5),
            (-3.8, -2.0, -12.3),
            ( 2.4, -0.4, -3.5),
            (-1.7,  3.0, -7.5),
            ( 1.3, -2.0, -2.5),
            ( 1.5,  2.0, -2.5),
            ( 1.5,  0.2, -1.5),
            (-1.3,  1.0, -1.5)
        ]

        self.vao = gl.glGenVertexArrays(1)
        gl.glBindVertexArray(self.vao)

        vbo = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, sizeof(vertices), vertices, gl.GL_STATIC_DRAW)

        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 5 * sizeof(c_float), c_void_p(0))
        gl.glEnableVertexAttribArray(0)

        gl.glVertexAttribPointer(1, 2, gl.GL_FLOAT, gl.GL_FALSE, 5 * sizeof(c_float), c_void_p(3 * sizeof(c_float)))
        gl.glEnableVertexAttribArray(1)

        # -- load texture 1
        self.texture1 = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.texture1)
        # -- texture wrapping
        gl.glTexParameter(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_REPEAT)
        gl.glTexParameter(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_REPEAT)
        # -- texture filterting
        gl.glTexParameter(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
        gl.glTexParameter(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)

        img = Image.open(get_texture('container.jpg')).transpose(Image.FLIP_TOP_BOTTOM)
        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGB, img.width, img.height, 0, gl.GL_RGB, gl.GL_UNSIGNED_BYTE, img.tobytes())
        gl.glGenerateMipmap(gl.GL_TEXTURE_2D)

        # -- load texture 2
        self.texture2 = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.texture2)
        # -- texture wrapping
        gl.glTexParameter(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_REPEAT)
        gl.glTexParameter(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_REPEAT)
        # -- texture filterting
        gl.glTexParameter(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
        gl.glTexParameter(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)

        img = Image.open(get_texture('awesomeface.png')).transpose(Image.FLIP_TOP_BOTTOM)
        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGB, img.width, img.height, 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, img.tobytes())
        gl.glGenerateMipmap(gl.GL_TEXTURE_2D)

        self.shader.use()
        self.shader.set_int("texture1", 0)
        self.shader.set_int("texture2", 1)

    def on_draw(self, time, frame_time):
        current_frame = glfw.get_time()
        self.delta_time = current_frame - self.last_frame
        self.last_frame = current_frame

        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glClearColor(.2, .3, .3, 1)

        gl.glActiveTexture(gl.GL_TEXTURE0)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.texture1)
        gl.glActiveTexture(gl.GL_TEXTURE1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.texture2)

        self.shader.use()

        projection = Matrix44.perspective_projection(self.camera.zoom, self.width/self.height, 0.1, 100.0)
        self.shader.set_mat4('projection', projection)

        view = self.camera.get_view_matrix()
        self.shader.set_mat4('view', view)

        gl.glBindVertexArray(self.vao)
        for idx, position in enumerate(self.cube_positions):
            angle = 20.0 * idx
            rotation = matrix44.create_from_axis_rotation([1.0, 0.3, 0.5], math.radians(angle))
            translation = Matrix44.from_translation(position)
            model = translation * rotation
            self.shader.set_mat4('model', model)
            gl.glDrawArrays(gl.GL_TRIANGLES, 0, 36)

    def on_resize(self, w, h):
        gl.glViewport(0, 0, w, h)

    def on_input(self, window):

        if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
            self.camera.process_keyboard(CameraMovement.FORWARD, self.delta_time)
        if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
            self.camera.process_keyboard(CameraMovement.BACKWARD, self.delta_time)

        if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
            self.camera.process_keyboard(CameraMovement.LEFT, self.delta_time)
        if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
            self.camera.process_keyboard(CameraMovement.RIGHT, self.delta_time)

    def on_mouse_scroll(self, dx, dy):
        self.camera.process_mouse_scroll(dy)

    def on_mouse_event(self, xpos, ypos):
        if self.first_mouse:
            self.last_x, self.last_y = xpos, ypos
            self.first_mouse = False

        xoffset = xpos - self.last_x
        yoffset = self.last_y - ypos  # XXX Note Reversed (y-coordinates go from bottom to top)
        self.last_x = xpos
        self.last_y = ypos

        self.camera.process_mouse_movement(xoffset, yoffset)


if __name__ == '__main__':
    # XXX Note cursor=False (tells GLFW to capture our mouse)
    win = Window(800, 600, "LearnOpenGL", cursor=False)
    win.show()
