import pygame as pg
from map import Map
from enemy import Enemy
from waveSpawner import Wave
from shop import Shop
from publisher import Publisher
from player import Player
from bullet import AoEBullet, Bullet
from spike import Spike



#main game class and while loop

WIDTH, HEIGHT = 800, 600 #setup of width and height for just the grid and for the whole screem + loading in fonts and images 
TOTALWIDTH, TOTALHEIGHT = 1200, 600
pg.init()
myfont = pg.font.SysFont("Comic Sans MS", 20)
screen = pg.display.set_mode((TOTALWIDTH, TOTALHEIGHT))

start = pg.image.load(".\data\Towerdefense-bg.jpg")
start = pg.transform.scale(start, (TOTALWIDTH, TOTALHEIGHT))

end = pg.image.load(".\data\Towerdefense-end.jpg")
end = pg.transform.scale(end, (TOTALWIDTH, TOTALHEIGHT))

instructions = pg.image.load(".\data\instructions-bg.jpg")
instructions = pg.transform.scale(instructions, (TOTALWIDTH, TOTALHEIGHT))


#main game class

class Game:
    def __init__(self) -> None:
        self.map = Map(WIDTH)

        Enemy.enemyKilled.subscribe(self, self.decrease_enemies)
        Enemy.enemyReachedEnd.subscribe(self, self.decrease_enemies)
        self.start = start
        self.end = end
        self.instructions = instructions
        self.endFont = pg.font.SysFont("Comic Sans MS", 50)
        self.screen = screen


        self.mouseHover = Publisher()#various 
        self.mouseClick = Publisher()
        

        self.gameState = "Start"

        self.map.init_elements(self)

        Bullet.bulletExploded.subscribe(self, self.draw_animation)
        Spike.spikeUsed.subscribe(self, self.draw_animation)
        

        self.shop = Shop(self)
        self.player = Player(self.shop, self, myfont)

        self.waves = [#initialize waves of enemies
            Wave(self.map.START, self.map.squareWidth, 10, 10),
            Wave(self.map.START, self.map.squareWidth, 10, 20),
            Wave(self.map.START, self.map.squareWidth, 20, 20),
            Wave(self.map.START, self.map.squareWidth, 20, 30),
            Wave(self.map.START, self.map.squareWidth, 20, 30),
            Wave(self.map.START, self.map.squareWidth, 30, 50),
            Wave(self.map.START, self.map.squareWidth, 60, 60),
        ]


        self.numOfEnemies = 0
        for w in self.waves:
            self.numOfEnemies += len(w.spawnables)

        
        self.startSpawn, self.endSpawn = 0, 0
        self.waveIndex = 0


        self.clock = pg.time.Clock()
        self.running = True
        

    def draw_animation(self, animation, coors):#function that draws the animation when the event publishes
        animation.startAnim = True
        animation.set_coors(coors)

    def decrease_enemies(self, *args):#decrease the number of enemies when an enemy reaches the end or gets killed
        self.numOfEnemies -= 1

    def spawn_wave(self):#spawns a wave every 1.2 seconds
        if self.waveIndex < len(self.waves):
            self.endSpawn = pg.time.get_ticks()
            if self.endSpawn - self.startSpawn > 1200:
                self.waves[self.waveIndex].spawned = True
                if self.waves[self.waveIndex].finishedSpawning:
                    self.waveIndex += 1
                self.startSpawn = self.endSpawn 

    def update_nodes(self, screen, waves):#runs the update node function for all the nodes on the map
        for n in self.map.nodeList:
            n.update_node(screen, self.waves)
    

    def update_waves(self):#updates all of the waves
        for wave in self.waves:
            if wave.spawned:
                self.spikes = [i.trap for i in self.map.pathList]
                wave.wave_update(screen, self.map.waypointList, self.spikes)

    def start_screen(self):#function for start screen
        keys = pg.key.get_pressed()
        self.screen.blit(self.start, (0, 0))
        if keys[pg.K_RETURN]:
            self.gameState = "Play"
        elif keys[pg.K_i]:
            self.gameState = "Instructions"

    def instructions_screen(self):#function for instructions screen
        keys = pg.key.get_pressed()
        self.screen.blit(self.instructions, (0, 0))
        if keys[pg.K_ESCAPE]:
            self.gameState = "Start"

    def end_screen(self):#function for end screen
        keys = pg.key.get_pressed()
        self.screen.blit(self.end, (0, 0))
        self.screen.blit(self.winner, (521, 86))
        if keys[pg.K_n]:
            self.running = False
        elif keys[pg.K_y]:
            self.reset()
            self.gameState = "Start"

    def update(self):#update function that draws the map, checks mouseHover event, handles waves, shop, and player
        self.numOfEnemies = 0
        for w in self.waves:
            if w.finishedSpawning:
                self.numOfEnemies += len(w.enemies)
            else:
                self.numOfEnemies += len(w.spawnables)

        if self.player.health < 0:
            self.winner = self.endFont.render("You lost!", 0, (255, 255, 255), (50, 50, 50))
            self.gameState = "End"
        elif self.numOfEnemies <= 0:
            self.winner = self.endFont.render("You won!", 0, (255, 255, 255), (50, 50, 50))
            self.gameState = "End"
        self.map.draw_map(self.screen, WIDTH, HEIGHT, self.waves)
        self.mouseHover.publish(pg.mouse.get_pos())
        self.spawn_wave()
        self.update_waves()
        self.update_nodes(self.screen, self.waves)
        self.shop.draw_shop(self.screen)
        self.player.draw_ui(self.screen)



    def reset(self):#function to reset the game if play again
        #reset player
        self.player.health = 50
        self.player.money = 100
        #reset map
        for n in self.map.nodeList:
            n.turret = None
        for p in self.map.pathList:
            p.trap = None
        
        #reset waves
        self.waveIndex = 0
        self.waves = [
            Wave(self.map.START, self.map.squareWidth, 10, 10),
            Wave(self.map.START, self.map.squareWidth, 10, 20),
            Wave(self.map.START, self.map.squareWidth, 20, 20),
            Wave(self.map.START, self.map.squareWidth, 20, 30),
            Wave(self.map.START, self.map.squareWidth, 20, 30),
            Wave(self.map.START, self.map.squareWidth, 30, 50),
            Wave(self.map.START, self.map.squareWidth, 60, 60),
        ]
        self.numOfEnemies = 0
  
    
    def play(self):#function handle gamestate
        if self.gameState == "Start":
            self.start_screen()
        elif self.gameState == "Instructions":
            self.instructions_screen()
        elif self.gameState == "Play":
            self.update()
        elif self.gameState == "End":
            self.end_screen()

game = Game()

while game.running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game.running = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            game.mouseClick.publish(pg.mouse.get_pos(), game.player)
    
    screen.fill(0)
    game.play()
    game.clock.tick(60)
    pg.display.update()

# pg.quit()
    