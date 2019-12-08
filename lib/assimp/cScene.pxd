from cTypes cimport aiString, aiMatrix4x4
from cMesh cimport aiMesh
from cMaterial cimport aiMaterial
from cAnim cimport aiAnimation
ctypedef int bool

cdef extern from "scene.h" nogil:
    cdef cppclass aiNode:
        aiString mName;
        aiMatrix4x4 mTransformation;
        aiNode* mParent;
        unsigned int mNumChildren;
        aiNode** mChildren;
        unsigned int mNumMeshes;
        unsigned int* mMeshes;

        aiNode()


    cdef cppclass aiScene:
        unsigned int mFlags;
        aiNode* mRootNode;
        unsigned int mNumMeshes;
        aiMesh** mMeshes;
        int mNumMaterials;
        aiMaterial** mMaterials;
        unsigned int mNumAnimations;
        aiAnimation** mAnimations;
        unsigned int mNumTextures;
        #aiTexture** mTextures;
        unsigned int mNumLights;
        #aiLight** mLights;
        unsigned int mNumCameras;
        #aiCamera** mCameras;

        inline bool HasMeshes() const
        inline bool HasMaterials() const
        inline bool HasLights() const
        inline bool HasTextures() const
        inline bool HasCameras() const
        inline bool HasAnimations() const

        aiScene()
