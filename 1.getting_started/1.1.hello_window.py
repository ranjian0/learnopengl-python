import os
import sys
sys.path.append(os.pardir)

import window


class Window(window.Window):
    pass


if __name__ == '__main__':
    win = Window(800, 600, "LearnOpenGL")
    win.show()
