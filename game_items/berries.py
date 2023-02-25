from item import Item
from load_functions import load_image


class Berries(Item):
    def __init__(self, pos, *group):
        image = load_image("game_items", "berries.png")
        super().__init__(pos, image, *group)

    def player_active(self, player):
        print("BERRIES USE!")
