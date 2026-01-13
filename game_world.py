from game_entity import Entity, Enemy
from game_map import GameMap
from constants import MAP_WORLD_WIDTH, MAP_WORLD_HEIGHT, base_stats, mech_base_stats, enemy_base_stats
from entity_factory import EnemyFactory
import random


class World:
    def __init__ (self):
        self.game_map = GameMap(MAP_WORLD_WIDTH, MAP_WORLD_HEIGHT)
        self.first_room = self.game_map.rooms[0]
        self.player = Entity("Player", "@", (255, 155, 55), self.first_room.center[0], self.first_room.center[1], base_stats, False, True)
        self.mech = Entity("Mech", "M", (100,100,255), self.first_room.center[0]+1, self.first_room.center[1], mech_base_stats, True, True)

        #Entity List
        self.entities=[self.player, self.mech]
        self.enemies=[]

    def get_spawnable_tile(self):
        while True:
            x = random.randint(0, MAP_WORLD_WIDTH - 1)
            y = random.randint(0, MAP_WORLD_HEIGHT - 1)

            if (not self.game_map.is_blocked(x, y, self.entities) and not self.game_map.is_tile_blocked(x, y)):
                return x, y

            

    def get_blocking_entity_at(self, x, y):
        for entity in self.entities:
            if (
                entity.blocks
                and entity.is_active
                and entity.x == x
                and entity.y == y
            ):
                return entity
        return None

    def try_move_entity(self, entity, dx, dy):
        dest_x = entity.x + dx
        dest_y = entity.y + dy
        # Map bounds check
        if not self.game_map.in_bounds(dest_x, dest_y):
            return (False, None)
        blocker = self.get_blocking_entity_at(dest_x, dest_y)
        if blocker:
            return(False, blocker)
        if self.game_map.is_tile_blocked(dest_x, dest_y):
            return (False, None)
        entity.x = dest_x
        entity.y = dest_y
        return (True, None)
    
    #

    def spawn_enemies(self, count: int):
        """Spawn multiple enemies randomly."""
        for _ in range(count):
            # Example: randomize enemy type and AI
            x, y = self.get_spawnable_tile()
            enemy_type = random.choice(["grunt","skirmisher"])
            enemy = EnemyFactory.create(enemy_type, x, y)
            self.entities.append(enemy)
            self.enemies.append(enemy)