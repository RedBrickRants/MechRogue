#game_entity.py
from typing import Tuple
import random

class Stats:
    def __init__(self, base: dict):
        self.base = base.copy()
        self.modifiers = {}
    
    def get_stat(self, stat: str):
        value = self.base.get(stat,0)
        for mod in self.modifiers.get(stat,[]):
            value = mod(value)
        return value
    def set_stat(self, stat: str, value):
        self.base[stat] = value

    #def get_stats(self):
        #for stat, value in self.base:
         #   return 
    def add_modifier(self, stat: str, modifier):
        self.modifiers.setdefault(stat, []).append(modifier)

class Trait:
    def on_damage(self, entity, amount, source): pass
    def on_death(self, entity, engine): pass

class Entity:
    def __init__(self, name: str, char: str, colour: Tuple[int, int, int], x: int, y:int, base_stats, is_mech: bool, blocks: bool = True, faction = "neuteral"):
        self.name = name
        self.char = char
        self.colour = colour
        self.x = x
        self.y = y
        self.stats = Stats(base_stats)
        self.traits = []
        self.effects = []
        self.is_mech = is_mech
        self.blocks = blocks
        self.is_active = True   # is this entity currently on the map?
        self.container = None  # what entity (if any) is holding this one
        self.base_faction = faction

    @property
    def faction(self):
        # If this entity is being piloted, inherit faction
        if self.container:
            return self.container.faction
        return self.base_faction

    def take_damage(self, amount: int, source=None):
        armor = self.stats.get_stat("armor")
        final = max(1, amount - armor)
        new_hp = self.stats.get_stat("hp") - final
        self.stats.set_stat("hp", max(0, new_hp))
        return final

class Enemy(Entity):
        def __init__(self, name = "Grunt", char = "g", colour = (200,50,50), x = 0, y = 0, base_stats=None, traits=None, ai_type="basic", faction = "enemy"):
            from constants import enemy_base_stats

            base_stats = base_stats or enemy_base_stats
            super().__init__(name,char, colour, x, y, base_stats, is_mech=False, blocks=True, faction= faction)
            self.ai_type = ai_type

            self.traits = traits or []

            self.loot_table = []

        def on_turn(self, engine):
            if not self.is_active:
                return
            target = engine.controlled_entity

            if not self.can_see(engine, target):
                return

            if self.ai_type == "basic":
                self.basic_ai_move(engine, target)
            if self.ai_type == "chaotic":
                self.chaotic_ai_move(engine)

        def basic_ai_move(self, engine, target):
            dx = target.x - self.x
            dy = target.y - self.y
            step_x = 0 if dx == 0 else (1 if dx > 0 else -1)
            step_y = 0 if dy == 0 else (1 if dy > 0 else -1)

            if abs(dx) > abs(dy):
                engine.try_move(self, step_x, 0)
            else:
                engine.try_move(self, 0, step_y)

        def can_see(self, engine, target):
            if not engine.world.game_map.in_bounds(target.x, target.y):
                return False
            return engine.visible_tiles[target.x, target.y]
        def chaotic_ai_move(self, engine):
            # Random movement each turn
            dx = random.randint(-1,1)
            dy = random.randint(-1,1)
            engine.try_move(self, dx, dy)

        def drop_loot(self, engine):
            for item, chance in self.loot_table:
                if random.random() < chance:
                    engine.world.entities.append(item)  # Or a proper item spawn method

        def on_death(self, engine):
            self.is_active = False
            self.drop_loot(engine)
            for trait in self.traits:
                trait.on_death(self, engine)