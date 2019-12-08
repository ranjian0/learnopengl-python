from cScene cimport aiScene

cdef extern from "cimport.h" nogil:
    const aiScene *aiImportFile(const char *pFile, unsigned int pFlags) except +
    void aiReleaseImport(const aiScene* pScene)
    const char* aiGetErrorString()

