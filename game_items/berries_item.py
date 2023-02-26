from item import Item
from load_functions import load_image


class BerriesItem(Item):
    def __init__(self):
        image = load_image("items", "berries.png")
        self.type_obj = "berries"
        super().__init__(image)

    def player_active(self, player):
        print("BERRIES USE!")
        player.hungry += 5
        return 1