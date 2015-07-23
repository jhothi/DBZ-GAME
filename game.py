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

        self.goku = Goku((100,200))
        self.vegeta = Vegeta((400, 200))
        self.players = pygame.sprite.Group()
        self.players.add(self.goku)
        self.players.add(self.vegeta)
        self.fpsClock = pygame.time.Clock()

    def main(self):

        while True:  # Main Game Loop
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            self.displaySurface.fill(self.bgColor)
            self.players.update()
            self.players.draw(self.displaySurface)
            pygame.display.update()
            self.fpsClock.tick(30)


game = Game(800, 600, (255, 255, 255))
game.main()
