from cTypes cimport *
cimport numpy as np

ctypedef int bool

cdef extern from "mesh.h" nogil:
    cdef int _AI_MAX_FACE_INDICES 'AI_MAX_FACE_INDICES'
    cdef int _AI_MAX_BONE_WEIGHTS 'AI_MAX_BONE_WEIGHTS'
    cdef int _AI_MAX_VERTICES 'AI_MAX_VERTICES'
    cdef int _AI_MAX_FACES 'AI_MAX_FACES'
    cdef int _AI_MAX_NUMBER_OF_COLOR_SETS 'AI_MAX_NUMBER_OF_COLOR_SETS'
    cdef int _AI_MAX_NUMBER_OF_TEXTURECOORDS 'AI_MAX_NUMBER_OF_TEXTURECOORDS'

    cdef cppclass aiMesh:
        unsigned int mPrimitiveTypes
        unsigned int mNumVertices
        unsigned int mNumFaces
        aiVector3D* mVertices
        aiVector3D* mNormals
        aiVector3D* mTangents
        aiVector3D* mBitangents
        aiColor4D* mColors[]
        aiVector3D* mTextureCoords[]
        unsigned int mNumUVComponents[]
        aiFace* mFaces
        unsigned int mNumBones
        aiBone** mBones
        unsigned int mMaterialIndex
        aiString mName
        #unsigned int mNumAnimMeshes
        #aiAnimMesh** mAnimMeshes

        aiMesh()

        bool HasPositions() const
        bool HasFaces() const
        bool HasNormals() const
        bool HasTangentsAndBitangents() const
        bool HasVertexColors( unsigned int pIndex) const
        bool HasTextureCoords( unsigned int pIndex) const
        unsigned int GetNumUVChannels() const
        unsigned int GetNumColorChannels() const
        inline bool HasBones() const

    cdef cppclass aiFace:
        unsigned int mNumIndices
        unsigned int* mIndices

        aiFace()


    cdef cppclass aiVertexWeight:
        unsigned int mVertexId
        float mWeight

        aiVertexWeight()
        
    cdef cppclass aiBone:
        aiString mName
        unsigned int mNumWeights
        aiVertexWeight* mWeights
        aiMatrix4x4 mOffsetMatrix

        aiBone()