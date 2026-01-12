from game_entity import Entity
from game_map import GameMap
from constants import MAP_WORLD_WIDTH, MAP_WORLD_HEIGHT, base_stats, mech_base_stats, enemy_base_stats
import random


class World:
    def __init__ (self):
        self.game_map = GameMap(MAP_WORLD_WIDTH, MAP_WORLD_HEIGHT)
        self.first_room = self.game_map.rooms[0]
        self.player = Entity("Player", "@", (255, 155, 55), self.first_room.center[0], self.first_room.center[1], base_stats, False, True)
        self.mech = Entity("Mech", "M", (100,100,255), self.first_room.center[0]+1, self.first_room.center[1], mech_base_stats, False, True)

        #Entity List
        self.entities=[self.player, self.mech]
        self.enemies=[]

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


    def spawn_enemy(self, x, y):
        while True:
            x = random.randint(0, MAP_WORLD_WIDTH - 1)
            y = random.randint(0, MAP_WORLD_HEIGHT - 1)
            if not self.game_map.is_blocked(x, y, self.entities) and not self.game_map.is_tile_blocked(x,y):
                return Entity("Grunt", "g", (200, 50, 50), x, y, enemy_base_stats, is_mech=False, blocks=True)
        
    def spawn_enemies(self, count: int):
        for _ in range(count):
            enemy = self.spawn_enemy(0, 0)
            self.enemies.append(enemy)
            self.entities.append(enemy)