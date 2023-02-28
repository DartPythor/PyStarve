from item import Item
from load_functions import load_image


class WoodItem(Item):
    def __init__(self):
        image = load_image("items", "wood.png")
        self.type_obj = "wood"
        super().__init__(image)

    def player_active(self, player):
        return 1
