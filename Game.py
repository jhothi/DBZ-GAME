import pygame, sys
from pygame.locals import *
from Player import Player


class Game:
    def __init__(self, width, height, bg_color):
        pygame.init()
        self.displaySurface = pygame.display.set_mode((width, height))
        self.bgColor = bg_color
        pygame.display.set_caption("GOKU")
        self.goku = Player(400,300)
        self.players = pygame.sprite.Group()
        self.players.add(self.goku)
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
