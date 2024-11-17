import pygame as pg
from turret import Turret
from bullet import Bullet, AoEBullet
from publisher import Publisher


#class for the nodes on the map. These are tiles where you can place turrets

basicTankImg = pg.image.load(".\data\Turret.png")
basicTankImg = pg.transform.scale(basicTankImg, (basicTankImg.get_width()//2, basicTankImg.get_height()//2))

aoeTankImg = pg.image.load(".\data\Aoeturret.png")
aoeTankImg = pg.transform.scale(aoeTankImg, (aoeTankImg.get_width()//2, aoeTankImg.get_height()//2))


class Node:#class for nodes

    boughtTurret = Publisher()

    def __init__(self, x, y, w, h, game) -> None:
        self.w = w
        self.pos = (x, y)
        self.rect = pg.Rect(x*w + 0.5, y*h + 0.5, w - 1, h - 1)
        self.colour = 0
        self.hoverColour = (0, 150, 0)
        self.unhoverColour = (0, 255, 0)
        self.turret = None
        self.buildables = {"basictank": Turret(self.pos[0], self.pos[1], self.w, (0, -1), Bullet, basicTankImg, 4), "aoetank": Turret(self.pos[0], self.pos[1], self.w, (0, -1), AoEBullet, aoeTankImg, 2)}
        self.isHovered = False
        game.mouseHover.subscribe(self, self.on_mouse_hover)#subscribes to mousehover and mouseclick events
        game.mouseClick.subscribe(self, self.on_mouse_click)

    def draw_node(self, screen):#draws the node
        pg.draw.rect(screen, self.colour, self.rect)
        
    
    def update_node(self, screen, waves):#updates the turret on the node
        if self.turret is not None:
            self.turret.find_closest_enemy(waves)
            self.turret.calculate_angle_of_rotation()
            self.turret.rotate_image() 
            self.turret.shoot(screen)
            self.turret.draw_turret(screen)
    
    def generate_turret(self, pos, player):#places the turret on the node
        if self.turret is None:
            if player.selectedId is not None and player.selectedId in self.buildables:
                self.turret = self.buildables[player.selectedId]
                Node.boughtTurret.publish(player)
        
    def on_mouse_click(self, pos, player):#handles the mouseclick event
        if self.isHovered:
            self.generate_turret(pos, player)
            for item in player.shop.items:
                item.isSelected = False
            player.selectedId = None

    def on_mouse_hover(self, mousePos):#handles the mousehover event
        if self.rect.collidepoint(mousePos):
            self.colour = self.hoverColour
            self.isHovered = True
        else:
            self.colour = self.unhoverColour
            self.isHovered = False
    
    