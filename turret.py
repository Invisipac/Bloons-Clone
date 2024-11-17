import pygame as pg
from enemy import Enemy
from waveSpawner import Wave
from math import acos, degrees, asin
from bullet import Bullet, AoEBullet
pivot = (200, 200)

#THE BEST CLASS BECAUSE OF THE ROTATION
#class for the turrets that are placed on the nodes



class Turret:#turret class
    def __init__(self, x, y, squareWidth, dir, bullet, img, firerate) -> None:
        self.img = img

        self.bulletType = bullet

        self.range = 2.5*squareWidth
        self.closest = None

        self.pos = pg.math.Vector2(x*squareWidth + squareWidth//2, y*squareWidth + squareWidth//2)
        self.imgCenter = (self.pos[0], self.pos[1])

        self.rotatedImage = pg.image.load(".\data\Turret.png")
        self.rotatedImageRect = self.rotatedImage.get_rect(center = self.imgCenter)

        self.angle = 0
        self.center = pg.math.Vector2(self.img.get_rect(topleft=self.pos).center)
        self.dir = pg.math.Vector2(dir)

        self.fireRate = firerate
        self.endShot, self.startShot = 0, 0
        self.bullets = []


    def shoot(self, screen):#function to shoot the bullets. honestly works alright but not perfectly, a bit buggy sometimes
        if self.closest is not None:
            self.endShot = pg.time.get_ticks()
            if self.endShot - self.startShot > 1000/self.fireRate:
                newBullet = self.bulletType((self.pos + self.dir))
                newBullet.set_target(self.closest)
                self.bullets.append(newBullet)
                self.startShot = self.endShot
            
            if self.bullets != []:
                for b in self.bullets:
                    b.seek_target()
                    b.draw_bullet(screen)

    
    def calculate_angle_of_rotation(self):
        
        #The best function in the code despite being on of the shortest
        #Does the tracking for the balloons by taking the dot product between the vector from the turret to its target
        #and its own direction vector.
        #Then it takes the arcsin of the dot product to determine the angle of rotation and then the image is rotated.
        #Rotation is also a bit tricky since the surface needs to always be recentered around the position of the turret.

        if self.closest is not None:
            angle = 0
            self.dir = self.dir.normalize()

            enemyPos = (self.closest.pos - self.pos).normalize()

            cross = round(self.dir.cross(enemyPos), 5)
            angle = degrees(asin(cross))
        

            self.dir = self.dir.rotate(angle)

            self.angle += angle

    def find_closest_enemy(self, waves):#determines which enemy is closest to the turret to pick who to shoot
        for w in waves:
            for e in w.enemies:
                if self.closest is None:
                    if self.pos.distance_to(e.pos) < self.range and e.spawned and e.alive:
                        self.closest = e
                        return
                else:
                    if not self.closest.alive or self.pos.distance_to(self.closest.pos) > self.range:
                        self.closest = None



    def rotate_image(self):#rotates the image
        self.rotatedImage = pg.transform.rotate(self.img, -self.angle)
        self.rotatedImageRect = self.rotatedImage.get_rect(center = self.imgCenter)
    
    def draw_turret(self, screen: pg.Surface):#draws the turret
        screen.blit(self.rotatedImage, self.rotatedImageRect)


