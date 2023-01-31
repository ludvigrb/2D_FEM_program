#imports:
import tkinter as tk
import Storage
from Classes import BeamSegment
from Classes import BarSegment
##----------------------------------------------------------------------------#
#                              Functions                                      #
#-----------------------------------------------------------------------------#
#dialogue box window for segment:
def openSegmentWindow(root,segmentType,canvas):
    # Toplevel object which will be treated as a new window
    segmentWindow = tk.Toplevel(root)
 
    # sets the title of the Toplevel widget
    segmentWindow.title("New Window")
 
    # sets the geometry of toplevel
    segmentWindow.geometry("230x280")
 
    #creating coordinate input titles
    tk.Label(segmentWindow,text =" Left x-coordinate: ",anchor='w').grid(row=0,column=0,sticky = 'W')
    tk.Label(segmentWindow,text =" Left y-coordinate: ",anchor='w').grid(row=1,column=0,sticky = 'W')
    tk.Label(segmentWindow,text =" Right x-coordinate: ",anchor='w').grid(row=2,column=0,sticky = 'W')
    tk.Label(segmentWindow,text =" Right y-coordinate: ",anchor='w').grid(row=3,column=0,sticky = 'W')
    #creating coordinate input fields:
    lxVal = tk.Entry(segmentWindow,width=5)
    lxVal.grid(row=0,column=1)
    lyVal = tk.Entry(segmentWindow,width=5)
    lyVal.grid(row=1,column=1)
    rxVal = tk.Entry(segmentWindow,width=5)
    rxVal.grid(row=2,column=1)
    ryVal = tk.Entry(segmentWindow,width=5)
    ryVal.grid(row=3,column=1)
    #creating input titles for width and height:
    tk.Label(segmentWindow,text =" Width:",anchor='w').grid(row=4,column=0,sticky = 'W')
    tk.Label(segmentWindow,text =" Height:",anchor='w').grid(row=5,column=0,sticky = 'W') 
    #creating width and height input fields:
    widthVal = tk.Entry(segmentWindow,width=5)
    widthVal.grid(row=4,column=1)
    heightVal = tk.Entry(segmentWindow,width=5)
    heightVal.grid(row=5,column=1)
    #creating input title for Youngs Modulus:
    tk.Label(segmentWindow,text =" Young's Modulus:",anchor='w').grid(row=6,column=0,sticky='W')
    #creating Young's input field
    EVal = tk.Entry(segmentWindow,width=5)
    EVal.grid(row=6,column=1)
    #creating title specifying number of elements:
    tk.Label(segmentWindow,text=" Number of elements:",anchor='w').grid(row=7,column=0,sticky='W')
    #creating input field for the number of elements:
    numEle = tk.Entry(segmentWindow,width=5)
    numEle.grid(row=7,column=1)
    #creating 'ok' button:
    okSegment = tk.Button(segmentWindow, text='ok', height=1, command = lambda: approveSegment(segmentWindow,segmentType,canvas,lxVal.get(),lyVal.get(),rxVal.get(),ryVal.get(),widthVal.get(),heightVal.get(),EVal.get(),numEle.get()))
    okSegment.grid(row=8,column=0)    
    #creating 'cancel' button:
    cancelSegment = tk.Button(segmentWindow, text='cancel', command=segmentWindow.destroy, height=1)
    cancelSegment.grid(row=8,column=1)
    
#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#
#defining function for when ok button is clicked:
def approveSegment(segmentWindow,segmentType,canvas,lx,ly,rx,ry,b,h,E,numEle):
    args = [lx,ly,rx,ry,b,h,E,numEle]
    if all(is_float(x) for x in args) == False:
        print('All entries have to be specified as numbers!')
        return
    if is_int(numEle) == False:
        print('The number of elements has to be an integer!')
        return
    if float(rx) <= float(lx):
        print('The right node must be to the right of the left node!')
        return
    else:
        #creating a line in canvas:
        canvas.create_line(lx, ly, rx, ry, width=3)
        #creating segment object and appending to segments list:
        if segmentType == 'Beam':
            Storage.segments.append(BeamSegment(Storage.globalCounter,Storage.coordToDOF))
        elif segmentType == 'Bar':
            Storage.segments.append(BarSegment(Storage.globalCounter,Storage.coordToDOF))
        #Setting the values of the segment:
        Storage.segments[-1].setCoordinates(float(lx), float(ly), float(rx), float(ry))
        Storage.segments[-1].setDimensions(float(b), float(h))
        Storage.segments[-1].setStiffness(float(E))
        Storage.segments[-1].createMesh(int(numEle))
        #updating counter and dict:
        Storage.globalCounter = Storage.segments[-1].globalCounter
        Storage.coordToDOF = Storage.segments[-1].coordToDOF
        #closing window
        segmentWindow.destroy()

#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#
#function to determine whether string is a float:
def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
#function determine whether string is an int:
def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False