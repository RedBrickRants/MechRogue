from enemy_definitions import ENEMY_DEFS
from game_entity import Enemy
import copy

class EnemyFactory:
    @staticmethod
    def create(enemy_id: str, x: int ,y: int):
        data = ENEMY_DEFS[enemy_id]
        return Enemy(name= data["name"], char= data["char"], colour= data["colour"], x=x, y=y, base_stats = copy.deepcopy(data["base_stats"]), traits = list(data.get("traits", [])), ai_type=data.get("ai_type", "basic"),)