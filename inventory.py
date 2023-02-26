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

    def get_new_item(self, item, count):
        if self.get_size_inv() <= 0:
            return None

        for key, obj in zip(self.inventory.keys(), self.inventory.values()):
            if obj is not None and item.type_obj == obj.item.type_obj and obj.max_count >= obj.count + 1:
                obj.add_count_item(1)
                break

            if obj is None:
                self.inventory[key] = InventorySlot(99, count, item)
                break

    def use_item(self, index_item):
        if self.inventory[index_item] is None:
            return None
        self.inventory[index_item] = self.inventory[index_item].use_item(self.player)

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
        return self

    def add_count_item(self, count):
        self.count += count

    def delete_item(self):
        return None
