import pygame


class Enemy(pygame.sprite.Sprite):
    dx = 1
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((32, 32))
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.direction = "RIGHT"
        self.dx = 0

    def update(self, dt, game):
        last = self.rect.copy
        if self.direction == "RIGHT":
            self.rect.x += Enemy.dx
        else:
            self.rect.x -= Enemy.dx

        self.collision(last,self.rect,game)

    def collision(self,old,new,game):
        for cell in game.tilemap.layers['triggers'].collide(new, 'reverse'):
            if self.direction == "RIGHT":
                self.direction = "LEFT"
                self.rect.x -= Enemy.dx
            else:
                self.direction = "RIGHT"
                self.rect.x += Enemy.dx

        player_hit_list = pygame.sprite.spritecollide(self, game.players, True)
