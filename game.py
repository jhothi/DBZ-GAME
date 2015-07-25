import pygame, sys, tmx
from pygame.locals import *
from player import Player
from goku import Goku
from vegeta import Vegeta

class Game:
    def __init__(self, width, height, bg_color):
        pygame.init()
        self.displaySurface = pygame.display.set_mode((width, height))
        self.bgColor = bg_color
        pygame.display.set_caption("GOKU")

        self.tilemap = tmx.load("res/Maps/test.tmx", self.displaySurface.get_size())
        self.players = tmx.SpriteLayer()
        self.goku = Goku((self.tilemap.layers["triggers"].find("player")[0].px,self.tilemap.layers["triggers"].find("player")[0].py))
        #self.vegeta = Vegeta((400, 200))
        self.players.add(self.goku)
        #self.players.add(self.vegeta)
        self.fpsClock = pygame.time.Clock()
        self.tilemap.layers.append(self.players)
        print self.tilemap.layers["triggers"].find("player")[0].px
    def main(self):
        x = 10
        y = 12
        while True:  # Main Game Loop
            dt = self.fpsClock.tick(30)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            self.displaySurface.fill(self.bgColor)
            #self.tilemap.set_focus(self.goku.rect.x, self.goku.rect.y)
            self.tilemap.update(dt / 1000, self)
            self.tilemap.draw(self.displaySurface)
            pygame.display.update()



game = Game(800, 600, (0,0,255))
game.main()
