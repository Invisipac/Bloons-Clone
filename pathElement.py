import pygame as pg
from publisher import Publisher
from spike import Spike

#class for the path elements where the spikes can be placed

class Path:
    boughtTrap = Publisher()
    def __init__(self, x, y, squarewidth, game) -> None:
        self.pos = (x, y)
        self.w = squarewidth
        self.rect = pg.Rect(x*self.w + 0.5, y*self.w + 0.5, self.w - 1, self.w - 1)
        self.trap = None
        self.hoverColour = (200, 200, 200)
        self.unhoverColour = (100, 100, 100)
        self.colour = self.unhoverColour
        self.buildables = {"spikes": Spike(self.pos[0], self.pos[1], squarewidth)}
        game.mouseHover.subscribe(self, self.on_mouse_hover)
        game.mouseClick.subscribe(self, self.on_mouse_click)

    def draw_path(self, screen: pg.Surface):#draws the path element
        pg.draw.rect(screen, self.colour, self.rect)
        if self.trap is not None:
            self.trap.update_spike(screen)

    def update_path(self, screen, enemy):#updates the path by drawing 
        self.draw_path(screen)

    def generate_trap(self, pos, player):#places the trap on the path element
        if self.trap is None:
            if player.selectedId is not None and player.selectedId in self.buildables:
                self.trap = self.buildables[player.selectedId]
                Path.boughtTrap.publish(player)

    def on_mouse_click(self, pos, player):#handles the mouse click event
        if self.isHovered:
            self.generate_trap(pos, player)
            for item in player.shop.items:
                item.isSelected = False
            player.selectedId = None

    def on_mouse_hover(self, mousePos):#handles the mouse hover event
        if self.rect.collidepoint(mousePos):
            self.colour = self.hoverColour
            self.isHovered = True
        else:
            self.colour = self.unhoverColour
            self.isHovered = False

    

