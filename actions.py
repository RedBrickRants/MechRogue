# actions.py
# Define various action classes that can be performed by entities in the game.

class Action:
    def __init__(self, entity):
        self.entity = entity
    def perform(self, engine):
        raise NotImplementedError()
    
class MoveAction(Action):
    def __init__(self, entity, dx, dy):
        super().__init__(entity)
        self.dx = dx
        self.dy = dy
    def perform(self, engine):
        engine.try_move(self.entity, self.dx, self.dy)

class WaitAction(Action):
    def perform(self, engine):
        if engine.game_state == engine.game_state.DEAD:
            return
        engine.message_log.add(f"{self.entity.name} waits.", colour=(173, 216, 230))

class ToggleControlAction(Action):
    def perform(self, engine):
        engine.toggle_controlled_entity()

class QuitAction(Action):
    def perform(self, engine):
        return "QUIT"

class AttackAction(Action):
    def __init__ (self, entity, target):
        super().__init__(entity)
        self.target = target
    def perform(self, engine):
        engine.damage_entity(self.target, self.entity.stats.get("melee", 0))

class PickupItemAction(Action):
    pass
class DropItemAction(Action):
    pass

class UseItemAction(Action):
    pass

class InteractAction(Action):
    pass