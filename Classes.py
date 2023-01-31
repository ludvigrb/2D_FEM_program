# Imports:
from math import sqrt
from math import sin as s
from math import cos as c
from math import atan
import numpy as np

#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#
class BeamSegment:
    def __init__(self,globalCounter,coordToDOF):
        self.globalCounter = globalCounter #takes in the global DOF number
                                           #thus far
        self.coordToDOF = coordToDOF #dictionary mapping DOF coordinates 
                                     #to global number 
                                     
        self.lx = None #left x-coordinate
        self.ly = None #left y coordinate
        self.rx = None #right x coordinate
        self.ry = None #right y coordinate
        self.E = None #youngs Modulus
        self.b = None #width of cross-section
        self.h = None #height of cross-section
        self.A = None #area of cross-section
        self.I = None #second moment of inertia
        self.L = None #length of beam segment
        self.angle = None #angle of the beam
        self.numElements = None #number of elements in beam segment
        self.elementLength = None #length of each element in beam segment
        self.elements = [] #list of element objects

        
    def setCoordinates(self,lx,ly,rx,ry):
        self.lx = lx
        self.ly = ly
        self.rx = rx
        self.ry = ry
        self.L = sqrt((rx-lx)**2 + (ry-ly)**2) # pythagoras
        self.angle = atan((ry-ly) / (rx-lx))
        
    def setDimensions(self,b,h):
        self.b = b
        self.h = h
        self.A = b*h
        self.I = b*h**3/12
        
    def setStiffness(self,E):
        self.E = E
        
    def checkIfIncomplete(self):
        attributes = [self.lx,self.ly,self.rx,self.ry,self.E,self.b,self.h]
        return any(x is None for x in attributes)
        
    def createMesh(self,numElements):
        #checks if the necessary values have been specified before meshing:
        if self.checkIfIncomplete() == True:
            print("The beam must be completely defined before meshing!")
            return
        else: #create nodes with DOFS and elements and add them to lists:
            self.numElements = numElements
            self.elementLength = self.L/numElements
            #create DOFS with local and global numbering, and if the global
            #DOF coordinates already exists, the global numbering is taken
            #from the existing DOF:
            for i in range(numElements):
                #coordinates of node to the left of the element:
                x_left = self.lx + (self.rx-self.lx)*(1/numElements)*i
                y_left = self.ly + (self.ry-self.ly)*(1/numElements)*i
                #coordinates of node to the right of the element:
                x_right = self.lx + (self.rx-self.lx)*(1/numElements)*(i+1)
                y_right = self.ly + (self.ry-self.ly)*(1/numElements)*(i+1)
                
                #left node#
                #checks if global left x-DOF already exists in dictionary:
                if 'xDOF: '+str([x_left,y_left]) in self.coordToDOF: 
                    left_xDOF = DOF(0,self.coordToDOF['xDOF: '+str([x_left,y_left])])
                else:
                    left_xDOF = DOF(0,self.globalCounter)
                    self.coordToDOF['xDOF: '+str([x_left,y_left])] = self.globalCounter
                    self.globalCounter += 1
                #checks if global left y-DOF already exists in dictionary:
                if 'yDOF: '+str([x_left,y_left]) in self.coordToDOF:
                    left_yDOF = DOF(1,self.coordToDOF['yDOF: '+str([x_left,y_left])])
                else:
                    left_yDOF = DOF(1,self.globalCounter)
                    self.coordToDOF['yDOF: '+str([x_left,y_left])] = self.globalCounter
                    self.globalCounter += 1    
                #checks if global left w-DOF already exists in dictionary:
                if 'wDOF: '+str([x_left,y_left]) in self.coordToDOF:
                    left_wDOF = DOF(2,self.coordToDOF['wDOF: '+str([x_left,y_left])])
                else:
                    left_wDOF = DOF(2,self.globalCounter)
                    self.coordToDOF['wDOF: '+str([x_left,y_left])] = self.globalCounter
                    self.globalCounter += 1 
                    
                #right node#    
                #checks if global right x-DOF already exists in dictionary:
                if 'xDOF: '+str([x_right,y_right]) in self.coordToDOF: 
                    right_xDOF = DOF(3,self.coordToDOF['xDOF: '+str([x_right,y_right])])
                else:
                    right_xDOF = DOF(3,self.globalCounter)
                    self.coordToDOF['xDOF: '+str([x_right,y_right])] = self.globalCounter
                    self.globalCounter += 1
                #checks if global right y-DOF already exists in dictionary:
                if 'yDOF: '+str([x_right,y_right]) in self.coordToDOF:
                    right_yDOF = DOF(4,self.coordToDOF['yDOF: '+str([x_right,y_right])])
                else:
                    right_yDOF = DOF(4,self.globalCounter)
                    self.coordToDOF['yDOF: '+str([x_right,y_right])] = self.globalCounter
                    self.globalCounter += 1    
                #checks if global right w-DOF already exists in dictionary:
                if 'wDOF: '+str([x_right,y_right]) in self.coordToDOF:
                    right_wDOF = DOF(5,self.coordToDOF['wDOF: '+str([x_right,y_right])])
                else:
                    right_wDOF = DOF(5,self.globalCounter)
                    self.coordToDOF['wDOF: '+str([x_right,y_right])] = self.globalCounter
                    self.globalCounter += 1 
                    
                #adding left DOFS to left node:
                leftNode = Node(x_left,y_left,left_xDOF,left_yDOF,wDOF=left_wDOF)
                #adding right DOFS to right node:
                rightNode = Node(x_right,y_right,right_xDOF,right_yDOF,wDOF=right_wDOF)
                #adding nodes to element and appending to list:
                self.elements.append(BeamElement(self.E,self.I,self.A,self.L,
                                                 self.angle,leftNode,rightNode))   
                            
#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#
class BeamElement: #6 DOFS, clockwise rotation
    def __init__(self,E,I,A,L,o,leftNode,rightNode):
        #o refers to the angle of the beam in radians
        #the stiffness matrix for a 6 DOF beam element (not transformed):
        a = E*A/L
        b = E*I/(L**3)
        K_temp = np.array([[a,0,0,-a,0,0],
                           [0,12*b,-6*b*L,0,-12*b,-6*b*L],
                           [0,-6*b*L,4*b*L**2,0,6*b*L,2*b*L**2],
                           [-a,0,0,a,0,0],
                           [0,-12*b,6*b*L,0,12*b,6*b*L],
                           [0,-6*b*L,2*b*L**2,0,6*b*L,4*b*L**2]])
        #tranformation matrix:
        T = np.array([[c(o),s(o),0,0,0,0],
                      [-s(o),c(o),0,0,0,0],
                      [0,0,1,0,0,0],
                      [0,0,0,c(o),s(o),0],
                      [0,0,0,-s(o),c(o),0],
                      [0,0,0,0,0,1]])
        #the transformed stiffness matrix w.r.t global DOFS
        self.K = np.matmul(np.matmul(np.transpose(T),K_temp),T)
        self.leftNode = leftNode
        self.rightNode = rightNode
        
        
        
#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------# 
class BarSegment:
    def __init__(self,globalCounter,coordToDOF):
        self.globalCounter = globalCounter #takes in the global DOF number
                                           #thus far
        self.coordToDOF = coordToDOF #dictionary mapping DOF coordinates 
                                     #to global number 
        
        self.lx = None #left x-coordinate
        self.ly = None #left y coordinate
        self.rx = None #right x coordinate
        self.ry = None #right y coordinate
        self.E = None #youngs Modulus
        self.b = None #width of cross-section
        self.h = None #height of cross-section
        self.A = None #area of cross-section
        self.L = None #length of bar
        self.angle = None #angle of the bar
        self.numElements = None #number of elements in bar segment
        self.elementLength = None #length of each element in bar segment
        self.elements = [] #list of element objects
    
    def setCoordinates(self,lx,ly,rx,ry):
        self.lx = lx
        self.ly = ly
        self.rx = rx
        self.ry = ry
        self.L = sqrt((rx-lx)**2 + (ry-ly)**2) # pythagoras
        self.angle = atan((ry-ly) / (rx-lx))
        
    def setDimensions(self,b,h):
        self.b = b
        self.h = h
        self.A = b*h
        
    def setStiffness(self,E):
        self.E = E
        
    def checkIfIncomplete(self):
        attributes = [self.lx,self.ly,self.rx,self.ry,self.E,self.b,self.h]
        return any(x is None for x in attributes)
        
    def createMesh(self,numElements):
        #checks if the necessary values have been specified before meshing:
        if self.checkIfIncomplete() == True:
            print("The bar must be completely defined before meshing!")
            return
        else: #create nodes with DOFS and elements and add them to lists:
            self.numElements = numElements
            self.elementLength = self.L/numElements
            #create DOFS with local and global numbering, and if the global
            #DOF coordinates already exists, the global numbering is taken
            #from the existing DOF:
            for i in range(numElements):
                #coordinates of node to the left of the element:
                x_left = self.lx + (self.rx-self.lx)*(1/numElements)*i
                y_left = self.ly + (self.ry-self.ly)*(1/numElements)*i
                #coordinates of node to the right of the element:
                x_right = self.lx + (self.rx-self.lx)*(1/numElements)*(i+1)
                y_right = self.ly + (self.ry-self.ly)*(1/numElements)*(i+1)
                
                #left node#
                #checks if global left x-DOF already exists in dictionary:
                if 'xDOF: '+str([x_left,y_left]) in self.coordToDOF: 
                    left_xDOF = DOF(0,self.coordToDOF['xDOF: '+str([x_left,y_left])])
                else:
                    left_xDOF = DOF(0,self.globalCounter)
                    self.coordToDOF['xDOF: '+str([x_left,y_left])] = self.globalCounter
                    self.globalCounter += 1
                #checks if global left y-DOF already exists in dictionary:
                if 'yDOF: '+str([x_left,y_left]) in self.coordToDOF:
                    left_yDOF = DOF(1,self.coordToDOF['yDOF: '+str([x_left,y_left])])
                else:
                    left_yDOF = DOF(1,self.globalCounter)
                    self.coordToDOF['yDOF: '+str([x_left,y_left])] = self.globalCounter
                    self.globalCounter += 1    
                    
                #right node#    
                #checks if global right x-DOF already exists in dictionary:
                if 'xDOF: '+str([x_right,y_right]) in self.coordToDOF: 
                    right_xDOF = DOF(2,self.coordToDOF['xDOF: '+str([x_right,y_right])])
                else:
                    right_xDOF = DOF(2,self.globalCounter)
                    self.coordToDOF['xDOF: '+str([x_right,y_right])] = self.globalCounter
                    self.globalCounter += 1
                #checks if global right y-DOF already exists in dictionary:
                if 'yDOF: '+str([x_right,y_right]) in self.coordToDOF:
                    right_yDOF = DOF(3,self.coordToDOF['yDOF: '+str([x_right,y_right])])
                else:
                    right_yDOF = DOF(3,self.globalCounter)
                    self.coordToDOF['yDOF: '+str([x_right,y_right])] = self.globalCounter
                    self.globalCounter += 1    
            
                    
                #adding left DOFS to left node:
                leftNode = Node(x_left,y_left,left_xDOF,left_yDOF)
                #adding right DOFS to right node:
                rightNode = Node(x_right,y_right,right_xDOF,right_yDOF)
                #adding nodes to element and appending to list:
                self.elements.append(BarElement(self.E,self.A,self.L,
                                                 self.angle,leftNode,rightNode)) 
        
#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#
class BarElement:
    def __init__(self,E,A,L,o,leftNode,rightNode):
        #o refers to the angle of the bar in radians
        #the stiffness matrix for a 4 DOF bar element:
        self.K = E*A/L*np.array([[c(o)**2,c(o)*s(o),-c(o)**2,-c(o)*s(o)],
                                 [c(o)*s(o),s(o)**2,-c(o)*s(o),-s(o)**2],
                                 [-c(o)**2,-c(o)*s(o),c(o)**2,c(o)*s(o)],
                                 [-c(o)*s(o),-s(o)**2,c(o)*s(o),s(o)**2]])
        self.leftNode = leftNode
        self.rightNode = rightNode


#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#
class Node:
    def __init__(self,x,y,xDOF,yDOF,wDOF=None):
        self.x = x #original global x-ccordinate
        self.y = y #original global y-coordinate
        self.xDOF = xDOF #translation DOF in the x-direction (object)
        self.yDOF = yDOF #translation DOF in the y-direction (object)
        self.wDOF = wDOF #rotational DOF (object)
        
#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#
class DOF:
    def __init__(self,localNum,globalNum):
        self.localNum = localNum #local DOF numbering
        self.globalNum = globalNum #global DOF numbering
        self.val = None
        
#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#
class pointLoad:
    def __init__(self,F,xloc,yloc,xdir,ydir):
        self.F = F
        self.xloc = xloc
        self.yloc = yloc
        self.xdir = xdir
        self.ydir = ydir
        
#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#        
class pointMoment:
    def __init__(self,M,xloc,yloc):
        self.M = M
        self.xloc = xloc
        self.yloc = yloc
        
#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#
class lineLoad:
    def __init__(self,lx,ly,rx,ry,intensity1,intensity2):
        self.lx = lx
        self.ly = ly
        self.rx = rx
        self.ry = ry
        self.intensity1 = intensity1
        self.intensity2 = intensity2