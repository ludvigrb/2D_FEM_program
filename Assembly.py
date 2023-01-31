#imports
import numpy as np

#REMEMEBER TO INCORPORATE DBC and RHS ASWELL!
#-----------------------------------------------------------------------------#
def assembleBeam(sysK,sysRHS,ele):
    rel = BeamEleToSys(ele)
    print(rel)
    for i in range(6):
        for j in range(6):
            sysK[int(rel[i][1])][int(rel[j][1])] += ele.K[i][j]
    return sysK
    
#-----------------------------------------------------------------------------#    
def assembleBar(sysK,sysRHS,ele):
    rel = BarEleToSys(ele)
    for i in range(4):
        for j in range(4):
            sysK[rel[i][1]][rel[j][1]] += ele.K[i][j]
    return sysK
    
#-----------------------------------------------------------------------------#
def BeamEleToSys(ele):    
    #ele is a 6 DOF beam element (object)
    rel = np.zeros([6,2])
    #local numbering:
    for i in range(6):
        rel[i][0] = i
    #global numbering
    rel[0][1] = ele.leftNode.xDOF.globalNum
    rel[1][1] = ele.leftNode.yDOF.globalNum
    rel[2][1] = ele.leftNode.wDOF.globalNum
    rel[3][1] = ele.rightNode.xDOF.globalNum
    rel[4][1] = ele.rightNode.yDOF.globalNum
    rel[5][1] = ele.rightNode.wDOF.globalNum
    return rel
#-----------------------------------------------------------------------------#    
def BarEleToSys(ele):
    #ele is a 4 DOF bar element (object)
    rel = np.zeros([4,2])
    #local numbering:
    for i in range(4):
        rel[i][0] = i
    #global numbering
    rel[0][1] = ele.leftNode.xDOF.globalNum
    rel[1][1] = ele.leftNode.yDOF.globalNum
    rel[2][1] = ele.rightNode.xDOF.globalNum
    rel[3][1] = ele.rightNode.yDOF.globalNum
    return rel
