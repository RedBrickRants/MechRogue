import tcod
import tcod.console
import numpy as np
from game_engine import Engine
import random
from typing import List, Tuple, Optional
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, MAP_WIDTH, MAP_HEIGHT
import game_renderer
from game_entity import Entity

def main ():
    engine = Engine()
    engine.spawn_enemies(5)

    # Set tileset
    tileset = tcod.tileset.load_tilesheet(
        "assets/dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )
    #Create the tcod context (OS Window) ie the box that holds the game.
    with tcod.context.new( columns= SCREEN_WIDTH, rows= SCREEN_HEIGHT, tileset=tileset, title="MechRogue") as context:
        #create the root console (the main console we will draw to)
        root_console = tcod.console.Console(SCREEN_WIDTH, SCREEN_HEIGHT, order="F")

        #game loop 
        while True:
            #clear the console
            root_console.clear()

            #Draw the entites at their current position
            game_renderer.render_entities(root_console, engine.entities)
                
            #Draw the map 
            game_renderer.render_game_bounds(root_console)
            #Draw the player stats
            game_renderer.render_stats(root_console, engine.controlled_entity)
            #Draw the log messages
            game_renderer.render_log(root_console, engine.log_messages)
            #present console to context (draw to screen)
            context.present(root_console)
            #listen for and handle events
            for event in tcod.event.wait():
                if isinstance(event, tcod.event.Quit):
                    return  #exit game loop and end program
                if engine.handle_input(event):
                    return

if __name__ == "__main__":
    main()