import pygame as pg
from publisher import Publisher
from animation import Animation, explosions


#class for the bullets shot by the tanks

class Bullet:

    bulletExploded = Publisher()

    def __init__(self, center) -> None:#constructor takes the starting position of the bullet
        self.center = pg.math.Vector2(center)
        self.speed = 8
        self.colour = (255, 0, 0)
        self.target = None
        self.r = 5
        self.visible = True
        self.moving = True
        self.damage = 35
        self.stopped = False

        self.explosionAnimation = Animation(50, explosions)

    def set_target(self, target):#function to set which enemy the bullet will follow
        self.target = target
    
    def bullet_explode(self):#checks if the bullet has reached the target
        if self.center.distance_to(self.target.pos) < self.speed:
            Bullet.bulletExploded.publish(self.explosionAnimation, self.center - (self.explosionAnimation.size//2, self.explosionAnimation.size//2))
            return True


    def seek_target(self):#function that moves the bullet towards the target
        if self.moving:
            moveVec = (self.target.pos - self.center).normalize()

            if not self.bullet_explode():
                self.center += moveVec*self.speed
            else:
                self.moving = False
                self.visible = False
                self.stopped = True

                if self.target.alive:
                    self.target.take_damage(self)


    def draw_bullet(self, screen):#draws the bullet on the screen
        if self.visible:
            pg.draw.circle(screen, self.colour, self.center, self.r)
        
        self.explosionAnimation.draw_animation(screen)


class AoEBullet(Bullet):#subclass for the bullet that does area of effect damage
    explodedInAoE = Publisher()
    def __init__(self, center) -> None:
        super().__init__(center)
        self.radius = 100
        self.damage = 15
        self.explosionAnimation = Animation(self.radius, explosions)
    

    def seek_target(self):#essentially the same function but sends an event when it has exploded so that enemies can check if they are in the radius
        if self.moving:
            moveVec = (self.target.pos - self.center).normalize()

            if not self.bullet_explode():
                self.center += moveVec*self.speed
            else:
                self.moving = False
                self.visible = False
                self.stopped = True
                AoEBullet.explodedInAoE.publish(self.radius, self.center, self)