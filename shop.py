import pygame as pg
from node import Node
from pathElement import Path
from publisher import Publisher

#class for items in the shop and class for displaying and handling the shop

shopLogo = pg.image.load(".\data\shop-logo.png")
shopLogo = pg.transform.scale(shopLogo, (400, 200))

basicTankItem = pg.image.load(".\data\Basic_tank_item.png")
basicTankItem = pg.transform.scale(basicTankItem, (199.5, basicTankItem.get_height()//1.5))

aoeTankItem = pg.image.load(".\data\Aoe_tank.png")
aoeTankItem = pg.transform.scale(aoeTankItem, (199.5, basicTankItem.get_height()))

spikes = pg.image.load(".\data\spike-image.png")
spikes = pg.transform.scale(spikes, (199.5, basicTankItem.get_height()))

class Item:#item class

    itemSelected = Publisher()

    def __init__(self, coors, img, id, game, price) -> None:
        self.coors = coors
        self.img = img
        self.rect = self.img.get_rect(topleft = coors)
        self.isSelected = False
        self.itemId = id
        self.price = price

        Node.boughtTurret.subscribe(self, self.bought_item)
        Path.boughtTrap.subscribe(self, self.bought_item)
        
        game.mouseClick.subscribe(self, self.on_mouse_click)
    
    def draw(self, screen: pg.Surface):#draws the item
        screen.blit(self.img, self.coors)

    
    def bought_item(self, player):#decreases players money when an item is bought
        if self.isSelected:
            player.money -= self.price


    def on_mouse_click(self, mousePos, player):#handles mouse click
        if self.rect.collidepoint(mousePos):
            if not self.isSelected:
                if player.money >= self.price:
                    Item.itemSelected.publish()
                    self.isSelected = True
                    player.selectedId = self.itemId
            else:
                self.isSelected = False
                player.selectedId = None
        

class Shop:#shop stores all the items and displays them
    def __init__(self, game) -> None:

        self.logo = shopLogo
        self.basicTankItem = Item((800, 200), basicTankItem, "basictank", game, 30)
        self.aoeTankItem = Item((1000, 200), aoeTankItem, "aoetank", game, 50)
        self.spikes = Item((800, spikes.get_height() + 200), spikes, "spikes", game, 20)
        self.items = [self.basicTankItem, self.aoeTankItem, self.spikes]

        Item.itemSelected.subscribe(self, self.clear_items)
        
    
    def draw_shop(self, screen: pg.Surface):#draws all the items in the shop
        screen.blit(self.logo, (800, 0))
        for item in self.items:
            item.draw(screen)
            if item.isSelected:
                pg.draw.rect(screen, (255, 255, 255), item.rect, 3)
    
    def clear_items(self):#clears all the selected items after clicking a different item
        for item in self.items:
            item.isSelected = False