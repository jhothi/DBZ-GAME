#!/usr/bin/python
import pygame, sys, tmx
from pygame.locals import *
from player import *
from enemy import *
from checkpoint import Checkpoint
from  hud import Hud
from dragonball import Dragonball


class Game:
    def __init__(self, width, height, bg_color):
        pygame.init()
        self.displaySurface = pygame.display.set_mode((width, height))
        self.bgColor = bg_color
        pygame.display.set_caption("GOKU")

        self.tilemap = tmx.load("test.tmx", self.displaySurface.get_size())
        self.players = tmx.SpriteLayer()
        self.enemies = tmx.SpriteLayer()
        self.blasts = tmx.SpriteLayer()
        self.hud = tmx.SpriteLayer()
        self.dragonball = tmx.SpriteLayer()
        self.checkpoints = Checkpoint()
        #self.bg = pygame.image.load('res/Map/dbz_background.jpg')
        player_cell = self.tilemap.layers["triggers"].find("player")[0]
        enemy_cells = self.tilemap.layers["triggers"].find("enemy")
        checkpoint_cells = self.tilemap.layers["triggers"].find("checkpoint")
        finish = self.tilemap.layers["triggers"].find("finish")[0]

        for cell in enemy_cells:
            self.enemies.add(Henchmen2((cell.left, cell.bottom)))

        for checkpoint in checkpoint_cells:
            self.checkpoints.add_checkpoint((checkpoint.px, checkpoint.py))

        self.goku = Goku((player_cell.px, player_cell.py))
        #  self.vegeta = Vegeta((400, 200))
        self.players.add(self.goku)
        self.hud.add(Hud(self.goku))
        self.dragonball.add(Dragonball((finish.px, finish.py)))
        # self.players.add(self.vegeta)
        self.fpsClock = pygame.time.Clock()
        self.tilemap.layers.append(self.players)
        self.tilemap.layers.append(self.enemies)
        self.tilemap.layers.append(self.blasts)
        self.tilemap.layers.append(self.hud)
        self.tilemap.layers.append(self.dragonball)

    def main(self):
        while True:  # Main Game Loop
            dt = self.fpsClock.tick(30)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            self.displaySurface.fill(self.bgColor)
            #self.displaySurface.blit(self.bg, (0,0))
            # self.tilemap.set_focus(self.goku.rect.x, self.goku.rect.y)
            self.tilemap.update(dt / 1000, self)
            self.tilemap.draw(self.displaySurface)
            pygame.display.update()


game = Game(800, 600, (0, 0, 255))
game.main()
