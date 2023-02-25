class Inventory:
    def __init__(self, player, start_inventory=None, count_slots=10):
        self.count_slots = count_slots
        if start_inventory is None:
            self.inventory = {i: None for i in range(1, 11)}
        else:
            self.inventory = start_inventory
        self.player = player

    def get_size_inv(self) -> int:
        return list(self.inventory.values()).count(None)

    def get_new_item(self, item):
        if self.get_size_inv() <= 0:
            return None

        for i in self.inventory.keys():
            if self.inventory[i] is None:
                self.inventory[i] = item
                return i

    def use_item(self, index_item):
        if self.inventory[index_item] is None:
            return None
        self.inventory[index_item].use_item(self.player)

    def delete_item(self, index_item):
        if self.inventory[index_item] is None:
            return None
        self.inventory[index_item] = self.inventory[index_item].delete_item()


class InventorySlot:
    def __init__(self, max_count, count, item):
        self.max_count = max_count
        self.count = count
        self.item = item

    def use_item(self, player):
        self.count -= self.item.player_active(player)
        if self.count <= 0:
            return self.delete_item()

    def add_count_item(self, count):
        self.count += count

    def delete_item(self):
        return None


if __name__ == '__main__':
    inv = Inventory(1)
    inv.get_new_item(InventorySlot(10, 1, 1))
    inv.get_new_item(InventorySlot(10, 1, 1))
    inv.get_new_item(InventorySlot(10, 2, 1))
    inv.delete_item(3)
    print(inv.inventory)
