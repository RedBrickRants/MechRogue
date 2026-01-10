from constants import MAP_WIDTH, MAP_HEIGHT
from game_entity import Entity
from typing import List

def render_game_bounds(console):
    for y in range(MAP_HEIGHT):
        console.print(MAP_WIDTH, y, '|', fg=(255, 255, 255))

    for x in range(MAP_WIDTH):
        console.print(x, MAP_HEIGHT, '-', fg=(255, 255, 255))

    console.print(MAP_WIDTH, MAP_HEIGHT, '+', fg=(255, 255, 255))

    console.print(2, MAP_HEIGHT + 1, "LOG")
    

def render_entities(console, entities):
    for entity in entities:
        if entity.is_active:
            console.print(entity.x, entity.y, entity.char, fg=entity.colour)
    


def render_stats(console, entity, start_x, start_y):
    y = start_y
    console.print(start_x, y, entity.name, fg=(255, 255, 0))
    y += 1

    for stat, value in entity.stats.items():
        console.print(start_x, y, f"{stat.upper()}: {value}")
        y += 1

    return y

# Log renderer
def render_log(console, log_messages: List[str]): 
    x = 2
    y = MAP_HEIGHT + 3
    for message in log_messages[-(console.height - MAP_HEIGHT - 3):]: 
        console.print(x, y, message, fg=(200, 200, 200))
        y += 1
