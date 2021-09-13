import sys
import glfw
import OpenGL.GL as gl
from pathlib import Path
from pyrr import Vector3, Matrix44

CURDIR = Path(__file__).absolute().parent
RESDIR = CURDIR.parent.parent.joinpath("resources")

sys.path.append(str(CURDIR.parent))
from model import Model
from shader import Shader
from camera import Camera, CameraMovement

# -- settings
SRC_WIDTH = 800
SRC_HEIGHT = 600

# -- camera
camera = Camera(Vector3([0.0, 0.0, 3.0]))
last_x = SRC_WIDTH / 2
last_y = SRC_HEIGHT / 2
first_mouse = True

# -- timing
delta_time = 0.0
last_frame = 0.0


def main():
    global delta_time, last_frame

    if not glfw.init():
        raise ValueError("Failed to initialize glfw")

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    window = glfw.create_window(SRC_WIDTH, SRC_HEIGHT, "learnOpenGL", None, None)
    if not window:
        glfw.terminate()
        raise ValueError("Failed to create window")

    glfw.make_context_current(window)
    glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)
    glfw.set_cursor_pos_callback(window, mouse_callback)
    glfw.set_scroll_callback(window, scroll_callback)

    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)

    gl.glEnable(gl.GL_DEPTH_TEST)

    model = Model(str(RESDIR.joinpath("objects/nanosuit/nanosuit.obj")))
    model_shader = Shader(str(CURDIR / "shaders/model_loading.vs"), str(CURDIR / "shaders/model_loading.fs"))
    # draw in wireframe
    # gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)
    # sys.exit()

    while not glfw.window_should_close(window):
        # -- time logic
        current_frame = glfw.get_time()
        delta_time = current_frame - last_frame
        last_frame = current_frame

        # -- input
        process_input(window)

        # -- render
        gl.glClearColor(0.05, 0.05, 0.05, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        model_shader.use()

        # -- view.projection transformations
        view = camera.get_view_matrix()
        projection = Matrix44.perspective_projection(
            camera.zoom, SRC_WIDTH/SRC_HEIGHT, 0.1, 100.0
        )
        model_shader.set_mat4("projection", projection)
        model_shader.set_mat4("view", view)

        # -- world transformation
        modelm = Matrix44.identity()
        modelm *= Matrix44.from_translation([0.0, -0.75, 0.0])
        modelm *= Matrix44.from_scale([0.2, 0.2, 0.2])
        model_shader.set_mat4("model", modelm)

        model.draw(model_shader)

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()


def process_input(window):
    if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
        glfw.set_window_should_close(window, True)

    if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
        camera.process_keyboard(CameraMovement.FORWARD, delta_time)
    if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
        camera.process_keyboard(CameraMovement.BACKWARD, delta_time)

    if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
        camera.process_keyboard(CameraMovement.LEFT, delta_time)
    if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
        camera.process_keyboard(CameraMovement.RIGHT, delta_time)


def framebuffer_size_callback(window, width, height):
    gl.glViewport(0, 0, width, height)


def mouse_callback(window, xpos, ypos):
    global first_mouse, last_x, last_y

    if first_mouse:
        last_x, last_y = xpos, ypos
        first_mouse = False

    xoffset = xpos - last_x
    yoffset = last_y - ypos  # XXX Note Reversed (y-coordinates go from bottom to top)
    last_x = xpos
    last_y = ypos

    camera.process_mouse_movement(xoffset, yoffset)


def scroll_callback(window, xoffset, yoffset):
    camera.process_mouse_scroll(yoffset)


if __name__ == '__main__':
    main()
