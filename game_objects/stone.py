import load_functions
import random
from game_object import GameObject
from player import Player


class Stone(GameObject):
    def __init__(self, pos: tuple, *group):
        super().__init__(pos, load_functions.load_image("stone", "stone.png"), *group)
        self.main_score += random.randint(1, 2)
        self.hitbox = self.rect.inflate(-40, -40)

    def player_active(self, player: Player):
        print("STONE !!!")
