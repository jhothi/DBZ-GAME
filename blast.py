import pygame, pyganim


class Blast(pygame.sprite.Sprite):
    dx = 3

    def __init__(self, position, direction, group):
        pygame.sprite.Sprite.__init__(self)
        self.beam = self.get_beam()
        self.head = self.get_head()
        self.start_position = position
        self.direction = direction
        self.start_position = position
        self.image = self.beam
        self.bullet_destroyed = False
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.group = group
        group.add(self)

    def get_beam(self):
        return None

    def get_head(self):
        return None

    def update(self, dt, game):
        last = self.rect.copy()
        # self.group.empty()
        self.image = self.extend_beam()
        new = self.rect
        self.collision(last, new, game)

    def is_animation_over(self):
        return self.bullet_destroyed

    def extend_beam(self):
        self.beam = pygame.transform.scale(self.beam, (self.beam.get_width() + Blast.dx, self.beam.get_height()))
        beam_rect = self.beam.get_rect()
        head_rect = self.head.get_rect()
        full_beam = pygame.Surface((beam_rect.width + head_rect.width, max(beam_rect.height, head_rect.height)),
                                   pygame.SRCALPHA)
        full_beam_rect = full_beam.get_rect()
        full_beam.blit(self.beam, (0, 4))
        full_beam.blit(self.head, (beam_rect.right - 4, full_beam_rect.top))
        self.rect = full_beam_rect
        if self.direction == "LEFT":
            full_beam = pygame.transform.flip(full_beam, True, False)
            self.rect.topright = self.start_position
        else:
            self.rect.topleft = self.start_position
        return full_beam

    def collision(self, last, new, game):
        for cell in game.tilemap.layers['triggers'].collide(new, 'wall'):
            if last.right <= cell.left < new.right:
                self.destroy_bullet()

            if last.left <= cell.right < cell.left:
                self.destroy_bullet()

        players = pygame.sprite.spritecollide(self, game.players, True)
        if len(players) > 0:
            self.destroy_bullet()

        if self.rect.width > 100:
            self.destroy_bullet()

    def destroy_bullet(self):
        self.bullet_destroyed = True
        self.group.remove(self)


class Laser(Blast):
    def __init__(self, position, direction, group):
        Blast.__init__(self, position, direction, group)

    def get_beam(self):
        return pygame.image.load('res/Sprites/Henchmen1/henchmen_1_shooting_beam.png')

    def get_head(self):
        return pygame.image.load('res/Sprites/Henchmen1/henchmen_1_shooting_head.png')


class KiBlast(Blast):
    def __init__(self, position, direction, group):
        Blast.__init__(self, position, direction, group)

    def get_beam(self):
        return pygame.image.load('res/Sprites/Henchmen2/henchmen_2_shooting_beam.png')

    def get_head(self):
        return pygame.image.load('res/Sprites/Henchmen2/henchmen_2_shooting_head.png')
