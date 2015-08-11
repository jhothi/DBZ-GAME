import pygame, pyganim, random
from blast import *
import utils


class Enemy(pygame.sprite.Sprite):
    dx = 1
    SHOOT_PROBABILITY = .01  # per frame

    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        # set up images
        self.walking_right_image = self.get_walking_right_image()
        self.walking_left_image = pygame.transform.flip(self.walking_right_image, True, False)
        self.shooting_animation_right = self.get_shooting_right_animation()
        self.shooting_animation_left = utils.flip_animation(self.shooting_animation_right, True, False)

        # set position
        self.image = self.walking_right_image
        self.rect = self.image.get_rect()
        self.rect.bottomleft = position

        # set state
        self.blast = None
        self.direction = "RIGHT"
        self.shooting = False
        self.fire = False

    def get_walking_right_image(self):
        return None

    def get_shooting_right_animation(self):
        return None

    def shooting_delta(self):
        return 0

    def update(self, dt, game):
        last = self.rect.copy()
        if not self.shooting:
            if self.direction == "RIGHT":
                self.set_image(self.walking_right_image)
                self.rect.x += Enemy.dx
            else:
                self.set_image(self.walking_left_image)
                self.rect.x -= Enemy.dx

        self.collision(last, self.rect, game)
        self.shoot((self.rect.right, self.rect.top + 14), game.blasts)

    def collision(self, old, new, game):
        if not self.shooting:
            for cell in game.tilemap.layers['triggers'].collide(new, 'reverse'):
                cell_type = cell['reverse']
                if self.direction == "RIGHT" and cell_type == "right":
                    self.direction = "LEFT"
                    self.rect.x -= Enemy.dx
                elif self.direction == "LEFT" and cell_type == "left":
                    self.direction = "RIGHT"
                    self.rect.x += Enemy.dx

        player_hit_list = pygame.sprite.spritecollide(self, game.players, False)
        for player in player_hit_list:
            if player.shooting:
                game.enemies.remove(self)
                game.blasts.remove(self.blast)
                player.shooting = False
            else:
                game.players.remove(player)

    def shoot(self, position, group):
        # shoot logic
        animation = None
        if self.direction == "RIGHT":
            animation = self.shooting_animation_right
        else:
            animation = self.shooting_animation_left

        if self.shooting:
            self.set_image(animation.getCurrentFrame())

        num = random.randint(0, 100)

        if num <= 100 * Enemy.SHOOT_PROBABILITY and not self.shooting:
            animation.play()
            self.shooting = True
        if animation.isFinished() and not self.fire:
            # fire shot
            self.fire = True
            if self.direction == "RIGHT":
                position = (self.rect.right, self.rect.top + self.shooting_delta())
            else:
                position = (self.rect.left, self.rect.top + self.shooting_delta())
            self.blast = self.get_blast(position, self.direction, group)

        if self.blast is not None:
            if self.blast.is_animation_over():
                self.shooting = False
                self.fire = False
                self.shooting_animation_left.stop()
                self.shooting_animation_right.stop()
                self.blast = None

    def set_image(self, image):
        old_rect = self.rect.copy()
        self.image = image
        self.rect = image.get_rect()
        if self.direction == "RIGHT":
            self.rect.topleft = old_rect.topleft
        else:
            self.rect.topright = old_rect.topright


class Henchmen1(Enemy):
    def __init__(self, position):
        Enemy.__init__(self, position)

    def get_walking_right_image(self):
        return pygame.image.load('res/Sprites/Henchmen1/henchmen_1_walking.png')

    def get_shooting_right_animation(self):
        return pyganim.PygAnimation(
            [('res/Sprites/Henchmen1/henchmen_1_shooting_0.png', .5),
             ('res/Sprites/Henchmen1/henchmen_1_shooting_1.png', .01)], False)

    def shooting_delta(self):
        return 10

    def get_blast(self, position, direction, group):
        return Laser(position, direction, group)


class Henchmen2(Enemy):
    def __init__(self, position):
        Enemy.__init__(self, position)

    def get_walking_right_image(self):
        return pygame.image.load('res/Sprites/Henchmen2/henchmen_2_walking.png')

    def get_shooting_right_animation(self):
        return pyganim.PygAnimation(
            [('res/Sprites/Henchmen2/henchmen_2_shooting_0.png', .5),
             ('res/Sprites/Henchmen2/henchmen_2_shooting_1.png', .01)], False)

    def shooting_delta(self):
        return 9

    def get_blast(self, position, direction, group):
        return KiBeam(position, direction, group)
