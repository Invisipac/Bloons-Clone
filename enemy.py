import pygame as pg
from publisher import Publisher
from bullet import Bullet, AoEBullet
from spike import Spike

#class for the enemies 
class Enemy:

    enemyKilled = Publisher()
    enemyReachedEnd = Publisher()

    def __init__(self, start, squareWidth) -> None:
        self.pos = pg.math.Vector2(start[0]*squareWidth + squareWidth//2, start[1]*squareWidth + squareWidth//2)
        self.r = 10
        self.squareWidth = squareWidth
        self.colour = (0, 0, 255)
        self.waypointIndex = 0
        self.speed = 2
        self.moving = False
        self.visible = False
        self.health = 100
        self.spawned = False
        self.alive = True
        self.damage = 1
        self.hitSpike = False
        self.curSpike = None
        self.moveVec: pg.math.Vector2

        AoEBullet.explodedInAoE.subscribe(self, self.inside_aoe)#subscribes to the event of the aoe explosion
    
    def inside_aoe(self, radius, center, bullet):#when the aoe event publishes, this function checks if the bullet is in the aoe and then the enemy will take damage
        if self.pos.distance_to(center) < radius:
            if self.alive:
                self.take_damage(bullet)


    def draw_enemy(self, screen):#draws the enemy on the screen
        if self.visible:
            pg.draw.circle(screen, (255, 255, 255), self.pos, self.r + 1, 1)
            pg.draw.circle(screen, self.colour, self.pos, self.r)
    
    def move_enemy(self, waypoints, wave):#moves the enemy towards the waypoints and increases the waypoint index once it reaches the waypoint
        
            if self.moving:
                if self.pos.distance_to(waypoints[self.waypointIndex].pos) < 1:
                    self.waypointIndex += 1
                if self.waypointIndex < len(waypoints):
                    self.moveVec = pg.math.Vector2(waypoints[self.waypointIndex].pos - self.pos).normalize()
                    
                    self.pos += self.moveVec*self.speed
                
                else:
                    self.spawned = False
                    self.visible = False
                    self.alive = False
                    wave.enemies.remove(self)
                    Enemy.enemyReachedEnd.publish(self.damage)#publishes an event when enemy reaches the end so that the player loses health


    def check_spike_collision(self, spikes):#checks for collisions with the spikes
        for s in spikes:
            if s is not None:
                if s.rect.collidepoint(self.pos) and self.alive:
                    if not self.hitSpike and s.alive:
                        self.curSpike = s
                        s.spikeAnimation.animationIndex = 0
                        Spike.spikeUsed.publish(s.spikeAnimation, (s.rect.x, s.rect.y))
                        s.health -= 1
                        self.take_damage(s)
                        self.hitSpike = True
                else:
                    if s == self.curSpike:
                        self.hitSpike = False

    def take_damage(self, damageItem):#function that subtracts health from the enemy and takes the item doing damage as a parameter
        self.health -= damageItem.damage

        if self.health <= 0:
            Enemy.enemyKilled.publish(self)
            self.moving = False
            self.visible = False
            self.alive = False
    
    def update(self, waypoints, screen, spikes, wave):#update function to move, draw, and check spike collisions for enemy
        self.move_enemy(waypoints, wave)
        self.draw_enemy(screen)
        self.check_spike_collision(spikes)

        

class TripleEnemy(Enemy):#subclass of enemy for the red enemy that explodes into three smaller ones

    tripleExploded = Publisher()

    def __init__(self, start, squareWidth) -> None:
        super().__init__(start, squareWidth)
        self.triple = []
        self.damage = 5
        self.colour = (100, 0, 0)
    
    def is_exploded_triple(self):#funcion checks if the balloon has died and then creates three new ones and then sends them to the wave spawner through the event
        if not self.alive and self.spawned:
            self.triple = [Enemy(self.pos, self.squareWidth), Enemy(self.pos + self.moveVec*10, self.squareWidth), Enemy(self.pos + self.moveVec*-10, self.squareWidth)]
            self.triple[0].pos = self.pos
            self.triple[1].pos = self.pos + self.moveVec*20
            self.triple[2].pos = self.pos + self.moveVec*-20


            for i in self.triple:
                i.spawned = True
                i.visible = True
                i.moving = True
                i.waypointIndex = self.waypointIndex

            TripleEnemy.tripleExploded.publish(self, self.triple)
            self.spawned = False
    
    def update(self, waypoints, screen, spikes, wave):
        super().update(waypoints, screen, spikes, wave)
        self.is_exploded_triple()
        

        
