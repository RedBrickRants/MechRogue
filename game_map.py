from constants import MAP_WIDTH, MAP_HEIGHT

class GameMap:
    def __init__(self):
        self.width = MAP_WIDTH
        self.height = MAP_HEIGHT
        self.in_bounds = self.in_bounds

    def in_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height