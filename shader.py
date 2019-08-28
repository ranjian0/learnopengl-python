import OpenGL.GL as gl
from OpenGL.GL import shaders


class Shader:

    def __init__(self, vertex_shader_path,
                       fragment_shader_path,
                       geometry_shader_path=None):

        vertex_shader   = self._load(vertex_shader_path)
        fragment_shader = self._load(fragment_shader_path)
        self.ID = shaders.compileProgram(
            shaders.compileShader(vertex_shader,    gl.GL_VERTEX_SHADER),
            shaders.compileShader(fragment_shader,  gl.GL_FRAGMENT_SHADER),
        )

    def _load(self, path):
        shader_source = ""
        with open(path, 'r') as shader_file:
            shader_source = shader_file.readlines()
        return shader_source

    def use(self):
        gl.glUseProgram(self.ID)

    def set_bool(self, name, value):
        gl.glUniform1i(gl.glGetUniformLocation(self.ID, name), value)

    def set_int(self, name, value):
        gl.glUniform1i(gl.glGetUniformLocation(self.ID, name), value)

    def set_float(self, name, value):
        gl.glUniform1f(gl.glGetUniformLocation(self.ID, name), value)

    def set_vec2(self, name, value):
        gl.glUniform2fv(gl.glGetUniformLocation(self.ID, name), 1, value)

    def set_vec3(self, name, value):
        gl.glUniform3fv(gl.glGetUniformLocation(self.ID, name), 1, value)

    def set_vec4(self, name, value):
        gl.glUniform4fv(gl.glGetUniformLocation(self.ID, name), 1, value)

    def set_mat3(self, name, value):
        gl.glUniformMatrix3fv(gl.glGetUniformLocation(self.ID, name), 1, gl.GL_FALSE, value)

    def set_mat4(self, name, value):
        gl.glUniformMatrix4fv(gl.glGetUniformLocation(self.ID, name), 1, gl.GL_FALSE, value)
