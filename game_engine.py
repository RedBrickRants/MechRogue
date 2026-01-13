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
from game_world import World

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
        self.world = World()
        self.game_state = GameState.PLAYING
        self.controlled_entity = self.world.player
        self.message_log = MessageLog()
        self.log_messages = []  # List of log messages for rendering
        self.turn_count = 0
        self.player_acted = True # Track if player has acted this turn
        self.camera = Camera(MAP_VIEW_WIDTH, MAP_VIEW_HEIGHT)
        self.visible_tiles = self.world.game_map.recompute_fov(
            self.controlled_entity.x,
            self.controlled_entity.y
        )

    def damage_entity(self, entity: Entity, damage: int):
        entity.stats["hp"] -= damage
        self.message_log.add(f"{entity.name} takes {damage} damage!", colour=(255, 0, 0))

        if entity.stats["hp"] > 0 or not entity.is_active:
            return

        if entity.is_mech:
            self.handle_mech_destroyed(entity)
            return

        # Normal entity death
        entity.is_active = False
        self.message_log.add(f"{entity.name} has been destroyed!", colour=(255, 0, 0))

        if entity == self.world.player:
            self.game_state = GameState.DEAD
            self.message_log.add("You have been killed!", colour=(255, 0, 0))

    def refresh_view(self):
        self.camera.follow(self.controlled_entity)
        self.visible_tiles = self.world.game_map.recompute_fov(
            self.controlled_entity.x,
            self.controlled_entity.y
        )
    
    def handle_enemy_turns(self):
        for enemy in self.world.enemies:
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
    
    def find_exit_tile(self):
        for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
            x = self.world.mech.x + dx
            y = self.world.mech.y + dy
            if not self.world.game_map.is_blocked(x, y, self.world.entities) and not self.world.game_map.is_tile_blocked(x,y):
                return x, y
        return self.world.mech.x, self.world.mech.y  # fallback (corpse ejection)

    def enter_mech(self):
        self.message_log.add("You enter the mech.", colour=(255, 255, 0))
        self.world.player.is_active = False
        self.world.player.container = self.world.mech
        self.controlled_entity = self.world.mech
        self.refresh_view()


    def exit_mech(self):
        self.message_log.add("You exit the mech.", colour=(255, 255, 0))
        self.world.player.is_active = True
        self.world.player.container = None
        self.world.player.x, self.world.player.y = self.find_exit_tile()
        self.controlled_entity = self.world.player
        self.refresh_view()


    def can_enter_mech(self) -> bool:
        if self.world.mech.stats["hp"] <= 0:
            return False
        dx = abs(self.world.player.x - self.world.mech.x)
        dy = abs(self.world.player.y - self.world.mech.y)
        return dx + dy == 1
    
    def toggle_controlled_entity(self):
        if self.controlled_entity == self.world.player:
            if self.can_enter_mech():
                self.enter_mech()
        elif self.controlled_entity == self.world.mech:
           self.exit_mech()
    
    def handle_mech_destroyed(self, mech: Entity):
        self.message_log.add("The mech explodes! You are violently ejected!", colour=(255, 50, 50))

        # Force exit BEFORE deactivating mech
        if self.controlled_entity == mech:
            self.exit_mech()

            # Apply ejection damage to player
            ejection_damage = 5
            self.world.player.stats["hp"] -= ejection_damage
            self.message_log.add(f"You take {ejection_damage} damage from the ejection!", colour=(255, 100, 100))

            if self.world.player.stats["hp"] <= 0:
                self.game_state = GameState.DEAD
                self.message_log.add("You died during the ejection.", colour=(255, 0, 0))

        mech.is_active = False

    
    def try_move(self, entity, dx, dy):
        dest_x = entity.x + dx
        dest_y = entity.y + dy
        # Map bounds check
        if not self.world.game_map.in_bounds(dest_x, dest_y):
            return
        blocker = self.world.get_blocking_entity_at(dest_x, dest_y)
        if blocker:
            attack = actions.AttackAction(entity, blocker)
            self.perform(attack)
            return
        if self.world.game_map.is_tile_blocked(dest_x, dest_y):
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
        self.visible_tiles = self.world.game_map.recompute_fov(self.controlled_entity.x, self.controlled_entity.y)
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


