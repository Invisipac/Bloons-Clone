import pygame as pg
from enemy import Enemy, TripleEnemy

#class for containing and managing the waves of enemies. by far the most annoying and finicky thing in this code.

class Wave:#wave class
    def __init__(self, start, squareWidth, numTriple, numNormal) -> None:
        self.start = (start[0]*squareWidth + squareWidth//2, start[0]*squareWidth + squareWidth//2)
        self.numOfEnemies = numTriple + numNormal

        self.spawnables = []

        self.spawnables += [TripleEnemy(start, squareWidth) for i in range(numTriple)]
        self.spawnables += [Enemy(start, squareWidth) for i in range(numNormal)]
        self.totalEnemies = 3*numTriple + numTriple + numNormal

        self.enemies = []
        self.enemyIndex = 0
        self.startSpawn, self.endSpawn = 0, 0
        self.spawned = False
        self.finishedSpawning = False
        TripleEnemy.tripleExploded.subscribe(self, self.add_triple)
        Enemy.enemyKilled.subscribe(self, self.remove_enemy)
    

    def add_triple(self, enemy, triple):#function to add three enemies when a triple enemy is exploded
        if enemy in self.enemies:
            for i in triple:
                self.enemies.insert(self.enemies.index(enemy), i)
            self.enemies.remove(enemy)

    def remove_enemy(self, enemy):#removes the blue enemies when they die
        if enemy in self.enemies and type(enemy) == Enemy:
            self.enemies.remove(enemy)

    def spawn_enemy(self):#spawns the enemies every 0.2 seconds
        if self.enemyIndex < self.numOfEnemies:
            self.endSpawn = pg.time.get_ticks()

            if self.endSpawn - self.startSpawn > 200:
                
                self.spawnables[self.enemyIndex].moving = True
                self.spawnables[self.enemyIndex].visible = True
                self.spawnables[self.enemyIndex].spawned = True

                self.enemies.append(self.spawnables[self.enemyIndex])

                self.enemyIndex += 1
                self.startSpawn = self.endSpawn
        elif self.enemyIndex == self.numOfEnemies:
            self.finishedSpawning = True

    def update_enemies(self, waypoints, screen, spikes):#updates all of the enemies in the list 
        for enemy in self.enemies:
            if enemy.alive or enemy.spawned:
                enemy.update(waypoints, screen, spikes, self)

    
    def wave_update(self, screen, waypoints, spikes):#updates the wave
        if not self.finishedSpawning:
            self.spawn_enemy()
        self.update_enemies(waypoints, screen, spikes)




