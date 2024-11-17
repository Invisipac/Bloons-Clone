import pygame as pg


#class for making animations

explosions = []#load in the different animations
for i in range(7):
    explosion = pg.image.load(f".\data\explosionframes\explosion{i + 1}.png")
    explosions.extend(2*[explosion])

spikes = []
for i in range(14):
    spike = pg.image.load(f".\data\Spikeframes\spike{i + 1}.png")
    spikes.extend([spike])


class Animation:
    def __init__(self, size, frames) -> None:#constructor takes animation size and which frames to use
        self.frames = frames.copy()
        self.coors = (0, 0)
        self.size = size
        for i in range(len(self.frames)):
            self.frames[i] = pg.transform.scale(self.frames[i], (self.size, self.size))
        
        self.animationIndex = 0
        self.startAnim = False
    
    def draw_animation(self, screen: pg.Surface):#loop that iterates every frame of the game and displays the next animation frame
        if self.startAnim:
            if self.animationIndex < len(self.frames):
                screen.blit(self.frames[self.animationIndex], self.coors)
                self.animationIndex += 1
            else:
                self.startAnim = False
    
    def set_coors(self, coors):#function to set coordinates of the animation
        self.coors = coors

