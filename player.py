import pyganim, pygame


class Player(pygame.sprite.Sprite):
    # CONSTANTS
    dx = 4
    dy = -2
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

        self.direction = "RIGHT"  # direction is one of "RIGHT" or "LEFT"
        self.jumping = False
        self.dy = Player.dy
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

    def update(self, dt):
        keys = pygame.key.get_pressed()
        if self.jumping:
            if keys[pygame.K_RIGHT]:
                self.direction = "RIGHT"
                self.rect.x += Player.dx
            elif keys[pygame.K_LEFT]:
                self.direction = "LEFT"
                self.rect.x -= Player.dx
            self.jump()

        else:
            if keys[pygame.K_UP]:
                self.jumping = True
                self.jump()
            elif keys[pygame.K_RIGHT]:
                self.direction = "RIGHT"
                self.setImage(self.walking_right_animation)
                self.rect.x += Player.dx
            elif keys[pygame.K_LEFT]:
                self.direction = "LEFT"
                self.setImage(self.walking_left_animation)
                self.rect.x -= Player.dx
            else:
                if self.direction == "RIGHT":
                    self.setImage(self.standing_right_animation)
                elif self.direction == "LEFT":
                    self.setImage(self.standing_left_animation)

    def render(self, surface, pos):
        self.animateObj.blit(surface, pos)

    def setImage(self, animation_obj):
        """
        replaces the current animation Object with animationObj
        :param animation_obj: a pyganim animation object to load as current image
        :return: None
        """
        self.animateObj = animation_obj
        self.image = self.animateObj.getCurrentFrame()
        self.animateObj.play()

    def jump(self):
        if self.direction == "RIGHT":
            jump_animation = self.jumping_right_animations
        else:
            jump_animation = self.jumping_left_animations

        if self.dy < -Player.JUMP_HALT_DELTA:
            self.image = jump_animation["up"]
        elif -Player.JUMP_HALT_DELTA <= self.dy <= Player.JUMP_HALT_DELTA:
            self.image = jump_animation["halt"]
        elif self.dy > Player.JUMP_HALT_DELTA:
            self.image = jump_animation["down"]

        # TODO replace with collision with floor
        if self.rect.y > 900:
            self.jumping = False
            self.dy = Player.dy

        self.rect.y += self.dy
        self.dy += Player.GRAVITY_ACCELERATION
