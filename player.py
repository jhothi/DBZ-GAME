import pyganim, pygame, utils
from blast import KiBlast

"""
A Player moves between states (given keyboard input)
contains a position, direction, and an image
"""
class Player(pygame.sprite.Sprite):

    # CONSTANTS
    dx = 4
    dy = -3.25
    ANIMATION_DT = .15
    GRAVITY_ACCELERATION = .1  # 3 px/sec
    JUMP_HALT_DELTA = 1  # if dy is in range [-JUMP_HALT_DELTA, JUMP_HALT_DELTA] jump halt animation will be displayed

    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        # Set up animation instance variables
        self.standing_right_animation = self.get_standing_right_animation()
        self.standing_left_animation = self.get_standing_left_animation()
        self.walking_right_animation = self.get_walking_right_animation()
        self.walking_left_animation = self.get_walking_left_animation()
        self.jumping_right_animations = self.get_jumping_right_animations()
        self.jumping_left_animations = self.get_jumping_left_animations()
        self.shooting_right_animation = self.get_shooting_right_animation()
        self.shooting_left_animation = self.get_shooting_left_animations()
        self.animation_dict = {"RIGHT": {"STANDING": self.standing_right_animation,
                                         "WALKING": self.walking_right_animation,
                                         "SHOOTING": self.shooting_right_animation},
                               "LEFT": {"STANDING": self.standing_left_animation,
                                        "WALKING": self.walking_left_animation,
                                        "SHOOTING": self.shooting_left_animation}}

        self.direction = "RIGHT"  # direction is one of "RIGHT" or "LEFT"
        self.state = "WALKING"  # state is one of "WALKING" or "STANDING"
        self.resting = False
        self.shooting = False
        self.fire = False
        self.dy = 0
        self.blast = None
        self.lives = 3
        self.animateObj = self.standing_right_animation
        self.rect = self.animateObj.getRect()
        self.rect.topleft = position
        self.image = self.animateObj.getCurrentFrame()
        self.animateObj.play()

    # To be overridden by child classes
    def get_standing_right_animation(self):
        return None

    def get_walking_right_animation(self):
        return None

    def get_jumping_right_animations(self):
        return {}

    def get_shooting_right_animation(self):
        return None

    # Flip right facing animations
    def get_standing_left_animation(self):
        return utils.flip_animation(self.get_standing_right_animation(), True, False)

    def get_walking_left_animation(self):
        return utils.flip_animation(self.get_walking_right_animation(), True, False)

    #intialize a dictionary of jumping images
    def get_jumping_left_animations(self):
        jump_left_animations = {}
        jump_right_animations = self.get_jumping_right_animations()
        for key, val in jump_right_animations.iteritems():
            if key == "land animation":
                jump_left_animations[key] = utils.flip_animation(jump_right_animations[key], True, False)
            else:
                jump_left_animations[key] = pygame.transform.flip(jump_right_animations[key], True, False)

        return jump_left_animations

    def get_shooting_left_animations(self):
        return utils.flip_animation(self.get_shooting_right_animation(), True, False)

    def update(self, dt, game):
        """
        Updates the player state each tick of the game
        :param dt: the amount of time passed since last call
        :param game: the game object with refrence to all sprites
        :return: None
        """
        last = self.rect.copy()
        keys = pygame.key.get_pressed()

        if self.resting and keys[pygame.K_SPACE]:
            self.state = "SHOOTING"
            self.shooting = True

        if not self.shooting:
            if self.resting and keys[pygame.K_UP]:
                self.dy = Player.dy
                self.resting = False
                # blast = KiBlast((self.rect.right, self.rect.top + 10),"RIGHT", game.blasts)
            elif keys[pygame.K_RIGHT]:
                self.direction = "RIGHT"
                self.state = "WALKING"
                self.rect.x += Player.dx
            elif keys[pygame.K_LEFT]:
                self.direction = "LEFT"
                self.state = "WALKING"
                self.rect.x -= Player.dx
            elif self.resting:
                self.state = "STANDING"

        # move down
        self.dy += Player.GRAVITY_ACCELERATION
        self.rect.y += self.dy

        if self.shooting:
            self.shoot(game.blasts)
        elif not self.resting:
            self.jump()
        else:
            self.set_animation(self.animation_dict[self.direction][self.state])
        # print "RESTING: %r  %s %s" % (self.resting, self.state, self.direction)

        new = self.rect
        self.resting = False
        self.collision(game, last, new)
        game.tilemap.set_focus(new.left, new.bottom)

    def collision(self, game, last, new):
        """
        Detects any collision with walls and moves player to previous position if collision
        If shooting it stops the shoot animation when colliding with the wall
        :param game: the game object (holds the walls)
        :param last:the previous position
        :param new: position
        :return: None
        """
        for cell in game.tilemap.layers['triggers'].collide(new, 'wall'):

            if last.right <= cell.left < new.right:
                if last.bottom != cell.top:  # allow sliding collision
                    if self.shooting:
                        self.animateObj.stop()
                        self.shooting = False
                    new.right = cell.left
            if last.left >= cell.right > new.left:
                if last.bottom != cell.top:  # allow sliding collision
                    if self.shooting:
                        self.animateObj.stop()
                        self.shooting = False
                    new.left = cell.right
            if last.bottom <= cell.top and new.bottom >= cell.top:
                self.resting = True
                new.bottom = cell.top
                self.dy = 0
            if last.top >= cell.bottom and new.top < cell.bottom:
                new.top = cell.bottom
                self.dy = 0


    def set_animation(self, animation_obj):
        """
        replaces the current animation Object with animationObj
        :param animation_obj: a pyganim animation object to load as current image
        :return: None
        """
        rect = self.rect.copy()
        self.animateObj = animation_obj
        self.image = self.animateObj.getCurrentFrame()
        self.rect = self.image.get_rect()
        if self.direction == "RIGHT":
            self.rect.bottomleft = rect.bottomleft
        else:
            self.rect.bottomright = rect.bottomright

        # self.image = pygame.Surface(self.rect.size)
        self.animateObj.play()

    def set_static_image(self, image_obj, topleft=True, change_rect=True):
        """
        Sets the image to a still image rather than an animation object
        :param image_obj: the image (pygame.Surface)
        :param topleft: whether to postion pinned to the top left or bottomleft
        :param change_rect: whether to change the bounding rect
        :return: None
        """
        rect = self.rect
        old_rect = self.rect
        self.image = image_obj
        if change_rect:
            self.rect = self.image.get_rect()
        # self.image = pygame.Surface(self.rect.size)
        if topleft:
            self.rect.topleft = old_rect.topleft
        else:
            self.rect.bottomleft = old_rect.bottomleft

    def jump(self):
        """
        Depending on direction and dy loads the correct jump image
        :return: None
        """
        if self.direction == "RIGHT":
            jump_animation = self.jumping_right_animations
        else:
            jump_animation = self.jumping_left_animations

        if self.dy < -Player.JUMP_HALT_DELTA:
            self.set_static_image(jump_animation["up"])
        elif -Player.JUMP_HALT_DELTA <= self.dy <= Player.JUMP_HALT_DELTA:
            self.set_static_image(jump_animation["halt"], True, False)
        elif self.dy > Player.JUMP_HALT_DELTA:
            self.set_static_image(jump_animation["down"])

    def shoot(self, group):
        """
        Shoots a blast by waiting for the correct frame and then creates a new blast
        :param group: the group to add the blast to
        :return: None
        """
        animation = self.animation_dict[self.direction]["SHOOTING"]

        # Check if reached the last frame to shoot and that we have not already fired
        if animation.getCurrentFrame() == animation.getFrame(7) and not self.fire:
            self.fire = True
            if self.direction == "RIGHT":
                position = (self.rect.right - 46, self.rect.top + 17)
            else:
                position = (self.rect.left + 46, self.rect.top + 17)

            self.blast = KiBlast(position, self.direction, group)

        # Once done shooting animation go reset states
        if self.animateObj.isFinished():
            print "finished"
            animation.stop()
            self.shooting = False
            self.fire = False
        else:
            self.set_animation(animation)

    def lose_life(self, game):
        """
        Decrements lives until 0, resets player to closest previous checkpoint
        :param game: the game contains checkponints
        :return: None
        """
        self.lives -= 1
        if self.lives == 0:
            game.players.remove(self)
        else:
            self.rect.topleft = game.checkpoints.get_nearest_chekpoint((self.rect.x, self.rect.y))


class Goku(Player):
    SHOOTING_DT = .05

    def __init__(self, position):
        Player.__init__(self, position)
        print self.rect.size

    def get_standing_right_animation(self):
        return pyganim.PygAnimation(
            [('res/Sprites/Goku/goku_standing_0.png', Goku.ANIMATION_DT),
             ('res/Sprites/Goku/goku_standing_1.png', Goku.ANIMATION_DT),
             ('res/Sprites/Goku/goku_standing_2.png', Goku.ANIMATION_DT),
             ('res/Sprites/Goku/goku_standing_3.png', Goku.ANIMATION_DT)])

    def get_walking_right_animation(self):
        return pyganim.PygAnimation(
            [('res/Sprites/Goku/goku_walking_right_0.png', Goku.ANIMATION_DT),
             ('res/Sprites/Goku/goku_walking_right_1.png', Goku.ANIMATION_DT),
             ('res/Sprites/Goku/goku_walking_right_2.png', Goku.ANIMATION_DT),
             ('res/Sprites/Goku/goku_walking_right_3.png', Goku.ANIMATION_DT)])

    def get_jumping_right_animations(self):
        jump_start_right = pygame.image.load("res/Sprites/Goku/goku_jumping_0.png")
        jump_up_right = pygame.image.load("res/Sprites/Goku/goku_jumping_1.png")
        jump_halt_right = pygame.image.load("res/Sprites/Goku/goku_jumping_2.png")
        jump_down_right = pygame.image.load("res/Sprites/Goku/goku_jumping_3.png")
        landing = pyganim.PygAnimation(
            [('res/Sprites/Goku/goku_jumping_4.png', Goku.ANIMATION_DT),
             ('res/Sprites/Goku/goku_jumping_5.png', Goku.ANIMATION_DT),
             ('res/Sprites/Goku/goku_jumping_6.png', Goku.ANIMATION_DT)
             ])
        return {"start": jump_start_right, "up": jump_up_right, "halt": jump_halt_right,
                "down": jump_down_right,
                "land animation": landing}

    def get_shooting_right_animation(self):
        return pyganim.PygAnimation([('res/Sprites/Goku/goku_shooting_0.png', Goku.ANIMATION_DT),
                                     ('res/Sprites/Goku/goku_shooting_1.png', Goku.SHOOTING_DT),
                                     ('res/Sprites/Goku/goku_shooting_2.png', Goku.SHOOTING_DT),
                                     ('res/Sprites/Goku/goku_shooting_3.png', Goku.SHOOTING_DT),
                                     ('res/Sprites/Goku/goku_shooting_4.png', Goku.SHOOTING_DT),
                                     ('res/Sprites/Goku/goku_shooting_5.png', Goku.SHOOTING_DT),
                                     ('res/Sprites/Goku/goku_shooting_6.png', Goku.SHOOTING_DT),
                                     ('res/Sprites/Goku/goku_shooting_7.png', Goku.SHOOTING_DT),
                                     ('res/Sprites/Goku/goku_shooting_8.png', Goku.SHOOTING_DT),
                                     ('res/Sprites/Goku/goku_shooting_9.png', Goku.SHOOTING_DT),
                                     ], False)


class Vegeta(Player):
    def __init__(self, position):
        Player.__init__(self, position)

    def get_standing_right_animation(self):
        return pyganim.PygAnimation(
            [('res/Sprites/Vegeta/vegeta_standing_0.png', Vegeta.ANIMATION_DT),
             ('res/Sprites/Vegeta/vegeta_standing_1.png', Vegeta.ANIMATION_DT),
             ('res/Sprites/Vegeta/vegeta_standing_2.png', Vegeta.ANIMATION_DT),
             ('res/Sprites/Vegeta/vegeta_standing_3.png', Vegeta.ANIMATION_DT)])

    def get_walking_right_animation(self):
        return pyganim.PygAnimation(
            [('res/Sprites/Vegeta/vegeta_walking_right_0.png', Vegeta.ANIMATION_DT),
             ('res/Sprites/Vegeta/vegeta_walking_right_1.png', Vegeta.ANIMATION_DT),
             ('res/Sprites/Vegeta/vegeta_walking_right_2.png', Vegeta.ANIMATION_DT)])

    def get_jumping_right_animations(self):
        jump_start_right = pygame.image.load("res/Sprites/Vegeta/vegeta_jumping_0.png")
        jump_up_right = pygame.image.load("res/Sprites/Vegeta/vegeta_jumping_1.png")
        jump_halt_right = pygame.image.load("res/Sprites/Vegeta/vegeta_jumping_2.png")
        jump_down_right = pygame.image.load("res/Sprites/Vegeta/vegeta_jumping_3.png")
        landing = pyganim.PygAnimation(
            [('res/Sprites/Vegeta/vegeta_jumping_4.png', Vegeta.ANIMATION_DT),
             ('res/Sprites/Vegeta/vegeta_jumping_5.png', Vegeta.ANIMATION_DT),
             ('res/Sprites/Vegeta/vegeta_jumping_6.png', Vegeta.ANIMATION_DT)
             ])
        return {"start": jump_start_right, "up": jump_up_right, "halt": jump_halt_right,
                "down": jump_down_right,
                "land animation": landing}
