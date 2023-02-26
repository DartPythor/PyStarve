import load_functions
import random
from game_object import GameObject
from player import Player
from game_items.berries_item import BerriesItem


class Berries(GameObject):
    def __init__(self, pos: tuple, *group):
        super().__init__(pos, load_functions.load_image("berries", "berries.png"), *group)
        self.main_score += random.randint(1, 2)
        self.hitbox = self.rect.inflate(-38, -38)

    def player_active(self, player: Player):
        player.inventory.get_new_item(BerriesItem(), 1)
        super().player_active(player)
