import os
import assimp
import OpenGL.GL as gl
from PIL import Image
from pprint import pformat
from mesh import vec2, vec3, Vertex, Texture, Mesh


class Model:

    def __init__(self, path, gamma=False):

        self.textures_loaded = set()
        self.meshes = list()
        self.directory = ""
        self.gamma_correction = gamma

        self._load_model(path)

    def __repr__(self):
        return "Model<meshs={}>".format(pformat(self.meshes))

    def draw(self, shader):
        for mesh in self.meshes:
            mesh.draw(shader)

    def _load_model(self, path):
        PP = assimp.aiPostProcessSteps
        post_process = (PP.aiProcess_Triangulate |
                        PP.aiProcess_FlipUVs |
                        PP.aiProcess_CalcTangentSpace)
        scene = assimp.aiImportFile(path, post_process)
        if not scene or not scene.mRootNode:
            raise ValueError("ERROR:: Assimp model failed to load, {}".format(path))
            return

        self.directory = os.path.dirname(path)
        self._process_node(scene.mRootNode, scene)

    def _process_node(self, node, scene):
        # process each mesh located at the current node
        for i in range(node.mNumMeshes):
            # the node object only contains indices to index the actual objects in the scene.
            # the scene contains all the data, node is just to keep stuff organized (like relations between nodes).
            mesh = scene.mMeshes[node.mMeshes[i]]
            self.meshes.append(self._process_mesh(mesh, scene))

        # -- recursively process child nodes
        for i in range(node.mNumChildren):
            self._process_node(node.mChildren[i], scene)

    def _process_mesh(self, mesh, scene):
        vertices, indices, textures = [], [], []

        # Walk through mesh's vertices
        for i in range(mesh.mNumVertices):
            px, py, pz = mesh.mVertices[i]
            nx, ny, nz = mesh.mNormals[i]

            # -- if we have texture coords
            tx, ty = 0.0, 0.0
            if mesh.mTextureCoords[0].any():
                tx, ty = mesh.mTextureCoords[0][i]

            tanx, tany, tanz = mesh.mTangents[i]
            bitanx, bitany, bitanz = mesh.mBitangents[i]

            vertices.append(Vertex(
                p=vec3(px, py, pz),
                n=vec3(nx, ny, nz),
                tc=vec2(tx, ty),
                tn=vec3(tanx, tany, tanz),
                bt=vec3(bitanx, bitany, bitanz))
            )

        # walk through mesh faces and retrieve indices
        for i in range(mesh.mNumFaces):
            indices.extend(list(mesh.mFaces[i]))

        # process materials
        material = scene.mMaterials[mesh.mMaterialIndex]

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

        return Mesh(vertices, indices, textures)

    def _load_material_textures(self, mat, type, type_name):
        textures = []

        for i in range(mat.GetTextureCount(type)):
            path = mat.GetTexture(type, i)

            skip = False
            for tex in self.textures_loaded:
                if path == tex.path:
                    textures.append(tex)
                    skip = True
                    break

            if not skip:
                tex = Texture(TextureFromFile(path, self.directory), type_name, path)
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
