import pyganim, pygame


class Player(pygame.sprite.Sprite):
    # CONSTANTS
    dx = 4
    dy = -2
    ANIMATION_DT = .2
    GRAVITY_ACCELERATION = 2.0 / 30  # 2 px/sec
    JUMP_HALT_DELTA = 0.6  # if dy is in range [-JUMP_HALT_DELTA, JUMP_HALT_DELTA] halt animation will be displayed

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        animations = self.init_animation_sprites()
        # Set up animation instance variables
        self.standing_right_animation = animations["standing right"]
        self.standing_left_animation = animations["standing left"]
        self.walking_right_animation = animations["walking right"]
        self.walking_left_animation = animations["walking left"]
        self.jumping_right_animations = animations["jumping right"]
        self.jumping_left_animations = animations["jumping left"]

        self.direction = "RIGHT"  # direction is one of "RIGHT" or "LEFT"
        self.jumping = False
        self.dy = Player.dy
        self.animateObj = self.standing_right_animation
        self.rect = self.animateObj.getRect()
        self.rect.topleft = (x, y)
        self.image = self.animateObj.getCurrentFrame()
        self.animateObj.play()

    def init_animation_sprites(self):
        """
        Loads the images and creates animations objects
        :return: A dictionary for standing and walking animations
        """
        standing_right = pyganim.PygAnimation(
            [('res/goku_standing_0.png', Player.ANIMATION_DT),
             ('res/goku_standing_1.png', Player.ANIMATION_DT),
             ('res/goku_standing_2.png', Player.ANIMATION_DT),
             ('res/goku_standing_3.png', Player.ANIMATION_DT)])
        walk_right = pyganim.PygAnimation(
            [('res/goku_walking_right_0.png', Player.ANIMATION_DT),
             ('res/goku_walking_right_1.png', Player.ANIMATION_DT),
             ('res/goku_walking_right_2.png', Player.ANIMATION_DT),
             ('res/goku_walking_right_3.png', Player.ANIMATION_DT)])

        standing_left = self.flipAnimation(standing_right, True, False)
        walk_left = self.flipAnimation(walk_right, True, False)

        jump_start_right = pygame.image.load("res/goku_jumping_0.png")
        jump_up_right = pygame.image.load("res/goku_jumping_1.png")
        jump_halt_right = pygame.image.load("res/goku_jumping_2.png")
        jump_down_right = pygame.image.load("res/goku_jumping_3.png")

        jump_start_left = pygame.transform.flip(jump_start_right, True, False)
        jump_up_left = pygame.transform.flip(jump_up_right, True, False)
        jump_halt_left = pygame.transform.flip(jump_halt_right, True, False)
        jump_down_left = pygame.transform.flip(jump_down_right, True, False)

        landing = pyganim.PygAnimation(
            [('res/goku_jumping_4.png', Player.ANIMATION_DT),
             ('res/goku_jumping_5.png', Player.ANIMATION_DT),
             ('res/goku_jumping_6.png', Player.ANIMATION_DT)
             ])
        return {'standing right': standing_right, "standing left": standing_left, "walking right": walk_right,
                "walking left": walk_left,
                "jumping right": {"start": jump_start_right, "up": jump_up_right, "halt": jump_halt_right,
                            "down": jump_down_right,
                            "land_animation": landing},
                "jumping left": {"start": jump_start_left, "up": jump_up_left, "halt": jump_halt_left,
                            "down": jump_down_left,
                            "land_animation": landing}}

    def flipAnimation(self, animationObj, flipX, flipY):
        flippedObj = animationObj.getCopy()
        flippedObj.flip(flipX, flipY)
        flippedObj.makeTransformsPermanent()
        return flippedObj

    def update(self):
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

    def setImage(self, animationObj):
        """
        replaces the current animation Object with animationObj
        :param animationObj: a pyganim animation object to load as current image
        :return: None
        """
        self.animateObj = animationObj
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
        if self.rect.y > 500:
            self.jumping = False
            self.dy = Player.dy

        self.rect.y += self.dy
        self.dy += Player.GRAVITY_ACCELERATION
