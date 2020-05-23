import os
import time
import assimp
import OpenGL.GL as gl
import itertools as it
from PIL import Image
from mesh import Texture, Mesh
from ctypes import c_uint, c_float


class Model:

    def __init__(self, path, gamma=False):
        self.path = path
        self.textures_loaded = set()
        self.meshes = list()
        self.directory = ""
        self.gamma_correction = gamma

        self._load_model()

    def draw(self, shader):
        for mesh in self.meshes:
            mesh.draw(shader)

    def unpack_data_to_c(self, data, ctype=c_float):
        unpacked = list(it.chain.from_iterable(data))
        return (ctype * len(unpacked))(*unpacked)

    def interweave(self, *items):
        result = []
        num_items = max(len(it) for it in items)
        for i in range(num_items):
            result.append([x for it in items for x in it[i]])
        return result

    def _load_model(self):
        path = self.path
        start_time = time.time()

        post_process = (assimp.Process_Triangulate |
                        assimp.Process_FlipUVs |
                        assimp.Process_CalcTangentSpace)
        scene = assimp.ImportFile(path, post_process)
        if not scene:
            raise ValueError("ERROR:: Assimp model failed to load, {}".format(path))

        self.directory = os.path.dirname(path)
        for m in scene.meshes:
            self.meshes.append(self._process_mesh(m, scene))

        print("Took {}s to load model {}".format(
                round(time.time()-start_time, 3), os.path.basename(path)))

    def _process_mesh(self, mesh, scene):
        texcoords = []
        if mesh.num_uv_components[0] == 2:
            texcoords = [(x, y) for x, y, x in mesh.texcoords[0]]

        vertex_data = [
            mesh.vertices,
            mesh.normals,
            texcoords,
            mesh.tangents,
            mesh.bitangents
        ]

        indices = self.unpack_data_to_c(mesh.faces, ctype=c_uint)
        data = self.unpack_data_to_c(self.interweave(*vertex_data))

        # process materials
        textures = []
        material = scene.materials[mesh.material_index]

        # we assume a convention for sampler names in the shaders. Each diffuse texture should be named
        # as 'texture_diffuseN' where N is a sequential number ranging from 1 to MAX_SAMPLER_NUMBER.
        # Same applies to other texture as the following list summarizes:
        # diffuse: texture_diffuseN
        # specular: texture_specularN
        # normal: texture_normalN

        # 1. diffuse maps
        diffuse_maps = self._load_material_textures(
            material, assimp.TextureType_DIFFUSE, "texture_diffuse")
        textures.extend(diffuse_maps)

        # 2. specular maps
        specular_maps = self._load_material_textures(
            material, assimp.TextureType_SPECULAR, "texture_specular")
        textures.extend(specular_maps)

        # 3. normal maps
        normal_maps = self._load_material_textures(
            material, assimp.TextureType_HEIGHT, "texture_normal")
        textures.extend(normal_maps)

        # 4. height maps
        height_maps = self._load_material_textures(
            material, assimp.TextureType_AMBIENT, "texture_height")
        textures.extend(height_maps)

        return Mesh(data, indices, textures)

    def _load_material_textures(self, mat, type, type_name):
        textures = []

        paths = mat["TEXTURES"].get(type)
        if paths:
            for p in paths:

                skip = False
                for tex in self.textures_loaded:
                    if p == tex.path:
                        textures.append(tex)
                        skip = True
                        break

                if not skip:
                    tex = Texture(TextureFromFile(p, self.directory), type_name, p)
                    textures.append(tex)
                    self.textures_loaded.add(tex)

        return textures


def TextureFromFile(path, directory, gamma=False):
    textureID = gl.glGenTextures(1)
    img = Image.open(os.path.join(directory, path))

    format_ = {
        1 : gl.GL_RED,
        3 : gl.GL_RGB,
        4 : gl.GL_RGBA,
    }.get(len(img.getbands()))

    gl.glBindTexture(gl.GL_TEXTURE_2D, textureID)
    gl.glTexImage2D(
        gl.GL_TEXTURE_2D, 0, format_, img.width, img.height,
        0, format_, gl.GL_UNSIGNED_BYTE, img.tobytes()
    )
    gl.glGenerateMipmap(gl.GL_TEXTURE_2D)

    # -- texture wrapping
    gl.glTexParameter(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_REPEAT)
    gl.glTexParameter(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_REPEAT)
    # -- texture filterting
    gl.glTexParameter(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR_MIPMAP_LINEAR)
    gl.glTexParameter(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)

    return textureID
