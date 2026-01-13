# Constants
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50

MAP_VIEW_WIDTH = 65
MAP_VIEW_HEIGHT = 35
MAP_WORLD_WIDTH = 300
MAP_WORLD_HEIGHT = 300

LOG_HEIGHT = SCREEN_HEIGHT - MAP_VIEW_HEIGHT
STATPANEL_WIDTH = SCREEN_WIDTH - MAP_VIEW_WIDTH

base_stats = {
    "hp": 100,
    "max_hp": 100,
    "melee": 10,
    "accuracy": 75,
    "evasion": 10,
    "armor": 5,
    "speed": 100,
}

enemy_base_stats = {
    "hp": 50,   
    "max_hp": 50,
    "melee": 8,
    "accuracy": 60,
    "evasion": 5,
    "armor": 2,
    "speed": 80,
}

mech_base_stats = {
    "hp": 2,
    "max_hp": 2,
    "melee": 15,
    "accuracy": 85,
    "evasion": 15,
    "armor": 10,
    "speed": 40
}