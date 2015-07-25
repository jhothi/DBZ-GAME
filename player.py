import pyganim, pygame


class Player(pygame.sprite.Sprite):
    # CONSTANTS
    dx = 4
    dy = -2.5
    ANIMATION_DT = .3
    GRAVITY_ACCELERATION = 2.0 / 30  # 2 px/sec
    JUMP_HALT_DELTA = 0.6  # if dy is in range [-JUMP_HALT_DELTA, JUMP_HALT_DELTA] jump halt animation will be displayed

    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        # Set up animation instance variables
        self.standing_right_animation = self.get_standing_right_animation()
        self.standing_left_animation = self.get_standing_left_animation()
        self.walking_right_animation = self.get_walking_right_animation()
        self.walking_left_animation = self.get_walking_left_animation()
        self.jumping_right_animations = self.get_jumping_right_animations()
        self.jumping_left_animations = self.get_jumping_left_animations()
        self.animation_dict = {"RIGHT": {"STANDING": self.standing_right_animation,
                                         "WALKING": self.walking_right_animation},
                               "LEFT": {"STANDING": self.standing_left_animation,
                                        "WALKING": self.walking_left_animation}}

        self.direction = "RIGHT"  # direction is one of "RIGHT" or "LEFT"
        self.state = "WALKING"  # state is one of "WALKING" or "STANDING"
        self.jumping = True
        self.resting = False
        self.dy = 0
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

    # Flip right facing animations
    def get_standing_left_animation(self):
        return self.flip_animation(self.get_standing_right_animation(), True, False)

    def get_walking_left_animation(self):
        return self.flip_animation(self.get_walking_right_animation(), True, False)

    def get_jumping_left_animations(self):
        jump_left_animations = {}
        jump_right_animations = self.get_jumping_right_animations()
        for key, val in jump_right_animations.iteritems():
            if key == "land animation":
                jump_left_animations[key] = self.flip_animation(jump_right_animations[key], True, False)
            else:
                jump_left_animations[key] = pygame.transform.flip(jump_right_animations[key], True, False)

        return jump_left_animations

    def flip_animation(self, animation_obj, flipX, flipY):
        flipped_obj = animation_obj.getCopy()
        flipped_obj.flip(flipX, flipY)
        flipped_obj.makeTransformsPermanent()
        return flipped_obj

    def update(self, dt, game):
        last = self.rect.copy()
        keys = pygame.key.get_pressed()
        if not self.jumping and keys[pygame.K_UP]:
            self.dy = Player.dy
            self.jumping = True
        elif keys[pygame.K_RIGHT]:
            self.direction = "RIGHT"
            self.state = "WALKING"
            self.rect.x += Player.dx
        elif keys[pygame.K_LEFT]:
            self.direction = "LEFT"
            self.state = "WALKING"
            self.rect.x -= Player.dx
        elif self.resting or not self.jumping:
            self.state = "STANDING"

        if self.jumping:
            self.jump()
        else:
            self.set_animation(self.animation_dict[self.direction][self.state])

        print "JUMPING: %r  %s %s" % (self.jumping, self.state, self.direction)

        # move down
        self.resting = False
        self.rect.y += self.dy
        self.dy += Player.GRAVITY_ACCELERATION

        new = self.rect
        self.resting = False
        self.collision(game, last, new)

        game.tilemap.set_focus(new.x, new.y)

    def collision(self, game, last, new):
        for cell in game.tilemap.layers['triggers'].collide(new, 'wall'):
            if last.right <= cell.left and new.right > cell.left:
                new.right = cell.left
            if last.left >= cell.right and new.left < cell.right:
                new.left = cell.right
            if last.bottom <= cell.top and new.bottom > cell.top:
                self.resting = True
                self.jumping = False
                new.bottom = cell.top
                self.dy = 0
            if last.top >= cell.bottom and new.top < cell.bottom:
                new.top = cell.bottom
                self.dy = 0

    def render(self, surface, pos):
        self.animateObj.blit(surface, pos)

    def set_animation(self, animation_obj):
        """
        replaces the current animation Object with animationObj
        :param animation_obj: a pyganim animation object to load as current image
        :return: None
        """
        position = self.rect.bottomleft
        self.animateObj = animation_obj
        self.image = self.animateObj.getCurrentFrame()
        self.rect = self.image.get_rect()
        self.rect.bottomleft = position
        self.animateObj.play()

    def set_static_image(self, image_obj, topleft=True):
        rect = self.rect
        position = None
        old_rect = self.rect
        self.image = image_obj
        self.rect = self.image.get_rect()
        if topleft:
            self.rect.topleft = old_rect.topleft
        else:
            self.rect.bottomleft = old_rect.bottomleft

    def jump(self):
        if self.direction == "RIGHT":
            jump_animation = self.jumping_right_animations
        else:
            jump_animation = self.jumping_left_animations

        if self.dy < -Player.JUMP_HALT_DELTA:
            self.set_static_image(jump_animation["up"])
        elif -Player.JUMP_HALT_DELTA <= self.dy <= Player.JUMP_HALT_DELTA:
            self.set_static_image(jump_animation["halt"])
        elif self.dy > Player.JUMP_HALT_DELTA:
            self.set_static_image(jump_animation["down"])
