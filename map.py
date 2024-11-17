import pygame as pg
from node import Node
from waypoint import Waypoint
from pathElement import Path

#class for the map of the game

class Map:
    def __init__(self, screenWidth) -> None:
        self.mapOutline = [#list to generate grid for the game
            ['################'],
            ['#0##############'],
            ['#*000000000*####'],
            ['###########*00*#'],
            ['##############0#'],
            ['#*000000000000*#'],
            ['#0##############'],
            ['#0##############'],
            ['#*0000*#########'],
            ['######0#########'],
            ['######*0000000*#'],
            ['################']
        ]

        self.nodeList = []#list of nodes on the map
        self.waypointList = []#list of waypoints on the map
        self.pathList = []#list of path elements on the map
        self.START = (1, 1)#start and end coordinates
        self.END = (14, 10)
        self.w = len(self.mapOutline[0][0])#dimensions
        self.h = len(self.mapOutline)
        self.squareWidth = screenWidth//self.w
    
    def draw_map(self, screen, W, H, waves):#funtion that draws the start and end square

        pg.draw.rect(screen, (0, 200, 200), (self.START[0]*self.squareWidth + 0.5, self.START[1]*self.squareWidth + 0.5, self.squareWidth - 1, self.squareWidth - 1))
        pg.draw.rect(screen, (255, 0, 0), (self.END[0]*self.squareWidth + 0.5, self.END[1]*self.squareWidth + 0.5, self.squareWidth - 1, self.squareWidth - 1))
        
        for n in self.nodeList:#draws nodes and pathelements
            n.draw_node(screen)
        for p in self.pathList:
            p.draw_path(screen)


    def init_elements(self, game):#function to populate the nodes and path elements based on the character in the map
        for i in range(self.h):
            for j in range(self.w):
                if self.mapOutline[i][0][j] == '#':
                    self.nodeList.append(Node(j, i, self.squareWidth, self.squareWidth, game))
                else:
                    if (i != self.END[1] or j != self.END[0]) and (i != self.START[1] or j != self.START[0]):
                        self.pathList.append(Path(j, i, self.squareWidth, game))
                        
        self.waypointList = [#list of waypoint for the enemies to follow
            Waypoint(1, 2, self.squareWidth),
            Waypoint(11, 2, self.squareWidth),
            Waypoint(11, 3, self.squareWidth),
            Waypoint(14, 3, self.squareWidth),
            Waypoint(14, 5, self.squareWidth),
            Waypoint(1, 5, self.squareWidth),
            Waypoint(1, 8, self.squareWidth),
            Waypoint(6, 8, self.squareWidth),            
            Waypoint(6, 10, self.squareWidth),
            Waypoint(14, 10, self.squareWidth)
        ]
        




        