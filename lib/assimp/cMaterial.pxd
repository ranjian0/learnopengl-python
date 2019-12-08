from cTypes cimport *

cdef extern from "mesh.h" nogil:
    cdef const char* _AI_DEFAULT_MATERIAL_NAME 'AI_DEFAULT_MATERIAL_NAME'
    #cdef const tup _AI_MATKEY_NAME 'AI_MATKEY_NAME'
    
    cdef cppclass aiMaterialProperty:
        aiString mKey
        unsigned int mSemantic
        unsigned int mIndex
        unsigned int mDataLength
        aiPropertyTypeInfo mType
        char* mData
    
        aiMaterialProperty()


    cdef cppclass aiMaterial:
        aiMaterialProperty** mProperties;
        unsigned int mNumProperties;
        unsigned int mNumAllocated;

        aiMaterial()


    #cdef aiReturn aiGetMaterialTexture(const aiMaterial* mat,
    #                                    aiTextureType type,
    #                                    unsigned int  index,
    #                                    aiString* path,
    #                                    aiTextureMapping* mapping,
    #                                    unsigned int* uvindex	,
    #                                    float* blend			,
    #                                    aiTextureOp* op			,
    #                                    aiTextureMapMode* mapmode,
    #                                    unsigned int* flags       )

    cdef aiReturn aiGetMaterialString(const aiMaterial* pMat,
                                        const char* pKey,
                                        unsigned int type,
                                        unsigned int index,
                                        aiString* pOut)

    cdef aiReturn aiGetMaterialFloatArray(const aiMaterial* pMat,
                                             const char* pKey,
                                             unsigned int type,
                                             unsigned int index,
                                             float* pOut,
                                             unsigned int* pMax)

    cdef aiReturn aiGetMaterialIntegerArray(const aiMaterial* pMat,
                                            const char* pKey,
                                            unsigned int type,
                                            unsigned int index,
                                            int* pOut,
                                            unsigned int* pMax)



    cdef enum aiTextureType:
        aiTextureType_NONE
        aiTextureType_DIFFUSE
        aiTextureType_SPECULAR
        aiTextureType_AMBIENT
        aiTextureType_EMISSIVE
        aiTextureType_HEIGHT
        aiTextureType_NORMALS
        aiTextureType_SHININESS
        aiTextureType_OPACITY
        aiTextureType_DISPLACEMENT
        aiTextureType_LIGHTMAP
        aiTextureType_REFLECTION
        aiTextureType_UNKNOWN

    cdef enum aiPropertyTypeInfo:
        aiPTI_Float
        aiPTI_String
        aiPTI_Integer
        aiPTI_Buffer

    cdef enum aiTextureOp:
        aiTextureOp_Multiply
        aiTextureOp_Add
        aiTextureOp_Subtract
        aiTextureOp_Divide
        aiTextureOp_SmoothAdd
        aiTextureOp_SignedAdd

    cdef enum aiTextureMapping:
        aiTextureMapping_UV
        aiTextureMapping_SPHERE
        aiTextureMapping_CYLINDER
        aiTextureMapping_BOX
        aiTextureMapping_PLANE
        aiTextureMapping_OTHER



_aiPTI_Float = aiPTI_Float
_aiPTI_String = aiPTI_String
_aiPTI_Integer = aiPTI_Integer
_aiPTI_Buffer = aiPTI_Buffer