from constants import MAP_WORLD_WIDTH, MAP_WORLD_HEIGHT, MAP_VIEW_WIDTH, MAP_VIEW_HEIGHT


class Tile:
    def __init__(self, name, glyph,colour, walkability, ):
        self.name = name
        self.colour = colour
        self.glyph = glyph
        self.iswalkable = walkability
        self.explored = False

class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = [
            [Tile("Floor", ".", (200, 200, 200), True) for y in range(height)]
            for x in range(width)
        ]

    def in_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def is_blocked(self,x, y, entities):
        if not self.in_bounds(x,y):
            return True
        if not self.tiles[x][y].iswalkable:
            return True
        for entity in entities:
            if entity.x == x and entity.y == y and entity.is_active:
                return True
        return False