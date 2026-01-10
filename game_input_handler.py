import tcod
from actions import MoveAction, QuitAction, ToggleControlAction, WaitAction

class InputHandler:

    def __init__(self, engine):
        self.engine = engine    
        self.keymap = {
            #we use lambdas to delay the creation of the action until the key is pressed
            #this means that the action gets the current controlled_entity when created 
            #which prevents bugs if the controlled_entity changes
            tcod.event.KeySym.UP: lambda: MoveAction(self.engine.controlled_entity, 0, -1),
            tcod.event.KeySym.DOWN: lambda: MoveAction(self.engine.controlled_entity, 0, 1),
            tcod.event.KeySym.LEFT: lambda: MoveAction(self.engine.controlled_entity, -1, 0),
            tcod.event.KeySym.RIGHT: lambda: MoveAction(self.engine.controlled_entity, 1, 0),
            tcod.event.KeySym.e: lambda: ToggleControlAction(self.engine.controlled_entity),
            tcod.event.KeySym.PERIOD: lambda: WaitAction(self.engine.controlled_entity),
            tcod.event.KeySym.q: lambda: QuitAction(self.engine.controlled_entity),
        }
        
    def handle_input(self, event):
        if event.type != "KEYDOWN":
            return None # return None if not a keydown event
        action_factory = self.keymap.get(event.sym)
        if action_factory:
           return action_factory() #will return an action or True for quit
        return None