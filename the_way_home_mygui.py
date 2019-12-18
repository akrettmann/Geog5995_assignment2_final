# -*- coding: utf-8 -*-
"""
Created on Sun Dec  8 13:13:11 2019

@author: Anak
"""
from PyQt5.uic import loadUiType
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas)
from PyQt5.QtWidgets import QApplication

"""
Load PyQT5-Designer class definitions
"""
Ui_MyMainWindow, QMainWindow = loadUiType('my_window.ui')

        
class MyMain(QMainWindow, Ui_MyMainWindow):
    """This class defines the application logic for a GUI construction 
    
    This class defines the application logic based on the GUI defined as
    the front end. The GUI is defined through the base classes Ui_MyMainWindow
    and QMainwindow. The class QMainWindow is part of every QT application ( at
    least one is need) and generates a window with the normal windows decorations,
    i.e. zou you can drag it around and resize it like any normal window.
    
    The class Ui_MyMainWindow is a subclass of QMainWindow customizing the 
    standard windows as created by an instance of QMainWindow. Ui_MyMainWindow 
    defines the overall GUI design while the class MyMain contains the necessary
    application logic to display matplotlib data plots and a plot selection
    list.    
    """
    def __init__(self, ):
        """
        Initialises an empty dictionary to store Figure instances by name.
        Clicks on list items are associated with the method changefig. 
        An empty figure instance is added to the plotting window during
        initialisation, such that the method changefig can remove the current 
        figure.
        """
        super(MyMain, self).__init__()
        self.setupUi(self)
        self.fig_dict = {}

        self.mplfigslist.itemClicked.connect(self.changefig)

        fig = Figure()
        self.addmpl(fig)
        

    def changefig(self, item):
        """
        Removes the current plot and displays the new one associated with the
        item clicked. 

        Parameters
        ----------
        item : instance of class QListWidgetItem, which defines a method 'text',
                which simply returns the text of the selectd item.
        """
        text = item.text()
        if text == 'Exit Application':
            self.close()
        else:    
            self.rmmpl()
            self.addmpl(self.fig_dict[text])

    def addfig(self, name, fig):
        """
        The Figure fig is added to the dictionary under the 'name' key.
        The name key is added to the list Widget 'mplfigslist' an instance of
        QT class QListWidget.

        Parameters
        ----------
        name : string 
            denoting the name of Figure instance.
        fig : Figure
              Figure instance associated with keyword 'name' .

        """
        self.fig_dict[name] = fig
        self.mplfigslist.addItem(name)

    def addmpl(self, fig):
        """
        Displays the Figure instance fig in the matplotlib container, a
        generic QT container widget. A vertical layout named 'mplvl' is 
        enforced for any encapsulated widgets in this container. This 
        instance of QT class QVBoxLayout has an 'addWidget' method for
        adding new vertically alligned widgets into the matplolib container 
        widget. Thismethd is used to upload the FigureCanvas object 'canvas',
        which contains the plot.

        Parameters
        ----------
        fig : Figure instance
        """
        self.canvas = FigureCanvas(fig)
        self.mplvl.addWidget(self.canvas)
        self.canvas.draw()

    def rmmpl(self):
        """
        Removes the container widget with the current plot from the
        GUI window and closes the canvas containing that current plot.
        The method 'removeWidget' of the 'mplv' QVBoxLayout is used.

        """
        self.mplvl.removeWidget(self.canvas)
        self.canvas.close()


