# enemy_defs.py

ENEMY_DEFS = {
    "grunt": {
        "name": "Grunt",
        "char": "g",
        "colour": (200, 50, 50),
        "base_stats": {
            "hp": 50,
            "max_hp": 50,
            "melee": 8,
            "accuracy": 60,
            "evasion": 5,
            "armor": 2,
            "speed": 80,
        },
        "ai_type": "basic",
        "traits": [],
        "loot": [],
    },

    "skirmisher": {
        "name": "Skirmisher",
        "char": "s",
        "colour": (200, 200, 50),
        "base_stats": {
            "hp": 35,
            "max_hp": 35,
            "melee": 6,
            "accuracy": 75,
            "evasion": 15,
            "armor": 1,
            "speed": 120,
        },
        "ai_type": "chaotic",
        "traits": [],
        "loot": [],
    },
}
