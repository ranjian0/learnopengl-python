cdef extern from "postprocess.h" nogil:
    cdef enum aiPostProcessSteps:
        aiProcess_CalcTangentSpace
        aiProcess_JoinIdenticalVertices
        aiProcess_MakeLeftHanded
        aiProcess_Triangulate
        aiProcess_RemoveComponent
        aiProcess_GenNormals
        aiProcess_GenSmoothNormals
        aiProcess_SplitLargeMeshes
        aiProcess_PreTransformVertices
        aiProcess_LimitBoneWeights
        aiProcess_ValidateDataStructure
        aiProcess_ImproveCacheLocality
        aiProcess_RemoveRedundantMaterials
        aiProcess_FixInfacingNormals
        aiProcess_SortByPType
        aiProcess_FindDegenerates
        aiProcess_FindInvalidData
        aiProcess_GenUVCoords
        aiProcess_TransformUVCoords
        aiProcess_FindInstances
        aiProcess_OptimizeMeshes
        aiProcess_OptimizeGraph
        aiProcess_FlipUVs
        aiProcess_FlipWindingOrder
        aiProcess_SplitByBoneCount
        aiProcess_Debone
        

