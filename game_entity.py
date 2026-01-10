from typing import Tuple

class Entity:
    def __init__(self, name: str, char: str, colour: Tuple[int, int, int], x: int, y:int, base_stats, is_mech: bool, ):
        self.name = name
        self.char = char
        self.colour = colour
        self.x = x
        self.y = y
        self.stats = base_stats.copy()
        self.is_mech = is_mech
        self.is_active = True   # is this entity currently on the map?
        self.container = None  # what entity (if any) is holding this one

    

    def move(self, dx, dy, map_width, map_height):
        new_x = self.x + dx
        new_y = self.y + dy

        if 0 <= new_x < map_width and 0 <= new_y < map_height:
            self.x = new_x
            self.y = new_y