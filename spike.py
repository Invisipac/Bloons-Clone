import pygame as pg
from animation import Animation, spikes
from publisher import Publisher

#class for the spike traps

spikeImg = pg.image.load(".\data\spikes.png")

class Spike:#spike class
    spikeUsed = Publisher()

    def __init__(self, x, y, w) -> None:
        self.rect = pg.Rect(x*w , y*w , w, w)
        self.img = spikeImg
        self.damage = 25
        self.health = 10
        self.visible = True
        self.alive = True
        self.img = pg.transform.scale(self.img, (50, 50))
        self.spikeAnimation = Animation(self.rect.width, spikes)

    def draw_trap(self, screen: pg.Surface):#draws the spike
        screen.blit(self.img, self.rect)
        self.spikeAnimation.draw_animation(screen)
    
    def update_spike(self, screen):#updates the spike. only 10 enemies can hit it before it dies otherwise its too strong
        if self.health <= 0:
            self.visible = False
            self.alive = False
        if self.visible:
            self.draw_trap(screen)