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
            if engine.game_state == engine.game_state.DEAD:
                game_renderer.render_death_screen(root_console)
                game_renderer.render_game_bounds(root_console)
                game_renderer.render_log(root_console, engine.message_log.messages, log_x, log_y, log_height)
            else:
                #clear the console
                root_console.clear()

                #Draw the entites at their current position
                game_renderer.render_entities(root_console, engine.entities)
                    
                #Draw the map 
                game_renderer.render_game_bounds(root_console)
                #Draw the player stats
                stats_x = MAP_WIDTH + 2
                stats_y = 3

                log_x = 2
                log_y = MAP_HEIGHT + 3
                log_height = SCREEN_HEIGHT - MAP_HEIGHT - 3

                game_renderer.render_stats(root_console, engine.player, stats_x, stats_y)

                stats_y += len(engine.player.stats) + 2  #space between stat panels
                if engine.controlled_entity != engine.player:
                    game_renderer.render_stats(root_console, engine.controlled_entity, stats_x, stats_y)
                    
                #Draw the log messages
                game_renderer.render_log(root_console, engine.message_log.messages, log_x, log_y, log_height)
                #present console to context (draw to screen)
            context.present(root_console)

            #listen for and handle events
            for event in tcod.event.wait():
                if isinstance(event, tcod.event.Quit):
                    return  #exit game loop and end program
                if engine.handle_input(event):
                    return
            engine.update()
if __name__ == "__main__":
    main()