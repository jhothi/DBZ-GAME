import player, pyganim, pygame


class Goku(player.Player):
    def __init__(self, position):
        player.Player.__init__(self, position)

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
