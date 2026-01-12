import random
import tcod
from constants import MAP_WORLD_WIDTH, MAP_WORLD_HEIGHT

class Tile:
    def __init__(self, name, glyph, colour, walkable, blocks_sight):
        self.name = name
        self.glyph = glyph
        self.colour = colour
        self.iswalkable = walkable
        self.blocks_sight = blocks_sight
        self.explored = False


class RectRoom:
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h
        self.sub_rooms = []

    @property
    def center(self):
        return (self.x1 + self.x2) // 2, (self.y1 + self.y2) // 2

    def intersects(self, other):
        return (
            self.x1 <= other.x2 and
            self.x2 >= other.x1 and
            self.y1 <= other.y2 and
            self.y2 >= other.y1
        )


class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        # Fill with solid walls
        self.tiles = [
            [
                Tile("Wall", "#", (90, 90, 90), False, True)
                for y in range(height)
            ]
            for x in range(width)
        ]

        self.rooms = []
        self.generate_dungeon()

        self.fov_map = self.initialize_fov()

    # ---------- Dungeon Generation ----------

    def generate_dungeon(self, max_rooms=35, room_min=6, room_max=12):
        for _ in range(max_rooms):
            w = random.randint(room_min, room_max)
            h = random.randint(room_min, room_max)
            x = random.randint(1, self.width - w - 2)
            y = random.randint(1, self.height - h - 2)

            room = RectRoom(x, y, w, h)

            if any(room.intersects(other) for other in self.rooms):
                continue

            self.create_room(room)

            if self.rooms:
                prev_x, prev_y = self.rooms[-1].center
                new_x, new_y = room.center

                if random.random() < 0.5:
                    self.create_h_tunnel(prev_x, new_x, prev_y)
                    self.create_v_tunnel(prev_y, new_y, new_x)
                else:
                    self.create_v_tunnel(prev_y, new_y, prev_x)
                    self.create_h_tunnel(prev_x, new_x, new_y)

            self.rooms.append(room)

    def create_room(self, room):
        for x in range(room.x1, room.x2):
            for y in range(room.y1, room.y2):
                self.tiles[x][y] = Tile("Floor", ".", (200, 180, 50), True, False)

    

    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y] = Tile("Floor", ".", (200, 180, 50), True, False)

    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y] = Tile("Floor", ".", (200, 180, 50), True, False)

    # ---------- Map Queries ----------

    def in_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height
    
    def is_blocked(self,x, y, entities):

        for entity in entities:
            if entity.x == x and entity.y == y and entity.is_active:
                return True
        return False

    def is_tile_blocked(self, x, y):
        if not self.in_bounds(x, y):
            return True
        return not self.tiles[x][y].iswalkable

    # ---------- FOV ----------

    def initialize_fov(self):
        fov_map = tcod.map.Map(self.width, self.height)
        for x in range(self.width):
            for y in range(self.height):
                tile = self.tiles[x][y]
                fov_map.transparent[x, y] = not tile.blocks_sight
                fov_map.walkable[x, y] = tile.iswalkable
        return fov_map

    def recompute_fov(self, x, y, radius=12):
        visible = tcod.map.compute_fov(
            self.fov_map.transparent,
            (x, y),
            radius=radius,
            light_walls=True
        )

        for vx in range(self.width):
            for vy in range(self.height):
                if visible[vx, vy]:
                    self.tiles[vx][vy].explored = True

        return visible
