from constants import MAP_WORLD_WIDTH, MAP_WORLD_HEIGHT, MAP_VIEW_WIDTH, MAP_VIEW_HEIGHT

from game_entity import Entity
from typing import List

def render_game_bounds(console):
    for y in range(MAP_VIEW_HEIGHT):
        console.print(MAP_VIEW_WIDTH, y, '|', fg=(255, 255, 255))

    for x in range(MAP_VIEW_WIDTH):
        console.print(x, MAP_VIEW_HEIGHT, '-', fg=(255, 255, 255))

    console.print(MAP_VIEW_WIDTH, MAP_VIEW_HEIGHT, '+', fg=(255, 255, 255))

    console.print(2, MAP_VIEW_HEIGHT + 1, "LOG")
    

def render_entities(console, entities, camera):
    for entity in entities:
        if not entity.is_active:
            continue
        screen_x = entity.x -camera.x
        screen_y = entity.y -camera.y
        if 0 <= screen_x < camera.width and 0<=screen_y<camera.height:
            console.print(screen_x, screen_y, entity.char, fg=entity.colour)
    
def render_map(console, map, camera):
    for x in range(map.width):
        for y in range(map.height):
            screen_x = x-camera.x
            screen_y = y-camera.y
        if 0<=screen_x<camera.width and 0<=screen_y<camera.height:
            tile = map.tiles[x][y]
            console.print(camera.x, camera.y, tile.glyph, fg=tile.colour)
        

def render_stats(console, entity, start_x, start_y):
    y = start_y
    console.print(start_x, y, entity.name, fg=(255, 255, 0))
    y += 1

    for stat, value in entity.stats.items():
        console.print(start_x, y, f"{stat.upper()}: {value}")
        y += 1

    return y

# Log renderer
def render_log(console, log_messages: List[str], x, y, height): 
    messages_to_render = list(log_messages)[-height:]
    for i, message in enumerate(messages_to_render): 
        text = message.text
        if message.count > 1:
            text += f" (x{message.count})"

        console.print(x, y+i, text, fg=message.colour)


def render_death_screen(console):
    console.clear()
    console.print(MAP_VIEW_WIDTH // 2 - 5, MAP_VIEW_HEIGHT // 2, "YOU DIED", fg=(255, 0, 0))
    console.print(MAP_VIEW_WIDTH // 2 - 10, MAP_VIEW_HEIGHT // 2 + 2, "Press 'q' to quit", fg=(255, 255, 255))