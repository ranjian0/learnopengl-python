import OpenGL.GL as gl
from ctypes import c_float, sizeof, c_void_p, Structure


Vec2 = (2 * c_float)
Vec3 = (3 * c_float)

class Vertex(Structure):
    _fields_ = [
        ("Position",    Vec3),
        ("Normal",      Vec3),
        ("TexCoords",   Vec2),
        ("Tangent",     Vec3),
        ("Bitangent",   Vec3),
    ]


class Texture:
    def __init__(self, id=0, type="", path=""):
        self.id = id
        self.type = type
        self.path = path

    def __repr__(self):
        return "Texture<id={}, path={}>".format(self.id, self.path)


class Mesh:
    def __init__(self, data, indices, textures=None):
        self.data = data
        self.indices = indices
        self.textures = textures

        self.vao = None

        self._vbo = None
        self._ebo = None
        self._setup_mesh()

    def draw(self, shader):
        normal_nr = 1
        height_nr = 1
        diffuse_nr = 1
        specular_nr = 1

        for idx, texture in enumerate(self.textures):
            gl.glActiveTexture(gl.GL_TEXTURE0 + idx)

            number = str()
            name = texture.type
            if name == 'texture_diffuse':
                number = str(diffuse_nr)
                diffuse_nr += 1
            elif name == 'texture_specular':
                number = str(specular_nr)
                specular_nr += 1
            elif name == 'texture_normal':
                number = str(normal_nr)
                normal_nr += 1
            elif name == 'texture_height':
                number = str(height_nr)
                height_nr += 1

            shader.set_int(name + number, idx)
            gl.glBindTexture(gl.GL_TEXTURE_2D, texture.id)

        gl.glBindVertexArray(self.vao)
        gl.glDrawElements(gl.GL_TRIANGLES, len(self.indices), gl.GL_UNSIGNED_INT, c_void_p(0))
        gl.glBindVertexArray(0)
        gl.glActiveTexture(gl.GL_TEXTURE0)

    def _setup_mesh(self):
        self.vao = gl.glGenVertexArrays(1)
        gl.glBindVertexArray(self.vao)

        self._vbo = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self._vbo)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, sizeof(self.data), self.data, gl.GL_STATIC_DRAW)

        self._ebo = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self._ebo)
        gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, sizeof(self.indices), self.indices, gl.GL_STATIC_DRAW)

        # -- set vertex attibute pointers
        # -- vertex positions
        gl.glEnableVertexAttribArray(0)
        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE,
                                 sizeof(Vertex), c_void_p(Vertex.Position.offset))

        # -- vertex normals
        gl.glEnableVertexAttribArray(1)
        gl.glVertexAttribPointer(1, 3, gl.GL_FLOAT, gl.GL_FALSE,
                                 sizeof(Vertex), c_void_p(Vertex.Normal.offset))

        # -- vertex texture coords
        gl.glEnableVertexAttribArray(2)
        gl.glVertexAttribPointer(2, 2, gl.GL_FLOAT, gl.GL_FALSE,
                                 sizeof(Vertex), c_void_p(Vertex.TexCoords.offset))

        # -- vertex tangent
        gl.glEnableVertexAttribArray(3)
        gl.glVertexAttribPointer(3, 3, gl.GL_FLOAT, gl.GL_FALSE,
                                 sizeof(Vertex), c_void_p(Vertex.Tangent.offset))

        # -- vertex bitangent
        gl.glEnableVertexAttribArray(4)
        gl.glVertexAttribPointer(4, 3, gl.GL_FLOAT, gl.GL_FALSE,
                                 sizeof(Vertex), c_void_p(Vertex.Bitangent.offset))


        gl.glBindVertexArray(0)
