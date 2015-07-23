import player, pyganim, pygame


class Vegeta(player.Player):
    def __init__(self, position):
        player.Player.__init__(self, position)

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

