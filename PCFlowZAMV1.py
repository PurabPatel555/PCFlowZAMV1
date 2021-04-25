# -*- coding: utf-8 -*-
"""
VentExtract_gui_VC.py
"""
import numpy as np
import csv
from matplotlib import pyplot as plt
from matplotlib.pyplot import ion
ion()
import os
import sys
from Tkinter import *
import tkFileDialog as filedialog
from tqdm import tqdm

def browse():  
    filename = filedialog.askopenfilename(initialdir = "/", 
                                          title = "Select ASC File", 
                                          filetypes = (("ASC files", 
                                                        "*.ASC*"), 
                                                       ("all files", 
                                                        "*.*")))
                                          
    global RAW_DATA
    RAW_DATA = filename

    import time

    def boundgen(inputarr):
        inputstates= inputarr[17,:]
        inputpressures = inputarr[3,:]
        bounds = []
        start = 0
        end = 0
        begun = False

        for i in range(1,(len(inputstates)-2)):
            if (inputstates[i]==0 and inputstates[i+1]==0 and inputstates[i+2]==0):
                begun = True 
            if (begun and inputstates[i-1]==0 and inputstates[i]>0):
                j = i
                while inputarr[1,j]<0:
                    j = j+1
                start = j
            if (begun and inputstates[i-1]>0 and inputstates[i]==0 and inputstates[i+1]==0):
                end = i
                print(start)
                print(end)
                if (np.max(inputpressures[start:end])<3.5):
                    bounds.append([start,end])
                    #print(start)
                    #print(inputarr[0,start])
                    #print(end)
                    #print(inputarr[0,end])
                    #print("-----")
                start = 0
                end = 0
        return bounds
    
    x_extract = np.genfromtxt(RAW_DATA, dtype=str, deletechars="b'")
    x = np.transpose(x_extract)
    x = x[:,1:]
    x = x.astype(float)

    bounds = boundgen(x)
    print len(bounds)

    for i in bounds:

        boundl = i[0]
        boundr = i[1]
        
        plt.plot(x[3,boundl:boundr])
        plt.plot(x[17,boundl:boundr])

    for i in bounds:

        boundl = i[0]
        boundr = i[1]

        vts = [np.average(x[14,boundl:boundr])]
        vt = 0

        for i in range(boundl, boundr):
            if x[1,i]<0 and x[1,i+2]<0 and x[1,i+4]<0:
                print("break")
                print(x[1,i])
                print(boundl)
                print(i)
                print(boundr)
                break
            vt = vt + x[1,i]*1000/62.5
            vts.append(vt)
            
        if (len(vts)>3):
            with open('ZAMOutput2.csv', 'ab') as file:
                writer = csv.writer(file)
                writer.writerow(vts)
        else:
            print("too short")
                                                                                                          
#GUI For File Loading, Path Selection
window = Tk() 
   
window.title('NVR') 
   
window.geometry("500x250") 
   
window.config(background = "white") 
   
title = Label(window,  
                            text = "VC Flow Calculator", 
                            width = 50, height = 4,  
                            fg = "blue") 
   
       
button_start = Button(window,  
                        text = "Start", 
                        command = browse)  
   
button_exit = Button(window,  
                     text = "Exit", 
                     command = exit)  
   
title.grid(column = 1, row = 1) 
   
button_start.grid(column = 1, row = 2) 
   
button_exit.grid(column = 1,row = 3) 
   
window.mainloop() 
