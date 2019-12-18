# -*- coding: utf-8 -*-
"""
Created on Sun Dec  8 10:37:29 2019

@author: Anak
"""
#from PyQt5.uic import loadUiType
import the_way_home_mygui as gui
import drunkframework as dr
'''
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas)
from PyQt5.QtWidgets import QApplication
'''
import sys
import csv

environment = []
density = []
rowlist = []
buildings = {}
buildings_numbers =[]
drunkslist = {}
xmin = {}
ymin = {}
xmax = {}
ymax = {}
corners = []

def read_in_data_from_file (environment, pathname):
    """
    Open file and read data into list of lists

    Parameters
    ----------
    environment : list of lists
        the datastructure into which the content of the input file is read.
    pathname : string
        represents the file name including the path if its not in the current
        working directory.

    Returns
    -------
    environment : list of list
        each element in environment contains one complete row of input file.

    """
    f = open(pathname, newline='') 
    reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
    for row in reader: 
        rowlist = []
        for value in row: # A list of value
            rowlist.append(value)
        environment.append(rowlist)
    f.close()
    return environment

def write_outputfile(inputlist, outputfile):
    """
    Writes the content of the inputlist to the outputfile in csv format.

    Parameters
    ----------
    inputlist : list of lists
        each element of the inputlist contains one row to be written out to
        the outputfile.
    outpufile : file
        represents the file name including the path unless the file is in the
        current workin directory.

    Returns
    -------
    None.

    """
    #open and, if necessary, create output file 
    f = open(outputfile,'w',newline='')
    #writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
    writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
    #writer.writerow(inputlist)
    for row in inputlist:
            writer.writerow(row)
            
    f.close()
    return

if __name__ == '__main__':
    """
    Step 1:
        Reading in environment data from external file 'drunk.plan'.
        The funktion read_in_data_from_file returns a list of lists:
        each row of the input file is stored in a list which inturn
        is stored as an element in the final list. This datastructure
        is assigned to the variable 'environment'.
    """
    print ("Reading in environment data from external file")
    environment = read_in_data_from_file (environment, "drunk.plan")
    
    """
    Step 2:
        Initialise the density map with all zeros and identify all the
        buildings in the environment including the pub. All building are
        stored in a dictionary with the house numbers as keys (pub no. is one).
        Under each key a list of coordinates defining the area of the building
        is stored. Thereby the (y,x) representation of the list of list is
        changed to a (x,y) representation in the datastructure of the buildings.
    """    
    for i in range(len(environment[0])):
        density.append([])
        for j in range(len(environment)):
            density[i].append(0)
            value = int(environment[i][j])
            if (value != 0):       
                if (value not in buildings_numbers):
                    buildings_numbers.append(value)
                    buildings[value]=[[i,j]]
                else:
                    tmp=buildings.get(value)
                    tmp.append([i,j])
                    buildings.update([(value,tmp)]) 
   
    """
    Step 3:
        Find minimun and maximum x and y coordinates for the pub and each home
        respectively and store these values in dictionaries with house numbers
        as keys: xmin and ymin for minimal x and y values respectively, and
        xmax and ymax for maximal x and y values respectively. The list 
        'corners' contains these 4 structures. 
    """
    #buildings_numbers.sort()
    for i in buildings_numbers:
        res_min = [min(idx) for idx in zip(*buildings.get(i))]
        res_max = [max(idx) for idx in zip(*buildings.get(i))]
        xmin.update([(i,res_min[1])])
        xmax.update([(i,res_max[1])])
        ymin.update([(i,res_min[0])])
        ymax.update([(i,res_max[0])])
    corners = [xmin,xmax,ymin,ymax]
    """
    Step 4:
        Initialise all drunks and store them in a dictionary with house
        numbers as keys. The environment list, the own house number,the
        list 'corners' and the density map are passed to the Drunk class.
    """
    
    for i in buildings_numbers:
        if i != 1:    
            drunkslist.update([(i,dr.Drunk(environment,i,corners,density))])
    
    """
    Step 5:
        Generate Figure classes:
            fig0: empty Figure
            fig1: contains the environment with all buildings
            fig2: displays the environment with all buildings and the path
                  of each drunk from the pub to their home.
            fig3: displays the density map as a scatter plot.
    """
    fig0 = gui.Figure()
    
    fig1 = gui.Figure()
    ax1f1 = fig1.add_subplot(111)
    ax1f1.scatter([0,300,0,300],[0,0,300,300], color='white')
    buildings_numbers.sort()
    for i in buildings_numbers:    
        x = [xmin.get(i),xmax.get(i),xmax.get(i),xmin.get(i),xmin.get(i)]
        y = [ymin.get(i),ymin.get(i),ymax.get(i),ymax.get(i),ymin.get(i)]
        if i == 1:
            ax1f1.plot(x,y,color='lightblue', linewidth=4)
            ax1f1.text(xmin.get(1)+3,ymin.get(1)+7,'PUB')
        else:
            ax1f1.plot(x,y,color='green', linewidth=4)
            h = 'Home ' + str(i)
            ax1f1.text(xmin.get(i)-8,ymin.get(i)-8,str(h))
    
    
    fig2 = gui.Figure()
    
    ax1f2 = fig2.add_subplot(111)
    ax1f2.scatter([0,300,0,300],[0,0,300,300], color='white')
    
    xpub = [xmin.get(1),xmax.get(1),xmax.get(1),xmin.get(1),xmin.get(1)]
    ypub = [ymin.get(1),ymin.get(1),ymax.get(1),ymax.get(1),ymin.get(1)]
    ax1f2.plot(xpub,ypub,color='lightblue', linewidth=4)
    ax1f2.text(xmin.get(1)+3,ymin.get(1)+7,'PUB')
    
    #plotcolor ={10:'blue',210:'green',50:'red',60:'cyan',220:'magenta',70:'yellow'}
    plotcolor ={10:'blue'}

    #for i in [210]:
    #for i in [10,220,210,50,60,70]:
    for i in buildings_numbers:
        if i != 1:
            drunkslist.get(i).leaving_pub()
            xminhome = xmin.get(i)
            xmaxhome = xmax.get(i)
            yminhome = ymin.get(i)
            ymaxhome = ymax.get(i)
            x = [xminhome,xmaxhome,xmaxhome,xminhome,xminhome]
            y = [yminhome,yminhome,ymaxhome,ymaxhome,yminhome]
            ax1f2.plot(x,y,color='green', linewidth=4)
            h = 'Home ' + str(i)
            ax1f2.text(xminhome-8,yminhome-8,str(h))    
            x = []
            y = []
            at_home = False
            count =0
            while(at_home == False and count < 1000 ) : 
                drunkslist.get(i).wonder_home()
                px = drunkslist.get(i).getx()
                py = drunkslist.get(i).gety()
                count += 1
                x.append(px)
                y.append(py)
                if px  >= xminhome and px <= xmaxhome and py >= yminhome and py <= ymaxhome:
                    at_home = True
            
            ax1f2.plot(x,y,color=plotcolor.get(i), linewidth=1)
    

    fig3 = gui.Figure()
    
    ax1f3 = fig3.add_subplot(111)
    ax1f3.scatter([0,300,0,300],[0,0,300,300], color='white')
    x = []
    y = []
    for i in range(len(environment[0])):
        for j in range(len(environment)): 
            if density[i][j] != 0:
                x.append(i)
                y.append(j)    
    ax1f3.scatter(x,y, color='darkblue')
    
    """
    Step 6:
        Writing the density map to the file 'density.plan' in the current
        workin directtory in csv format.
    """
    print("Saving density map to file 'density.plan' ")
    write_outputfile(density, "density.plan")

    """
    Step 7:
        Launch the main event handler of PyQT5 by creating a instance of the
        class QApplication. Launching the custom frontend gui and adding figures
        0-3, and finally display the gui window.
    """
    app = gui.QApplication(sys.argv)
    main = gui.MyMain()
    main.addfig('Exit Application', fig0)
    main.addfig('Show Environment', fig1)
    main.addfig('Wondering Home', fig2)
    main.addfig('Density map',fig3)
  
    main.show()
    sys.exit(app.exec_())
