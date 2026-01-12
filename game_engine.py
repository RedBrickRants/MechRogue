from enum import Enum, auto
import actions
import tcod 
from collections import deque
from dataclasses import dataclass # deque is a double-ended queue, useful for adding/removing list elements from both ends efficiently
from game_entity import Entity
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, base_stats,mech_base_stats ,enemy_base_stats, MAP_WORLD_WIDTH, MAP_WORLD_HEIGHT, MAP_VIEW_WIDTH, MAP_VIEW_HEIGHT
import random
from game_map import GameMap
from game_input_handler import InputHandler

class Camera:
    def __init__(self,width, height):
        self.x = 0
        self.y = 0
        self.width = width
        self.height = height
    def follow (self, target):
        self.x = target.x -self.width //2
        self.y = target.y - self.height//2
        self.x = max(0, min(self.x, MAP_WORLD_WIDTH - self.width))
        self.y = max(0, min(self.y, MAP_WORLD_HEIGHT - self.height))



class GameState (Enum):
    PLAYING = auto()
    PAUSED = auto()
    DEAD = auto()
@dataclass
class Message:
    text: str
    colour: tuple
    count: int = 1

class MessageLog:
    def __init__(self, max_length = 100):
        self.messages = deque(maxlen=max_length)

    def add(self, text: str, colour=(255, 255, 255)):
        # If there is a previous message and it matches → collapse
        if self.messages:
            last = self.messages[-1]
            if last.text == text and last.colour == colour:
                last.count += 1
                return

        # Otherwise create a new message
        self.messages.append(Message(text, colour))



class Engine:
    def __init__(self):
        self.input_handler = InputHandler(self) # Initialize input handler
        self.player = Entity("Player", "@", (255, 155, 55), MAP_WORLD_WIDTH // 2, MAP_WORLD_HEIGHT // 2, base_stats, is_mech=False, blocks=True)
        self.mech = Entity("Mech", "M", (100, 100, 255), MAP_WORLD_WIDTH // 2 + 1, MAP_WORLD_HEIGHT // 2, mech_base_stats, is_mech=True, blocks=True)
        self.game_map = GameMap(MAP_WORLD_WIDTH, MAP_WORLD_HEIGHT)
        self.game_state = GameState.PLAYING
        self.entities = [self.player, self.mech]
        self.controlled_entity = self.player
        self.message_log = MessageLog()
        self.enemies = []
        self.log_messages = []  # List of log messages for rendering
        self.turn_count = 0
        self.player_acted = True # Track if player has acted this turn
        self.camera = Camera(MAP_VIEW_WIDTH, MAP_VIEW_HEIGHT)

    def damage_entity(self, entity: Entity, damage: int):
        entity.stats["hp"] -= damage
        self.message_log.add(f"{entity.name} takes {damage} damage!", colour=(255, 0, 0))
        if entity.stats["hp"] <= 0 and entity.is_active:
            entity.is_active = False
            self.message_log.add(f"{entity.name} has been destroyed!", colour=(255, 0, 0))
            if entity == self.player:
                self.game_state = GameState.DEAD
                self.message_log.add("You have been killed!", colour=(255, 0, 0))

            if entity.is_mech and entity == self.controlled_entity:
                self.exit_mech()
                self.controlled_entity.stats["hp"] -= damage - entity.stats.get("armour", 0)
                self.message_log.add("Your mech has been destroyed! You exit the mech.", colour=(255, 0, 0))

    def handle_enemy_turns(self):
        for enemy in self.enemies:
            if not enemy.is_active:
                continue

            dx = self.controlled_entity.x - enemy.x
            dy = self.controlled_entity.y - enemy.y

            step_x = 0 if dx == 0 else (1 if dx > 0 else -1)
            step_y = 0 if dy == 0 else (1 if dy > 0 else -1)

            # Pick a direction to try (no pathfinding yet)
            if abs(dx) > abs(dy):
                self.try_move(enemy, step_x, 0)
            else:
                self.try_move(enemy, 0, step_y)

    
    
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
            if not self.game_map.is_blocked(x, y, self.entities):
                return Entity("Grunt", "g", (200, 50, 50), x, y, enemy_base_stats, is_mech=False, blocks=True)
            
    def spawn_enemies(self, count: int):
        for _ in range(count):
            enemy = self.spawn_enemy(0, 0)
            self.enemies.append(enemy)
            self.entities.append(enemy)
    
    def find_exit_tile(self):
        for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
            x = self.mech.x + dx
            y = self.mech.y + dy
            if not self.game_map.is_blocked(x, y, self.entities):
                return x, y
        return self.mech.x, self.mech.y  # fallback (corpse ejection)

    def enter_mech(self):
        self.message_log.add("You enter the mech.", colour=(255, 255, 0))
        self.player.is_active = False
        self.player.container = self.mech
        self.controlled_entity = self.mech

    def exit_mech(self):
        self.message_log.add("You exit the mech.", colour=(255, 255, 0))
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
    
    def try_move(self, entity, dx, dy):
        dest_x = entity.x + dx
        dest_y = entity.y + dy
        # Map bounds check
        if not self.game_map.in_bounds(dest_x, dest_y):
            return
        blocker = self.get_blocking_entity_at(dest_x, dest_y)
        if blocker:
            attack = actions.AttackAction(entity, blocker)
            self.perform(attack)
            return
        entity.x = dest_x
        entity.y = dest_y

    def perform(self, action):
        return action.perform(self) #do the action
        
        


    def update(self):
        if not self.player_acted:
            return
        if self.game_state != GameState.PLAYING:
            return
        self.camera.follow(self.controlled_entity)
        self.handle_enemy_turns()
        self.turn_count += 1
        self.player_acted = False   

    def handle_input(self, event):
        action = self.input_handler.handle_input(event)
        
        if not action:
            return False
        
        result = self.perform(action) #result will be an action or True for quit

        if result == "QUIT":
            return True
        self.player_acted = True

        if self.game_state == GameState.DEAD:
            if action.__class__ != actions.QuitAction:
                self.message_log.add("You are dead! Press 'q' to quit.", colour=(255, 0, 0))

        return False


