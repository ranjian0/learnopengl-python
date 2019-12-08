import os
import numpy as np
from glob import glob
# from pathlib import Path


CURDIR = os.path.abspath(os.path.dirname(__file__))

ASSIMP_SOURCES = [
    os.path.join(CURDIR, 'source', 'assimp', 'all.pyx')
] + glob(os.path.join(CURDIR, 'extern', 'assimp', 'code') + '/**/*.cpp', recursive=True)

ASSIMP_INCLUDE_DIRS = [
    np.get_include(),
    os.path.join(CURDIR, 'source', 'assimp'),
    os.path.join(CURDIR, 'extern', 'assimp'),
    os.path.join(CURDIR, 'extern', 'assimp', 'code'),
    os.path.join(CURDIR, 'extern', 'assimp', 'include'),
    os.path.join(CURDIR, 'extern', 'assimp', 'include', 'assimp')
]
print(ASSIMP_INCLUDE_DIRS)


ASSIMP_DEFINES = [
    # ('OPENDDLPARSER_BUILD', None).
    # ('ASSIMP_BUILD_SINGLETHREADED', None),
    # ('ASSIMP_BUILD_BOOST_WORKAROUND', None),
    # ('ASSIMP_BUILD_NO_OBJ_IMPORTER', None),
    ('ASSIMP_BUILD_NO_EXPORT', None),
    ('ASSIMP_BUILD_NO_OWN_ZLIB', None),
    ('ASSIMP_BUILD_NO_X_IMPORTER', None),
    ('ASSIMP_BUILD_NO_3D_IMPORTER', None),
    ('ASSIMP_BUILD_NO_AC_IMPORTER', None),
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
    ('ASSIMP_BUILD_NO_BVH_IMPORTER', None),
    ('ASSIMP_BUILD_NO_IRR_IMPORTER', None),
    ('ASSIMP_BUILD_NO_Q3D_IMPORTER', None),
    ('ASSIMP_BUILD_NO_B3D_IMPORTER', None),
    ('ASSIMP_BUILD_NO_CSM_IMPORTER', None),
    ('ASSIMP_BUILD_NO_LWS_IMPORTER', None),
    ('ASSIMP_BUILD_NO_COB_IMPORTER', None),
    ('ASSIMP_BUILD_NO_IFC_IMPORTER', None),
    ('ASSIMP_BUILD_NO_XGL_IMPORTER', None),
    ('ASSIMP_BUILD_NO_NDO_IMPORTER', None),
    ('ASSIMP_BUILD_NO_C4D_IMPORTER', None),
    ('ASSIMP_BUILD_NO_3MF_IMPORTER', None),
    ('ASSIMP_BUILD_NO_X3D_IMPORTER', None),
    ('ASSIMP_BUILD_NO_M3D_IMPORTER', None),
    ('ASSIMP_BUILD_NO_MMD_IMPORTER', None),
    ('ASSIMP_BUILD_NO_FBX_IMPORTER', None),
    ('ASSIMP_BUILD_NO_GLTF_IMPORTER', None),
    ('ASSIMP_BUILD_NO_MS3D_IMPORTER', None),
    ('ASSIMP_BUILD_NO_STEP_IMPORTER', None),
    ('ASSIMP_BUILD_NO_OGRE_IMPORTER', None),
    ('ASSIMP_BUILD_NO_BLEND_IMPORTER', None),
    ('ASSIMP_BUILD_NO_GLTF2_IMPORTER', None),
    ('ASSIMP_BUILD_NO_Q3BSP_IMPORTER', None),
    ('ASSIMP_BUILD_NO_ASSBIN_IMPORTER', None),
    ('ASSIMP_BUILD_NO_IRRMESH_IMPORTER', None),
    ('ASSIMP_BUILD_NO_COLLADA_IMPORTER', None),
    ('ASSIMP_BUILD_NO_OPENGEX_IMPORTER', None),
    ('ASSIMP_BUILD_NO_TERRAGEN_IMPORTER', None),
]