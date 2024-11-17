import pygame as pg

#object for the enemies to move towards

class Waypoint:
    def __init__(self, x, y, squareWidth) -> None:
        self.pos = pg.math.Vector2(x*squareWidth + squareWidth//2, y*squareWidth + squareWidth//2)
    
    def draw_waypoint(self, screen):
        pg.draw.circle(screen, (255, 0, 0), self.pos, 5)