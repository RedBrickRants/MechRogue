from game_entity import Entity
import tcod 
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, base_stats,mech_base_stats ,enemy_base_stats, MAP_WIDTH, MAP_HEIGHT
import random
from game_map import GameMap


class Engine:
    def __init__(self):
        self.player = Entity("Player", "@", (255, 155, 55), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, base_stats, is_mech=False, )
        self.mech = Entity("Mech", "M", (100, 100, 255), SCREEN_WIDTH // 2 + 1, SCREEN_HEIGHT // 2, mech_base_stats, is_mech=True, )
        self.game_map = GameMap()
        self.entities = [self.player, self.mech]
        self.controlled_entity = self.player
        self.enemies = []
        self.log_messages = []
    def is_blocked(self,x, y, entities):
        for entity in entities:
            if entity.x == x and entity.y == y and entity.is_active:
                return True
        return False

    def spawn_enemy(self, x, y):
        while True:
            x = random.randint(0, MAP_WIDTH - 1)
            y = random.randint(0, MAP_HEIGHT - 1)
            if not self.is_blocked(x, y, self.entities):
                return Entity("Grunt", "g", (200, 50, 50), x, y, enemy_base_stats, is_mech=False, )
            
    def spawn_enemies(self, count: int):
        for _ in range(count):
            enemy = self.spawn_enemy(0, 0)
            self.enemies.append(enemy)
            self.entities.append(enemy)
    
    def find_exit_tile(self):
        for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
            x = self.mech.x + dx
            y = self.mech.y + dy
            if not self.is_blocked(x, y, self.entities):
                return x, y
        return self.mech.x, self.mech.y  # fallback (corpse ejection)

    def enter_mech(self):
        self.log_messages.append("You enter the mech.")
        self.player.is_active = False
        self.player.container = self.mech
        self.controlled_entity = self.mech

    def exit_mech(self):
        self.log_messages.append("You exit the mech.")
        self.player.is_active = True
        self.player.container = None
        self.player.x, self.player.y = self.find_exit_tile()
        self.controlled_entity = self.player

    def can_enter_mech(self) -> bool:
        if self.mech.stats["hp"] <= 0:
            return False
        dx = abs(self.player.x - self.mech.x)
        dy = abs(self.player.y - self.mech.y)
        return dx + dy == 1
    
    def toggle_controlled_entity(self):
        if self.controlled_entity == self.player:
            if self.can_enter_mech():
                self.enter_mech()
        elif self.controlled_entity == self.mech:
           self.exit_mech()
    
    
    def handle_input(self, event):
        if event.type != "KEYDOWN":
            return False

        if event.sym == tcod.event.KeySym.UP:
            self.controlled_entity.move(0, -1, self.game_map.width, self.game_map.height)
        elif event.sym == tcod.event.KeySym.DOWN:
            self.controlled_entity.move(0, 1, self.game_map.width, self.game_map.height)
        elif event.sym == tcod.event.KeySym.LEFT:
            self.controlled_entity.move(-1, 0, self.game_map.width, self.game_map.height)
        elif event.sym == tcod.event.KeySym.RIGHT:
            self.controlled_entity.move(1, 0, self.game_map.width, self.game_map.height)
        elif event.sym == tcod.event.KeySym.e:
            self.toggle_controlled_entity()
        elif event.sym == tcod.event.KeySym.q:
            return True  # signal quit

        return False

