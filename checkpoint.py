"""
Represents a list of checkpoints loaded in from tmx file
uses a list of tuples (x,y) to represent each checkpoint
"""
class Checkpoint:
    def __init__(self):
        self.checkpoints = []

    def add_checkpoint(self, position):
        self.checkpoints.append(position)

    def get_nearest_chekpoint(self, position):
        min_distance = 100000000
        closest_checkpoint = None
        for checkpoint in self.checkpoints:
            delta_x = position[0] - checkpoint[0]
            print delta_x
            if 0 < delta_x < min_distance:
                min_distance = delta_x
                closest_checkpoint = checkpoint
        return closest_checkpoint