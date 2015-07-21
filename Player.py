import pyganim, pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.standing_animation = pyganim.PygAnimation(
            [('res/goku_standing_0.png', 0.25),
             ('res/goku_standing_1.png', 0.25),
             ('res/goku_standing_2.png', 0.25),
             ('res/goku_standing_3.png', 0.25)])
        self.walking_animation = pyganim.PygAnimation(
            [('res/goku_walking_right_0.png', 0.25),
             ('res/goku_walking_right_1.png', 0.25),
             ('res/goku_walking_right_2.png', 0.25),
             ('res/goku_walking_right_3.png', 0.25)])

        self.animateObj = self.standing_animation
        self.rect = self.animateObj.getRect()
        self.rect.topleft = (x, y)
        self.image = self.animateObj.getCurrentFrame()
        self.animateObj.play()

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.setImage(self.walking_animation)
            self.rect.x += 1
        else:
            self.setImage(self.standing_animation)

    def render(self, surface, pos):
        self.animateObj.blit(surface, pos)

    def setImage(self, animationObj):
        self.animateObj = animationObj
        self.image = self.animateObj.getCurrentFrame()
        self.animateObj.play()
