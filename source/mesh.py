import OpenGL.GL as gl
from ctypes import c_uint, c_float, sizeof, c_void_p


class vec2:
    def __init__(self, x=0, y=0):
        self.x, self.y = x, y

    def __getitem__(self, i):
        return [self.x, self.y][i]


class vec3:
    def __init__(self, x=0, y=0, z=0):
        self.x, self.y, self.z = x, y, z

    def __getitem__(self, i):
        return [self.x, self.y, self.z][i]


class Vertex:
    def __init__(self, p=vec3(), n=vec3(), tc=vec2(), tn=vec3(), bt=vec3()):
        self.position = p
        self.normal = n
        self.texcoords = tc
        self.tangent = tn
        self.bitangent = bt

    @staticmethod
    def size():
        """ Combined byte size of attibutes """
        #       p   n   t   tn  bt
        return (3 + 3 + 2 + 3 + 3) * sizeof(c_float)

    @staticmethod
    def offset(attribute):
        """ Determine the offset of an attribute in the vertex byte data"""
        # [p, p, p, n, n, n, t, t, tn, tn, tn, bt, bt, bt]
        #  ^        ^        ^     ^           ^
        offsets = [0, 3, 6, 8, 11]
        attributes = ["position", "normal", "texcoords", "tangent", "bitangent"]
        if attribute not in attributes:
            raise ValueError(
                "Invalid attribute name. must be one of {}".format(attributes)
            )

        return c_void_p(dict(zip(attributes, offsets)).get(attribute) * sizeof(c_float))

    def data(self):
        return (self.position[:] +
                self.normal[:] +
                self.texcoords[:] +
                self.tangent[:] +
                self.bitangent[:])


class Texture:
    def __init__(self, id=0, type="", path=""):
        self.id = id
        self.type = type
        self.path = path

    def __repr__(self):
        return "Texture<id={}, path={}>".format(self.id, self.path)


class Mesh:
    def __init__(self, vertices=None, indices=None, textures=None):
        self.vertices = vertices or list()
        self.indices = indices or list()
        self.textures = textures or list()
        self.vao = None

        self._vbo = None
        self._ebo = None
        self._setup_mesh()

    def __repr__(self):
        return "Mesh<nverts={}, texture={}>".format(len(self.vertices), self.textures)

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
        gl.glDrawElements(gl.GL_TRIANGLES, len(self.indices), gl.GL_UNSIGNED_INT, 0)
        gl.glBindVertexArray(0)
        gl.glActiveTexture(gl.GL_TEXTURE0)

    def _cdata(self):
        """ Transform list of Vertex data into float array """
        data = []
        for v in self.vertices:
            data.extend(v.data())
        return (c_float * len(data))(*data)

    def _cindices(self):
        return (c_uint * len(self.indices))(*self.indices)

    def _setup_mesh(self):
        self.vao = gl.glGenVertexArrays(1)
        self._vbo = gl.glGenBuffers(1)
        self._ebo = gl.glGenBuffers(1)

        gl.glBindVertexArray(self.vao)

        data = self._cdata()
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self._vbo)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, sizeof(data), data, gl.GL_STATIC_DRAW)

        index = self._cindices()
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self._ebo)
        gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, sizeof(index), index, gl.GL_STATIC_DRAW)

        # -- set vertex attibute pointers
        # -- vertex positions
        gl.glEnableVertexAttribArray(0)
        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE,
                                 Vertex.size(), Vertex.offset("position"))

        # -- vertex normals
        gl.glEnableVertexAttribArray(1)
        gl.glVertexAttribPointer(1, 3, gl.GL_FLOAT, gl.GL_FALSE,
                                 Vertex.size(), Vertex.offset("normal"))
        # -- vertex texture coords
        gl.glEnableVertexAttribArray(2)
        gl.glVertexAttribPointer(2, 2, gl.GL_FLOAT, gl.GL_FALSE,
                                 Vertex.size(), Vertex.offset("texcoords"))
        # -- vertex tangent
        gl.glEnableVertexAttribArray(3)
        gl.glVertexAttribPointer(3, 3, gl.GL_FLOAT, gl.GL_FALSE,
                                 Vertex.size(), Vertex.offset("tangent"))
        # -- vertex bitangent
        gl.glEnableVertexAttribArray(4)
        gl.glVertexAttribPointer(4, 3, gl.GL_FLOAT, gl.GL_FALSE,
                                 Vertex.size(), Vertex.offset("bitangent"))

        gl.glBindVertexArray(0)
