from cTypes cimport *

cdef extern from "anim.h" nogil:
    cdef cppclass aiVectorKey:
        double mTime
        aiVector3D mValue

        aiVectorKey()

    cdef cppclass aiQuatKey:
        double mTime
        aiQuaternion mValue

        aiQuatKey()

    cdef cppclass aiMeshKey:
        double mTime
        unsigned int mValue

        aiMeshKey()
        
    cdef cppclass aiNodeAnim:
        aiString mNodeName
        unsigned int mNumPositionKeys
        aiVectorKey* mPositionKeys
        unsigned int mNumRotationKeys
        aiQuatKey* mRotationKeys
        unsigned int mNumScalingKeys
        aiVectorKey* mScalingKeys
        #aiAnimBehaviour mPreState
        #aiAnimBehaviour mPostState

        aiNodeAnim()

    cdef cppclass aiMeshAnim:
        aiString mName
        unsigned int mNumKeys
        aiMeshKey* mKeys
        
        aiMeshAnim()

    cdef cppclass aiAnimation:
        aiString mName
        double mDuration
        double mTicksPerSecond
        unsigned int mNumChannels
        aiNodeAnim** mChannels
        unsigned int mNumMeshChannels
        aiMeshAnim** mMeshChannels

        aiAnimation()