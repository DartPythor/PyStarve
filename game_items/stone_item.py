from item import Item
from load_functions import load_image


class StoneItem(Item):
    def __init__(self):
        image = load_image("items", "stone.png")
        self.type_obj = "stone"
        super().__init__(image)

    def player_active(self, player):
        print("STONE USE!")
        return 0