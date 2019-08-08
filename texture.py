import os
import OpenGL.GL as gl

from PIL import Image

RESOURCES = os.path.abspath('resources')
TEXTURES_DIR = os.path.join(RESOURCES, 'textures')


def get_image_data(file_path, flip_y=False, flip_x=False):
    img = Image.open(file_path)
    if flip_y:
        img = img.transpose(Image.FLIP_TOP_BOTTOM)
    if flip_x:
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
    return img, img.tobytes()


def load_texture(filename,
                 texture_format=gl.GL_RGB, image_format=gl.GL_RGB,
                 wrap_method=gl.GL_REPEAT, filter_method=gl.GL_LINEAR,
                 flip_y=True, flip_x=False,
                 generate_mipmaps=True):

    textureID = gl.glGenTextures(1)
    gl.glBindTexture(gl.GL_TEXTURE_2D, textureID)
    # -- texture wrapping
    gl.glTexParameter(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, wrap_method)
    gl.glTexParameter(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, wrap_method)
    # -- texture filterting
    gl.glTexParameter(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, filter_method)
    gl.glTexParameter(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, filter_method)

    img, img_data = get_image_data(os.path.join(TEXTURES_DIR, filename), flip_y, flip_x)
    gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, texture_format, img.width, img.height, 0, image_format, gl.GL_UNSIGNED_BYTE, img_data)
    if generate_mipmaps:
        gl.glGenerateMipmap(gl.GL_TEXTURE_2D)
    return textureID
