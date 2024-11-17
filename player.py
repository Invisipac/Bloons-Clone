import pygame as pg
from turret import Turret

from enemy import Enemy

#class for the player that can buy and place objects, earn money, and lose health


heart = pg.image.load(".\data\lives.png")
heart = pg.transform.scale(heart, (heart.get_width()//9, heart.get_height()//9))
coin = pg.image.load(".\data\money.png")
coin = pg.transform.scale(coin, (coin.get_width()//7, coin.get_height()//7))



class Player:#player class
    def __init__(self, shop, game, font: pg.font.Font) -> None:

        Enemy.enemyReachedEnd.subscribe(self, self.lose_life)
        Enemy.enemyKilled.subscribe(self, self.gain_money)
        self.health = 50
        self.money = 100
        self.font = font
        self.healthText = font.render(f"{self.health}", 0, (255, 255, 255), (100, 100, 100))
        self.moneyText = font.render(f"{self.money}", 0, (255, 255, 255), (100, 100, 100))
        self.selectedId = None
        self.shop = shop
    
    def lose_life(self, dmg):#function that decreases health based on damage of the enemy
        self.health -= dmg

    def gain_money(self, *args):#earn money
        self.money += 1

    def draw_ui(self, screen: pg.Surface):#draw the health and money
        screen.blit(heart, (346, -2))
        screen.blit(coin, (553, 2))


        self.healthText = self.font.render(f"{self.health}", 0, (255, 255, 255), (100, 100, 100))
        self.moneyText = self.font.render(f"{self.money}", 0, (255, 255, 255), (100, 100, 100))
        screen.blit(self.healthText, (408, 4))
        screen.blit(self.moneyText, (600, 4))
    

    



    
    
    