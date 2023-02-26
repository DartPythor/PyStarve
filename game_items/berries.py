from item import Item
from load_functions import load_image


class Berries(Item):
    def __init__(self):
        image = load_image("items", "berries.png")
        super().__init__(image)

    def player_active(self, player):
        print("BERRIES USE!")
