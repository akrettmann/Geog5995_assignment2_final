# Geog5995_assignment2_final

Assessment-2-GEOG5995M

Agent based model of agents (drunks) each moving randomly from on central location (pub) to their 
specific location (home).

About

This practicals implements an agent based model acting in an environment with a central central
building (pub) and a number of dwellings (homes) distributed in all directions around it. 

The agents (drunks) are moving randomly, however, in some form of guided fashion, from within
the pub to their individuals home thereby circumventing the homes that may be in the way. 

The agents "know" the general direction in which their homes lie: north, south, east, west,
north-east, south-east, north-west or south-west. The random moves are therefore guided in the
sense that certain directions have lower probabilty to be chosen or are even excluded at each step. 

The practical has been implemented in Python using the program development environment Spider
and the graphical user interface (GUI) designer QT Designer. 

The model takes in a raster input file consisting of 300 rows and 300 columns of integer values
to be taking as an environment grid of (y,x) coordinates in which agents (e.g. drunks) and resources 
(e.g. commercial buildings and dwellings) are placed. The numbers in the grid represent the buildings
(integer values greater than zero) and the background area where the agents can move around(denoted 
by zero).

The commercial building, i.e. the pub, is assumed to be denoted by the integer value 1.
The interger numbers for the dwellings are denoted by integer numbers other than 1. The agent number
are assumed to correspond to the numbers of the dwellings. The current location of an agent is 
represented by its corresponding coordinates on the grid. The agents can only move on the background
of the grid denoted by the number zero.

The input raster file of the town plan "drunk.plan" contains 25 houses with number 250, 240,..etc...10.
The implementation indentifies the house and their corresponding house numbers from the inputfile,
such that any numbers of houses and house numbers can be processed.

The program also records all the locations on the grid where agents have passed through and how
many agents passed through any of these points. Finally this information is written out to the file
"density.plan".

Via the GUI of the program three matplotlib graphs can be alternatively shown:
1. The environment with all the building.
2. The way home of all mthe agents.
3. The density map  

Installation and Execution
The program, the gui definition file "my_window.ui" and the raster input file 'plan.txt' can be 
accessed from the following github repository:

https://github.com/akrettmann/Geog5995_assignment2_final

The main program can be executed in the Spider development environment.


Authors and Acknowledgement
This practical has been completed by Anna Krettmann as part of Assignment 2, GEOG5995 Programming for Social Science.

License
The license can be found at: https://github.com/akrettmann/Geog5995_assignment2_final

Authors and Acknowledgement
This practical has been completed by Anna Krettmann as part of Assignment 2, GEOG5995 Programming for Social Science.
