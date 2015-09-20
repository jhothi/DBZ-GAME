import pygame


class Dragonball(pygame.sprite.Sprite):
    def __init__(self, position):
        """
        Set up the dragonball which ends the level
        :param position: the topleft tuple where to place the dragonball
        :return:
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('res/Map/1_Star_Dragon_Ball.png')
        self.rect = self.image.get_rect()
        self.rect.topleft = position

    def update(self, dt, game):
        players = pygame.sprite.spritecollide(self, game.players, False)
        if len(players) > 0:
            players[0].lose_life(game)

