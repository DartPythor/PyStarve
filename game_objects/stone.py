import load_functions
import random
from game_object import GameObject
from player import Player
from game_items.stone_item import StoneItem


class Stone(GameObject):
    def __init__(self, pos: tuple, *group):
        super().__init__(pos, load_functions.load_image("stone", "stone.png"), *group)
        self.main_score += random.randint(1, 2)
        self.start_pos = self.rect.center
        self.hitbox = self.rect.inflate(-40, -40)

    def player_active(self, player: Player):
        player.inventory.get_new_item(StoneItem(), 1)
        super().player_active(player)

    def update(self) -> None:
        self.move_object()
