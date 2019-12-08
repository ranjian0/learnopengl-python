cdef extern from "types.h" nogil:
    cdef cppclass aiString:
        char data[1024]
        aiString()

    cdef cppclass aiVector3D:
        float x,y,z

    cdef cppclass aiVector2D:
        float x,y

    cdef cppclass aiQuaternion:
        float w, x, y, z

    cdef cppclass aiMatrix4x4:
        float a1, a2, a3, a4
        float b1, b2, b3, b4
        float c1, c2, c3, c4
        float d1, d2, d3, d4

    cdef cppclass aiColor4D:
        float r, g, b, a

    cdef enum aiReturn:
        aiReturn_SUCCESS
        aiReturn_FAILURE
        aiReturn_OUTOFMEMORY

#AI_SUCCESS = aiReturn_SUCCESS
#AI_FAILURE = aiReturn_FAILURE
#AI_OUTOFMEMORY = aiReturn_OUTOFMEMORY