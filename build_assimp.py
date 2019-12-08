import os
import numpy as np
from Cython.Build import cythonize
from sys import platform as _platform
from setuptools import Extension, setup

# monkey-patch for parallel compilation
import multiprocessing
import multiprocessing.pool


def parallelCCompile(self, sources, output_dir=None, macros=None, include_dirs=None,
    debug=0, extra_preargs=None, extra_postargs=None, depends=None):

    # those lines are copied from distutils.ccompiler.CCompiler directly
    macros, objects, extra_postargs, pp_opts, build = self._setup_compile(
      output_dir, macros, include_dirs, sources, depends, extra_postargs)
    cc_args = self._get_cc_args(pp_opts, debug, extra_preargs)
    # parallel code
    N = 2 * multiprocessing.cpu_count()  # number of parallel compilations
    try:
        # On Unix-like platforms attempt to obtain the total memory in the
        # machine and limit the number of parallel jobs to the number of Gbs
        # of RAM (to avoid killing smaller platforms like the Pi)
        mem = os.sysconf('SC_PHYS_PAGES') * os.sysconf('SC_PAGE_SIZE')  # bytes
    except (AttributeError, ValueError):
        # Couldn't query RAM; don't limit parallelism (it's probably a well
        # equipped Windows / Mac OS X box)
        pass
    else:
        mem = max(1, int(round(mem / 1024**3)))  # convert to Gb
        N = min(mem, N)

    def _single_compile(obj):
        try:
            src, ext = build[obj]
        except KeyError:
            return
        newcc_args = cc_args
        if _platform == "darwin":
            if src.endswith('.cpp'):
                newcc_args = cc_args + ["-mmacosx-version-min=10.7", "-stdlib=libc++"]
        self._compile(obj, src, ext, newcc_args, extra_postargs, pp_opts)

    # convert to list, imap is evaluated on-demand
    pool = multiprocessing.pool.ThreadPool(N)
    list(pool.imap(_single_compile, objects))
    return objects


import distutils.ccompiler
distutils.ccompiler.CCompiler.compile = parallelCCompile


CURDIR = os.path.dirname(__file__)

includes = [
    np.get_include(),
    os.path.join(CURDIR, 'lib', 'assimp'),
    os.path.join(CURDIR, 'extern', 'assimp'),
    os.path.join(CURDIR, 'extern', 'assimp', 'code'),
    os.path.join(CURDIR, 'extern', 'assimp', 'include'),
    os.path.join(CURDIR, 'extern', 'assimp', 'include', 'assimp')
    # os.path.join(CURDIR, 'extern', 'assimp', 'assimp'),
]


sources = [
    os.path.join(CURDIR, 'lib', 'assimp', 'all.pyx')
]

for path, dirs, files in os.walk(os.path.join(CURDIR, 'extern', 'assimp', 'code')):
    for file in files:
        if file.endswith('.cpp'):
            sources.append(os.path.join(path, file))

assimp_options = [
    # ('OPENDDLPARSER_BUILD', None).
    # ('ASSIMP_BUILD_SINGLETHREADED', None),
    # ('ASSIMP_BUILD_BOOST_WORKAROUND', None),
    # ('ASSIMP_BUILD_NO_OBJ_IMPORTER', None),
    ('ASSIMP_BUILD_NO_EXPORT', None),
    ('ASSIMP_BUILD_NO_OWN_ZLIB', None),
    ('ASSIMP_BUILD_NO_X_IMPORTER', None),
    ('ASSIMP_BUILD_NO_AMF_IMPORTER', None),
    ('ASSIMP_BUILD_NO_3DS_IMPORTER', None),
    ('ASSIMP_BUILD_NO_MD3_IMPORTER', None),
    ('ASSIMP_BUILD_NO_MD5_IMPORTER', None),
    ('ASSIMP_BUILD_NO_MDL_IMPORTER', None),
    ('ASSIMP_BUILD_NO_MD2_IMPORTER', None),
    ('ASSIMP_BUILD_NO_PLY_IMPORTER', None),
    ('ASSIMP_BUILD_NO_ASE_IMPORTER', None),
    ('ASSIMP_BUILD_NO_HMP_IMPORTER', None),
    ('ASSIMP_BUILD_NO_SMD_IMPORTER', None),
    ('ASSIMP_BUILD_NO_MDC_IMPORTER', None),
    ('ASSIMP_BUILD_NO_MD5_IMPORTER', None),
    ('ASSIMP_BUILD_NO_STL_IMPORTER', None),
    ('ASSIMP_BUILD_NO_LWO_IMPORTER', None),
    ('ASSIMP_BUILD_NO_DXF_IMPORTER', None),
    ('ASSIMP_BUILD_NO_NFF_IMPORTER', None),
    ('ASSIMP_BUILD_NO_RAW_IMPORTER', None),
    ('ASSIMP_BUILD_NO_SIB_IMPORTER', None),
    ('ASSIMP_BUILD_NO_OFF_IMPORTER', None),
    ('ASSIMP_BUILD_NO_AC_IMPORTER', None),
    ('ASSIMP_BUILD_NO_BVH_IMPORTER', None),
    ('ASSIMP_BUILD_NO_IRRMESH_IMPORTER', None),
    ('ASSIMP_BUILD_NO_IRR_IMPORTER', None),
    ('ASSIMP_BUILD_NO_Q3D_IMPORTER', None),
    ('ASSIMP_BUILD_NO_B3D_IMPORTER', None),
    ('ASSIMP_BUILD_NO_COLLADA_IMPORTER', None),
    ('ASSIMP_BUILD_NO_TERRAGEN_IMPORTER', None),
    ('ASSIMP_BUILD_NO_CSM_IMPORTER', None),
    ('ASSIMP_BUILD_NO_3D_IMPORTER', None),
    ('ASSIMP_BUILD_NO_LWS_IMPORTER', None),
    ('ASSIMP_BUILD_NO_OGRE_IMPORTER', None),
    ('ASSIMP_BUILD_NO_OPENGEX_IMPORTER', None),
    ('ASSIMP_BUILD_NO_MS3D_IMPORTER', None),
    ('ASSIMP_BUILD_NO_COB_IMPORTER', None),
    ('ASSIMP_BUILD_NO_BLEND_IMPORTER', None),
    ('ASSIMP_BUILD_NO_Q3BSP_IMPORTER', None),
    ('ASSIMP_BUILD_NO_NDO_IMPORTER', None),
    ('ASSIMP_BUILD_NO_STEP_IMPORTER', None),
    ('ASSIMP_BUILD_NO_IFC_IMPORTER', None),
    ('ASSIMP_BUILD_NO_XGL_IMPORTER', None),
    ('ASSIMP_BUILD_NO_ASSBIN_IMPORTER', None),
    ('ASSIMP_BUILD_NO_C4D_IMPORTER', None),
    ('ASSIMP_BUILD_NO_3MF_IMPORTER', None),
    ('ASSIMP_BUILD_NO_X3D_IMPORTER', None),
    ('ASSIMP_BUILD_NO_GLTF_IMPORTER', None),
    ('ASSIMP_BUILD_NO_GLTF2_IMPORTER', None),
    ('ASSIMP_BUILD_NO_M3D_IMPORTER', None),
    ('ASSIMP_BUILD_NO_MMD_IMPORTER', None),
    ('ASSIMP_BUILD_NO_FBX_IMPORTER', None),
]

setup(
    name="assimpcy",
    version='0.1',
    description='Faster Python bindings for Assimp.',
    install_requires=['numpy'],
    packages=["assimp"],
    ext_modules=cythonize([
        Extension('lib.assimp.all', sources,
                  include_dirs=includes,
                  define_macros=assimp_options,
                  language="c++")
    ]),
    requires=['numpy']
)
