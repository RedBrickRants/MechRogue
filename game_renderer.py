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
    


def render_stats(console, entity):
    x = MAP_WIDTH + 2
    y = 3
    console.print(MAP_WIDTH + 2, 1, "STATS")
    console.print(x, y, f"{entity.name}", fg=(255, 255, 0))
    y += 1

    for stat_name, value in entity.stats.items():
        colour = (255, 255, 255)

        if stat_name == "hp":
            colour = (255, 100, 100)
        elif stat_name == "melee":
            colour = (255, 180, 100)
        elif stat_name == "accuracy":
            colour = (100, 255, 100)
        elif stat_name == "armor":
            colour = (150, 150, 255)
        elif stat_name == "speed":
            colour = (255, 255, 150)

        label = stat_name.upper().replace("_", " ")
        console.print(x, y, f"{label}: {value}", fg=colour)
        y += 1

# Log renderer
def render_log(console, log_messages: List[str]): 
    x = 2
    y = MAP_HEIGHT + 3
    for message in log_messages[-(console.height - MAP_HEIGHT - 3):]: 
        console.print(x, y, message, fg=(200, 200, 200))
        y += 1
