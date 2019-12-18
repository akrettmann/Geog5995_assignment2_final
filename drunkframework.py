# -*- coding: utf-8 -*-
"""
Created on Sun Dec  8 13:13:11 2019

@author: Anak
"""

import random


class Drunk():
        """ This class models drunks wondering randomly home in the background
        area of an environment with buildings in it.
    
        """
        def __init__(self, environment,home,corners,density):
            """ 
            Determines the minimal and the maximal x,y coordinates of the own 
            home as well as for the pub.
            
            Finds out the size of environment in which the drunks operate
            and initialise drunks such that their coordinates stay within
            the limits of the pub within the environment. For randomising the 
            coordinates the house number  is provided as the "seed" value
            for the random function. 
            
            Places the drunk randomly inside the pub and records that location
            in the density map.
            
            Parameters
            ----------
            
            environment: list of lists, representing a 300x300 grid
            home       : integer representing the house number of drunks own home.
            corners    : list of dicts containing the minimal and the maximal 
                         x and y values of all the buildings in the environment.
                         the house numbers of the houses and the pub are the
                         keys for the dicts.
            density    : list of list, representing a 300x300 grid which records
                         how many times a drunks pass each location of the
                         environment.
            """
            self.environment = environment
            self.home = home
            self.density = density
            self.xminhome = corners[0].get(self.home)
            self.xmaxhome = corners[1].get(self.home)
            self.yminhome = corners[2].get(self.home)
            self.ymaxhome = corners[3].get(self.home)
            self.xminpub = corners[0].get(1)
            self.xmaxpub = corners[1].get(1)
            self.yminpub = corners[2].get(1)
            self.ymaxpub = corners[3].get(1)
            self.direction = ''
            
            random.seed(self.home)
            
            self._x = random.randint(self.xminpub,self.xmaxpub)
            self._y = random.randint(self.yminpub,self.ymaxpub)
            self.density[self._x][self._y] += 1
            self.width = len(environment)
            self.height = len(environment[0])
            
        def leaving_pub(self):
            """
            It is assumed that drunks have a general sense of where their
            home  is located. This methods determines a general direction by
            comparing the minimaland the maximal x an y coordinates of the
            drunks own home with the corresponding coordinates of the pub.
            The possible general directions are: se, ne, e, sw, nw, w, n, s.
            
            The method then moves the drunk to that side of the pub
            which is closest to his/her home, i.e. one of the coordinates is
            set such that the new location is just outside the pub's area
            (+1 or -1 of the border).
            
            Returns
            -------
            None.

            """
            if self.xminhome >= self.xmaxpub:
                self._x = self.xmaxpub+1
                if self.ymaxhome <= self.yminpub:
                    self.direction = 'se'
                elif self.yminhome >= self.ymaxpub:
                    self.direction = 'ne'
                else:
                    self.direction = 'e'
            elif self.xmaxhome <= self.xminpub:
                self._x = self.xminpub-1
                if self.ymaxhome <= self.yminpub:
                    self.direction = 'sw'
                elif self.yminhome >= self.ymaxpub:
                    self.direction = 'nw'
                else:
                    self.direction = 'w'
            elif self.xminhome < self.xmaxpub or self.xmaxhome > self.xminpub:
                if self.yminhome >= self.ymaxpub:
                    self._y = self.ymaxpub + 1
                    self.direction = 'n'
                elif self.ymaxhome <= self.yminpub:
                    self._y = self.yminpub - 1
                    self.direction = 's'
                    
            self.density[self._x][self._y] += 1
        
            
        def wonder_home(self):
            """
            This method moves the drunk agent one step by changing one of the 
            two coordinates randomly. However, the random move is guided in the
            sense that the choice of directions and their probability of being
            choosen is depending on the general direction in which the target
            is located. Buildings, that are in way also determine the choice
            of directions at their probability of being choosen as well as the
            edges of the environment. Only the own home, i.e. the target, can
            be entered.
            
            Returns
            -------
            None.

            """
            self.flag_e = False
            self.flag_n = False
            self.flag_s = False
            self.flag_w = False
            if self._x < self.width - 1:    
                de = self.environment[self._y ][self._x+1]
                if de != 0 and de != self.home :
                    self.flag_e = True
            else: 
                de = self.environment[self._y ][self._x]
                
            if self._y < self.height - 1:    
                dn = self.environment[self._y+1][self._x]
                if dn != 0 and dn != self.home :
                    self.flag_n = True
            else:
                dn = self.environment[self._y][self._x]
            
            if self._y > 0: 
                ds = self.environment[self._y-1][self._x]
                if ds != 0 and ds != self.home :
                    self.flag_s = True
            else:
                ds = self.environment[self._y][self._x]
                
            if self._x > 0:
                dw = self.environment[self._y ][self._x-1]
                if dw != 0 and dw != self.home :
                    self.flag_w = True
            else:
                dw = self.environment[self._y ][self._x]
            
            
            if self.direction == 'e':
                
                if self._x > self.xmaxhome :
                    self._x = self._x - 1
                else:
                    choice = ['n','e','e','s']
                    if (de != 0 and de != self.home)  or self._x == self.width-1:
                        choice.remove('e')
                        choice.remove('e')
                        choice.append('w')
                        choice.append('w')
                    if (dn != 0 and dn != self.home) or self._y == self.height-1:
                        choice.remove('n')
                    if  (ds != 0 and ds != self.home) or self._y == 1:
                        choice.remove('s')
                        choice.appen('n')
                    d = random.choice(choice)
                    if d == 'e':
                        self._x = self._x + 1
                    elif d == 'n':
                        if (self._y > self.ymaxhome and self.flag_e == False):
                            self._y = self._y - 1
                        else:
                            self._y = self._y + 1
                    elif d == 's':
                        if (self._y < self.yminhome and self.flag_e == False):
                            self._y = self._y + 1
                        else:
                            self._y = self._y - 1
                    elif d =='w':
                        self._x = self._x - 1
                    
                    
                            
            elif self.direction == 'w':
                
                if self._x < self.xminhome:
                    self._x = self._x + 1
                else:
                    choice = ['n','w','w','s']
                    if (dw != 0 and dw != self.home)  or self._x == 1:
                        choice.remove('w')
                        choice.remove('w')
                    if (dn != 0 and dn != self.home) or self._y == self.height:
                        choice.remove('n')
                    if (ds != 0 and ds != self.home) or self._y == 1:
                        choice.remove('s')
                    d = random.choice(choice)
                    if d == 'w':
                        self._x = self._x - 1
                    elif d == 'n':
                        if (self._y > self.ymaxhome and self.flag_w == False):
                            self._y = self._y - 1
                        else:
                            self._y = self._y + 1
                    elif d == 's':
                        if (self._y < self.yminhome and self.flag_w == False):
                            self._y = self._y + 1
                        else:
                            self._y = self._y - 1
                    
                            
            elif self.direction == 'n':
                
                if self._y > self.ymaxhome:
                    self._y = self._y - 1
                else:
                    choice = ['n','n','w','e']
                    if (dn != 0 and dn != self.home) or self._y == self.height:
                        choice.remove('n')
                        choice.remove('n')
                    if (de != 0 and de != self.home) or self._x  == self.width:
                        choice.remove('e')
                    if (dw != 0 and dw != self.home) or self._x  == 1:
                        choice.remove('w')
                    d = random.choice(choice)
                    if d == 'n':
                        self._y = self._y + 1
                    elif d == 'w':
                        if (self._x < self.xminhome and self.flag_n == False):
                            self._x = self._x + 1
                        else:
                            self._x = self._x - 1
                    elif d == 'e':
                        if (self._x > self.xmaxhome and self.flag_n == False):
                            self._x = self._x - 1
                        else:
                            self._x = self._x + 1
                
                
            elif self.direction == 's':
                if self._y <  self.yminhome:
                    self._y = self._y + 1
                else:
                    choice = ['s','s','w','e']
                    if (ds != 0 and ds != self.home) or self._y == 1:
                        choice.remove('s')
                        choice.remove('s')
                    if (de != 0 and de != self.home) or self._x  == self.width:
                        choice.remove('e')
                    if (dw != 0 and dw != self.home) or self._x  == 1:
                        choice.remove('w')
                    d = random.choice(choice)
                    if d == 's':
                        self._y = self._y - 1
                    elif d == 'w':
                        if (self._x < self.xminhome and self.flag_s == False):
                            self._x = self._x + 1
                        else:
                            self._x = self._x - 1
                    elif d == 'e':
                        if (self._x > self.xmaxhome and self.flag_s == False):
                            self._x = self._x - 1
                        else:
                            self._x = self._x + 1
                    
                
            elif self.direction == 'se':
                if self._y <  self.yminhome:
                    self._y = self._y + 1
                else: 
                    choice = ['s','s','n','e','e']
                    if (ds != 0 and ds != self.home) or self._y == 1:
                        choice.remove('s')
                        choice.remove('s')
                    if (de != 0 and de != self.home) or self._x  == self.width:
                        choice.remove('e')
                        choice.remove('e')
                    if (dn != 0 and dn != self.home) or self._y  == self.height:
                        choice.remove('n')
                    d = random.choice(choice)
                    if d == 's':
                        self._y = self._y - 1
                    elif d == 'n':
                        self._y = self._y + 1
                    elif d == 'e':
                        if (self._x > self.xmaxhome and self.flag_s == False):        
                            self._x = self._x - 1
                        else:
                            self._x = self._x + 1
                         
            elif self.direction == 'ne':
                if self._y >  self.ymaxhome:
                    self._y = self._y - 1
                else: 
                    choice = ['s','n','n','e','e']
                    if (ds != 0 and ds != self.home) or self._y == 0:
                        choice.remove('s')
                    if (de != 0 and de != self.home) or self._x  == self.width-1:
                        choice.remove('e')
                        choice.remove('e')
                    if (dn != 0 and dn != self.home) or self._y == self.height - 1 :
                        choice.remove('n')
                        choice.remove('n')
                    d = random.choice(choice)
                    if d == 's':
                        self._y = self._y - 1
                    elif d == 'n':
                        self._y = self._y + 1
                    elif d == 'e':
                        if (self._x > self.xmaxhome and self.flag_n == False):
                            self._x = self._x - 1
                        else:
                            self._x = self._x + 1  

            
            elif self.direction == 'sw':
                if self._y <  self.yminhome:
                    self._y = self._y + 1
                else:
                    choice = ['s','s','n','w','w']
                    if (ds != 0 and ds != self.home) or self._y == 1:
                        choice.remove('s')
                        choice.remove('s')
                    if (dw != 0 and dw != self.home) or self._x  == 1:
                        choice.remove('w')
                        choice.remove('w')
                    if (dn != 0 and dn != self.home) or self._y  == self.height:
                        choice.remove('n')
                    d = random.choice(choice)
                    if d == 's':
                        self._y = self._y - 1
                    elif d == 'n':
                        self._y = self._y + 1
                    elif d == 'w':
                        if (self._x < self.xminhome and self.flag_s == False):
                            self._x = self._x + 1
                        else:
                            self._x = self._x - 1
            
            elif self.direction == 'nw':
                if self._y >  self.ymaxhome:
                    self._y = self._y - 1
                else:
                    choice = ['s','n','n','w','w']
                    if (ds != 0 and ds != self.home) or self._y == 0:
                        choice.remove('s')
                    if (dw != 0 and dw != self.home) or self._x  == 0:
                        choice.remove('w')
                        choice.remove('w')
                    if (dn != 0 and dn != self.home) or self._y  == self.height-1:
                        choice.remove('n')
                        choice.remove('n')
                    d = random.choice(choice)
                    if d == 's':
                        self._y = self._y - 1
                    elif d == 'n':
                        self._y = self._y + 1
                    elif d == 'w':
                        if (self._x < self.xminhome and self.flag_n == False):
                            self._x = self._x + 1
                        else:
                            self._x = self._x - 1
                            
            self.density[self._x][self._y] += 1

        
        
        def getx(self):
            """
            This method retreives the x-coordinate of the location
            of the drunk.

            Returns
            -------
            integer:
                represents the current x-coordinate.

            """
            return self._x
        
        def gety(self):
            """
            This method retreives the y-coordinate of the location
            of the drunk.

            Returns
            -------
            integer:
                represents the current x-coordinate.

            """
            return self._y
            
