import os
import OpenGL.GL as gl

from PIL import Image
from pathlib import Path


RESOURCES = Path(__file__).absolute().parent.parent.joinpath('resources')
TEXTURES_DIR = RESOURCES.joinpath('textures')


def load_texture(path,
                 mag_filter=gl.GL_LINEAR,
                 min_filter=gl.GL_LINEAR_MIPMAP_LINEAR,
                 wrap_s=gl.GL_REPEAT, wrap_t=gl.GL_REPEAT,
                 flip_y=False, flip_x=False,
                 generate_mipmaps=True):

    textureID = gl.glGenTextures(1)
    img = Image.open(os.path.join(TEXTURES_DIR, path))
    img = flip_image(img, flip_x, flip_y)

    format_ = {
        1 : gl.GL_RED,
        3 : gl.GL_RGB,
        4 : gl.GL_RGBA,
    }.get(len(img.getbands()))

    gl.glBindTexture(gl.GL_TEXTURE_2D, textureID)
    gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, format_, img.width, img.height, 0, format_, gl.GL_UNSIGNED_BYTE, img.tobytes())
    if generate_mipmaps:
        gl.glGenerateMipmap(gl.GL_TEXTURE_2D)

    # -- texture wrapping
    gl.glTexParameter(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, wrap_s)
    gl.glTexParameter(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, wrap_t)
    # -- texture filterting
    gl.glTexParameter(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, min_filter)
    gl.glTexParameter(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, mag_filter)

    return textureID


def flip_image(img, flip_y=False, flip_x=False):
    if flip_y:
        return img.transpose(Image.FLIP_TOP_BOTTOM)
    elif flip_x:
        return img.transpose(Image.FLIP_LEFT_RIGHT)
    return img
