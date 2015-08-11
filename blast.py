import pygame, pyganim


class Beam(pygame.sprite.Sprite):
    dx = 3

    def __init__(self, position, direction, group):
        pygame.sprite.Sprite.__init__(self)
        self.beam = self.get_beam()
        self.head = self.get_head()
        self.start_position = position
        self.direction = direction
        self.start_position = position
        self.image = self.get_starting_image()
        self.bullet_destroyed = False
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.group = group
        group.add(self)

    def get_beam(self):
        return None

    def get_head(self):
        return None

    def get_starting_image(self):
        return self.get_beam()

    def update(self, dt, game):
        last = self.rect.copy()
        # self.group.empty()
        self.image = self.extend_beam()
        new = self.rect
        self.collision(last, new, game)

    def is_animation_over(self):
        return self.bullet_destroyed

    def extend_beam(self):
        self.beam = pygame.transform.scale(self.beam, (self.beam.get_width() + Beam.dx, self.beam.get_height()))
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

            if last.left <= cell.right < new.left:
                self.destroy_bullet()

        players = pygame.sprite.spritecollide(self, game.players, True)
        if len(players) > 0:
            self.destroy_bullet()

        if self.rect.width > 100:
            self.destroy_bullet()

    def destroy_bullet(self):
        self.bullet_destroyed = True
        self.group.remove(self)


class Laser(Beam):
    def __init__(self, position, direction, group):
        Beam.__init__(self, position, direction, group)

    def get_beam(self):
        return pygame.image.load('res/Sprites/Henchmen1/henchmen_1_shooting_beam.png')

    def get_head(self):
        return pygame.image.load('res/Sprites/Henchmen1/henchmen_1_shooting_head.png')


class KiBeam(Beam):
    def __init__(self, position, direction, group):
        Beam.__init__(self, position, direction, group)

    def get_beam(self):
        return pygame.image.load('res/Sprites/Henchmen2/henchmen_2_shooting_beam.png')

    def get_head(self):
        return pygame.image.load('res/Sprites/Henchmen2/henchmen_2_shooting_head.png')


class KiBlast(pygame.sprite.Sprite):
    dx = 4
    def __init__(self, position, direction, group):
        pygame.sprite.Sprite.__init__(self)
        self.blast_animation = pyganim.PygAnimation([('res/Sprites/Goku/goku_shooting_blast_0.png', .1),
                                                     ('res/Sprites/Goku/goku_shooting_blast_1.png', .1),
                                                     ('res/Sprites/Goku/goku_shooting_blast_2.png', .1),
                                                     ('res/Sprites/Goku/goku_shooting_blast_3.png', .1),
                                                     ('res/Sprites/Goku/goku_shooting_blast_4.png', .1),
                                                     ])
        self.blast_right = pygame.image.load('res/Sprites/Goku/goku_shooting_blast_4.png')
        self.blast_left = pygame.transform.flip(self.blast_right, True, False)
        self.start_position = position
        if direction == "RIGHT":
            self.image = self.blast_right
            self.rect = self.image.get_rect()
            self.rect.topleft = position
        else:
            self.image = self.blast_left
            self.rect = self.image.get_rect()
            self.rect.topright = position

        self.bullet_destroyed = False
        self.direction = direction
        #self.blast_animation.play()
        self.group = group
        group.add(self)

    def update(self, dt, game):
        last = self.rect.copy()
        if self.direction == "RIGHT":
            self.rect.x += KiBlast.dx
        else:
            self.rect.x -= KiBlast.dx

        self.collision(last, self.rect, game)

    def extend_beam(self):
        return self.blast_animation.getCurrentFrame()

    def get_starting_image(self):
        return self.blast_animation.getCurrentFrame()

    def collision(self, last, new, game):
        cells =  game.tilemap.layers['triggers'].collide(new, 'wall')
        if len(cells) > 0:
            self.destroy_bullet()

        enemies = pygame.sprite.spritecollide(self, game.enemies, True)
        if len(enemies) > 0:
            self.destroy_bullet()

    def destroy_bullet(self):
        self.bullet_destroyed = True
        self.group.remove(self)

    def is_animation_over(self):
        return self.bullet_destroyed
