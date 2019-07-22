import os
import sys
sys.path.append(os.pardir)

import window
import OpenGL.GL as gl


class Window(window.Window):

    def on_draw(self, time, frame_time):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        gl.glClearColor(.2, .3, .3, 1)


if __name__ == '__main__':
    win = Window(800, 600, "LearnOpenGL")
    win.show()
