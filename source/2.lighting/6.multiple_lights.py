import sys
import math
import glfw
import OpenGL.GL as gl
from pathlib import Path
from pyrr import Vector3, Matrix44, matrix44
from ctypes import c_float, sizeof, c_void_p

CURDIR = Path(__file__).parent.absolute()
sys.path.append(str(CURDIR.parent))

from shader import Shader
from camera import Camera, CameraMovement
from texture import load_texture

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

    glfw.init()
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

    lamp_shader = Shader(CURDIR / "shaders/1.lamp.vs", CURDIR / "shaders/1.lamp.fs")
    lighting_shader = Shader(CURDIR / "shaders/6.multiple_lights.vs", CURDIR / "shaders/6.multiple_lights.fs")

    vertices = [
        # positions        normals           texture coords
        -0.5, -0.5, -0.5,  0.0,  0.0, -1.0,  0.0,  0.0,
         0.5, -0.5, -0.5,  0.0,  0.0, -1.0,  1.0,  0.0,
         0.5,  0.5, -0.5,  0.0,  0.0, -1.0,  1.0,  1.0,
         0.5,  0.5, -0.5,  0.0,  0.0, -1.0,  1.0,  1.0,
        -0.5,  0.5, -0.5,  0.0,  0.0, -1.0,  0.0,  1.0,
        -0.5, -0.5, -0.5,  0.0,  0.0, -1.0,  0.0,  0.0,

        -0.5, -0.5,  0.5,  0.0,  0.0,  1.0,  0.0,  0.0,
         0.5, -0.5,  0.5,  0.0,  0.0,  1.0,  1.0,  0.0,
         0.5,  0.5,  0.5,  0.0,  0.0,  1.0,  1.0,  1.0,
         0.5,  0.5,  0.5,  0.0,  0.0,  1.0,  1.0,  1.0,
        -0.5,  0.5,  0.5,  0.0,  0.0,  1.0,  0.0,  1.0,
        -0.5, -0.5,  0.5,  0.0,  0.0,  1.0,  0.0,  0.0,

        -0.5,  0.5,  0.5, -1.0,  0.0,  0.0,  1.0,  0.0,
        -0.5,  0.5, -0.5, -1.0,  0.0,  0.0,  1.0,  1.0,
        -0.5, -0.5, -0.5, -1.0,  0.0,  0.0,  0.0,  1.0,
        -0.5, -0.5, -0.5, -1.0,  0.0,  0.0,  0.0,  1.0,
        -0.5, -0.5,  0.5, -1.0,  0.0,  0.0,  0.0,  0.0,
        -0.5,  0.5,  0.5, -1.0,  0.0,  0.0,  1.0,  0.0,

         0.5,  0.5,  0.5,  1.0,  0.0,  0.0,  1.0,  0.0,
         0.5,  0.5, -0.5,  1.0,  0.0,  0.0,  1.0,  1.0,
         0.5, -0.5, -0.5,  1.0,  0.0,  0.0,  0.0,  1.0,
         0.5, -0.5, -0.5,  1.0,  0.0,  0.0,  0.0,  1.0,
         0.5, -0.5,  0.5,  1.0,  0.0,  0.0,  0.0,  0.0,
         0.5,  0.5,  0.5,  1.0,  0.0,  0.0,  1.0,  0.0,

        -0.5, -0.5, -0.5,  0.0, -1.0,  0.0,  0.0,  1.0,
         0.5, -0.5, -0.5,  0.0, -1.0,  0.0,  1.0,  1.0,
         0.5, -0.5,  0.5,  0.0, -1.0,  0.0,  1.0,  0.0,
         0.5, -0.5,  0.5,  0.0, -1.0,  0.0,  1.0,  0.0,
        -0.5, -0.5,  0.5,  0.0, -1.0,  0.0,  0.0,  0.0,
        -0.5, -0.5, -0.5,  0.0, -1.0,  0.0,  0.0,  1.0,

        -0.5,  0.5, -0.5,  0.0,  1.0,  0.0,  0.0,  1.0,
         0.5,  0.5, -0.5,  0.0,  1.0,  0.0,  1.0,  1.0,
         0.5,  0.5,  0.5,  0.0,  1.0,  0.0,  1.0,  0.0,
         0.5,  0.5,  0.5,  0.0,  1.0,  0.0,  1.0,  0.0,
        -0.5,  0.5,  0.5,  0.0,  1.0,  0.0,  0.0,  0.0,
        -0.5,  0.5, -0.5,  0.0,  1.0,  0.0,  0.0,  1.0
    ]
    vertices = (c_float * len(vertices))(*vertices)

    cube_positions = [
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

    point_light_positions = [
        ( 0.7,  0.2,  2.0),
        ( 2.3, -3.3, -4.0),
        (-4.0,  2.0, -12.0),
        ( 0.0,  0.0, -3.0),
    ]

    cube_vao = gl.glGenVertexArrays(1)
    vbo = gl.glGenBuffers(1)

    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)
    gl.glBufferData(gl.GL_ARRAY_BUFFER, sizeof(vertices), vertices, gl.GL_STATIC_DRAW)

    gl.glBindVertexArray(cube_vao)

    # -- position attribute
    gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 8 * sizeof(c_float), c_void_p(0))
    gl.glEnableVertexAttribArray(0)
    # -- normal attribute
    gl.glVertexAttribPointer(1, 3, gl.GL_FLOAT, gl.GL_FALSE, 8 * sizeof(c_float), c_void_p(3 * sizeof(c_float)))
    gl.glEnableVertexAttribArray(1)
    # -- texture coordinate
    gl.glVertexAttribPointer(2, 2, gl.GL_FLOAT, gl.GL_FALSE, 8 * sizeof(c_float), c_void_p(6 * sizeof(c_float)))
    gl.glEnableVertexAttribArray(2)

    # -- second configure light vao (vbo is the same)
    light_vao = gl.glGenVertexArrays(1)
    gl.glBindVertexArray(light_vao)

    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)
    gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 8 * sizeof(c_float), c_void_p(0))
    gl.glEnableVertexAttribArray(0)

    # -- load texture
    diffuse_map = load_texture("container2.png")
    specular_map = load_texture("container2_specular.png")

    # -- shader configuration
    lighting_shader.use()
    lighting_shader.set_int("material.diffuse", 0)
    lighting_shader.set_int("material.specular", 1)

    while not glfw.window_should_close(window):
        # -- time logic
        current_frame = glfw.get_time()
        delta_time = current_frame - last_frame
        last_frame = current_frame

        # -- input
        process_input(window)

        # -- render
        gl.glClearColor(0.1, 0.1, 0.1, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        lighting_shader.use()
        lighting_shader.set_vec3("viewPos", camera.position)
        lighting_shader.set_float("material.shininess", 32.0)

        # -- directional light
        lighting_shader.set_vec3("dirLight.direction", [-0.2, -1.0, -0.3])
        lighting_shader.set_vec3("dirLight.ambient", [0.05, 0.05, 0.05])
        lighting_shader.set_vec3("dirLight.diffuse", [0.4, 0.4, 0.4])
        lighting_shader.set_vec3("dirLight.specular", [0.5, 0.5, 0.5])
        # -- point light 1
        lighting_shader.set_vec3("pointLights[0].position", point_light_positions[0])
        lighting_shader.set_vec3("pointLights[0].ambient", [0.05, 0.05, 0.05])
        lighting_shader.set_vec3("pointLights[0].diffuse", [0.8, 0.8, 0.8])
        lighting_shader.set_vec3("pointLights[0].specular", [1.0, 1.0, 1.0])
        lighting_shader.set_float("pointLights[0].constant", 1.0)
        lighting_shader.set_float("pointLights[0].linear", 0.09)
        lighting_shader.set_float("pointLights[0].quadratic", 0.032)
        # -- point light 2
        lighting_shader.set_vec3("pointLights[1].position", point_light_positions[1])
        lighting_shader.set_vec3("pointLights[1].ambient", [0.05, 0.05, 0.05])
        lighting_shader.set_vec3("pointLights[1].diffuse", [0.8, 0.8, 0.8])
        lighting_shader.set_vec3("pointLights[1].specular", [1.0, 1.0, 1.0])
        lighting_shader.set_float("pointLights[1].constant", 1.0)
        lighting_shader.set_float("pointLights[1].linear", 0.09)
        lighting_shader.set_float("pointLights[1].quadratic", 0.032)
        # -- point light 3
        lighting_shader.set_vec3("pointLights[2].position", point_light_positions[2])
        lighting_shader.set_vec3("pointLights[2].ambient", [0.05, 0.05, 0.05])
        lighting_shader.set_vec3("pointLights[2].diffuse", [0.8, 0.8, 0.8])
        lighting_shader.set_vec3("pointLights[2].specular", [1.0, 1.0, 1.0])
        lighting_shader.set_float("pointLights[2].constant", 1.0)
        lighting_shader.set_float("pointLights[2].linear", 0.09)
        lighting_shader.set_float("pointLights[2].quadratic", 0.032)
        # -- point light 4
        lighting_shader.set_vec3("pointLights[3].position", point_light_positions[3])
        lighting_shader.set_vec3("pointLights[3].ambient", [0.05, 0.05, 0.05])
        lighting_shader.set_vec3("pointLights[3].diffuse", [0.8, 0.8, 0.8])
        lighting_shader.set_vec3("pointLights[3].specular", [1.0, 1.0, 1.0])
        lighting_shader.set_float("pointLights[3].constant", 1.0)
        lighting_shader.set_float("pointLights[3].linear", 0.09)
        lighting_shader.set_float("pointLights[3].quadratic", 0.032)
        # -- spotLight
        lighting_shader.set_vec3("spotLight.position", camera.position)
        lighting_shader.set_vec3("spotLight.direction", camera.front)
        lighting_shader.set_vec3("spotLight.ambient", [0.0, 0.0, 0.0])
        lighting_shader.set_vec3("spotLight.diffuse", [1.0, 1.0, 1.0])
        lighting_shader.set_vec3("spotLight.specular", [1.0, 1.0, 1.0])
        lighting_shader.set_float("spotLight.constant", 1.0)
        lighting_shader.set_float("spotLight.linear", 0.09)
        lighting_shader.set_float("spotLight.quadratic", 0.032)
        lighting_shader.set_float("spotLight.cutOff", math.cos(math.radians(12.5)))
        lighting_shader.set_float("spotLight.outerCutOff", math.cos(math.radians(15.0)))

        # -- view.projection transformations
        projection = Matrix44.perspective_projection(camera.zoom, SRC_WIDTH/SRC_HEIGHT, 0.1, 100.0)
        view = camera.get_view_matrix()
        lighting_shader.set_mat4("projection", projection)
        lighting_shader.set_mat4("view", view)

        # -- world transformation
        model = Matrix44.identity()
        lighting_shader.set_mat4("model", model)

        # -- bind diffuse map
        gl.glActiveTexture(gl.GL_TEXTURE0)
        gl.glBindTexture(gl.GL_TEXTURE_2D, diffuse_map)

        # -- bind specular map
        gl.glActiveTexture(gl.GL_TEXTURE1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, specular_map)

        # -- render continers
        gl.glBindVertexArray(cube_vao)
        for idx, position in enumerate(cube_positions):
            angle = 20.0 * idx
            rotation = matrix44.create_from_axis_rotation([1.0, 0.3, 0.5], math.radians(angle))
            translation = Matrix44.from_translation(position)
            model = translation * rotation
            lighting_shader.set_mat4('model', model)
            gl.glDrawArrays(gl.GL_TRIANGLES, 0, 36)

        # -- draw lamp object(s)
        lamp_shader.use()
        lamp_shader.set_mat4("projection", projection)
        lamp_shader.set_mat4("view", view)

        gl.glBindVertexArray(light_vao)
        for pos in point_light_positions:
            model = Matrix44.identity()
            model *= Matrix44.from_translation(pos)
            model *= Matrix44.from_scale(Vector3([.2, .2, .2]))
            lamp_shader.set_mat4("model", model)
            gl.glDrawArrays(gl.GL_TRIANGLES, 0, 36)

        glfw.swap_buffers(window)
        glfw.poll_events()

    gl.glDeleteVertexArrays(1, id(cube_vao))
    gl.glDeleteVertexArrays(1, id(light_vao))
    gl.glDeleteBuffers(1, id(vbo))
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
