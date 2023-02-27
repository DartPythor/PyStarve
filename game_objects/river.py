import load_functions
import random
from game_object import GameObject
from player import Player


class River(GameObject):
    def __init__(self, pos: tuple, image_river: str, *group):
        super().__init__(pos, load_functions.load_image("river", image_river), *group)
        self.main_score += random.randint(1, 2)
        self.hitbox = self.rect.inflate(-38, -38)

    def player_active(self, player: Player):
        print("PLAYER IN WATER")
