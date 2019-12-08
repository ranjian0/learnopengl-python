import glfw
import OpenGL.GL as gl
from OpenGL.GL import shaders
from ctypes import c_float, sizeof, c_void_p

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


def main():
    glfw.init()
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    window = glfw.create_window(800, 600, "LearnOpenGL", None, None)
    if not window:
        print("Window Creation failed!")
        glfw.terminate()

    glfw.make_context_current(window)
    glfw.set_window_size_callback(window, on_resize)

    shader = shaders.compileProgram(
        shaders.compileShader(vertex_shader,    gl.GL_VERTEX_SHADER),
        shaders.compileShader(fragment_shader,  gl.GL_FRAGMENT_SHADER),
    )

    vertices_tria_a = [
     # first triangle
     -0.9, -0.5, 0.0,  # left
     -0.0, -0.5, 0.0,  # right
     -0.45, 0.5, 0.0,  # top
     ]
    vertices_tria_a = (c_float * len(vertices_tria_a))(*vertices_tria_a)

    vertices_tria_b = [
     # second triangle
     0.0, -0.5, 0.0,  # left
     0.9, -0.5, 0.0,  # right
     0.45, 0.5, 0.0   # top
    ]
    vertices_tria_b = (c_float * len(vertices_tria_b))(*vertices_tria_b)

    vaos = gl.glGenVertexArrays(2)
    vbos = gl.glGenBuffers(2)

    gl.glBindVertexArray(vaos[0])
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbos[0])
    gl.glBufferData(gl.GL_ARRAY_BUFFER, sizeof(vertices_tria_a), vertices_tria_a, gl.GL_STATIC_DRAW)
    gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 3 * sizeof(c_float), c_void_p(0))
    gl.glEnableVertexAttribArray(0)

    gl.glBindVertexArray(vaos[1])
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbos[1])
    gl.glBufferData(gl.GL_ARRAY_BUFFER, sizeof(vertices_tria_b), vertices_tria_b, gl.GL_STATIC_DRAW)
    gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 3 * sizeof(c_float), c_void_p(0))
    gl.glEnableVertexAttribArray(0)

    while not glfw.window_should_close(window):
        process_input(window)

        gl.glClearColor(.2, .3, .3, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        gl.glUseProgram(shader)
        gl.glBindVertexArray(vaos[0])
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, 3)

        gl.glBindVertexArray(vaos[1])
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, 3)

        glfw.poll_events()
        glfw.swap_buffers(window)

    gl.glDeleteVertexArrays(2, id(vaos))
    gl.glDeleteBuffers(2, id(vbos))
    glfw.terminate()


def on_resize(window, w, h):
    gl.glViewport(0, 0, w, h)


def process_input(window):
    if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
        glfw.set_window_should_close(window, True)


if __name__ == '__main__':
    main()
