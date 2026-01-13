from game_entity import Entity, Enemy
from game_map import GameMap
from constants import MAP_WORLD_WIDTH, MAP_WORLD_HEIGHT, base_stats, mech_base_stats, enemy_base_stats
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


    def spawn_enemy(self, x=None, y=None, enemy_type="Grunt", ai_type="basic", traits=None):
        """Spawn a single enemy with optional AI and traits."""
        # Pick a random valid tile if no coords provided
        while True:
            if x is None or y is None:
                x = random.randint(0, MAP_WORLD_WIDTH - 1)
                y = random.randint(0, MAP_WORLD_HEIGHT - 1)

            if not self.game_map.is_blocked(x, y, self.entities) and not self.game_map.is_tile_blocked(x, y):
                break
            # If blocked, try again
            x, y = None, None

        # Create enemy based on type
        if enemy_type == "Grunt":
            name, char, colour, base_stats_used = "Grunt", "g", (200, 50, 50), enemy_base_stats
        elif enemy_type == "Brute":
            name, char, colour, base_stats_used = "Brute", "B", (150, 0, 0), {**enemy_base_stats, "hp": 80, "melee": 15, "armor": 5}
        elif enemy_type == "Scout":
            name, char, colour, base_stats_used = "Scout", "s", (100, 200, 50), {**enemy_base_stats, "speed": 120, "hp": 40}
        elif enemy_type == "Scarab":
            name, char, colour, base_stats_used = "Scarab", "S", (120, 130, 140), {**enemy_base_stats, "hp": 130, "melee": 30, "armour": 10}
        else:
            name, char, colour, base_stats_used = "Unknown", "?", (255,255,255), enemy_base_stats

        enemy = Enemy(
            name=name,
            char=char,
            colour=colour,
            x=x,
            y=y,
            base_stats=base_stats_used,
            ai_type=ai_type,
            traits=traits
        )

        # Add to world
        self.enemies.append(enemy)
        self.entities.append(enemy)

        return enemy

    def spawn_enemies(self, count: int):
        """Spawn multiple enemies randomly."""
        for _ in range(count):
            # Example: randomize enemy type and AI
            enemy_type = random.choice(["Grunt", "Brute", "Scout"])
            ai_type = random.choice(["basic", "chaotic"])
            self.spawn_enemy(enemy_type=enemy_type, ai_type=ai_type)