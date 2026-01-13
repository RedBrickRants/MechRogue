from typing import Tuple

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
        self.modifer.setdefault(stat, [].append(modifier))

class Trait:
    def on_damage(self, entity, amount, source): pass
    def on_death(self, entity, engine): pass

class Entity:
    def __init__(self, name: str, char: str, colour: Tuple[int, int, int], x: int, y:int, base_stats, is_mech: bool, blocks: bool = True):
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

    

    def take_damage(self, amount: int, source=None):
        armor = self.stats.get_stat("armor")
        final = max(1, amount - armor)
        new_hp = self.stats.get_stat("hp") - final
        self.stats.set_stat("hp", max(0, new_hp))
        return final

        