#imports:
import numpy as np
import tkinter as tk
import Storage
from GUI_functions import openSegmentWindow
from Assembly import assembleBeam
#-----------------------------------------------------------------------------#
#                              Main                                           #
#-----------------------------------------------------------------------------#
#root window:
root = tk.Tk()
#determining window size:
root.geometry('1900x950') 
#creating a title:
title = tk.Label(root, text='My FEM software')
#shoving it onto the screen:
title.grid(row=0,column=0)

#-----------------------------------------------------------------------------#
#creating a canvas#
myCanvas = tk.Canvas(root, bg="white", height=500, width=800)
myCanvas.grid(row=2,column=0,columnspan=2)

#-----------------------------------------------------------------------------#    
#creating dropdown menu:
# datatype of menu text
clicked = tk.StringVar()
#dropdown options:
options = ['Beam','Bar']
# initial menu text
clicked.set( "Beam")
# Create Dropdown menu
drop = tk.OptionMenu( root , clicked , *options, command= lambda _: openSegmentWindow(root,clicked.get(),myCanvas))
drop.grid(row=0,column=2)
drop.config(width=7)

#-----------------------------------------------------------------------------#
#the loop that runs the program until it is exited:
root.mainloop()

#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#
#testing:
print(Storage.segments[0].elements[2].rightNode.wDOF.globalNum)
print(Storage.segments[0].elements[2].rightNode.wDOF.localNum)

print(Storage.segments[1].elements[0].leftNode.wDOF.globalNum)
print(Storage.segments[1].elements[0].leftNode.wDOF.localNum)

sysK = np.zeros([Storage.globalCounter,Storage.globalCounter])
for segment in Storage.segments:
    for ele in segment.elements:
        sysK = assembleBeam(sysK,0,ele)

print(sysK.shape)
