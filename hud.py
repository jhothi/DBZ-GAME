import pygame

class Hud(pygame.sprite.Sprite):
    def __init__(self, player):
        pygame.sprite.Sprite.__init__(self)
        self.image = player.icon
        self.player = player
        self.rect = self.image.get_rect()
        self.rect.topleft = player.rect.topleft

    def update(self, dt, game):
        lives = self.player.lives
        icon_rect = self.player.icon.get_rect()
        hud_width = icon_rect.width * lives
        hud_surface = pygame.Surface((hud_width, icon_rect.height), pygame.SRCALPHA)

        for num in xrange(lives):
            hud_surface.blit(self.player.icon, (icon_rect.width * num, 0))

        self.image = hud_surface
        self.rect = self.image.get_rect()
        self.rect.topleft = game.tilemap.viewport.topleft