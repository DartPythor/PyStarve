import pygame
import load_functions
import random
from game_object import GameObject
from player import Player


class Furnace(GameObject):
    def __init__(self, pos: tuple, *group):
        super().__init__(pos, load_functions.load_image("furnace", "furnace0.png"), *group)
        self.main_score += random.randint(1, 2)
        self.start_pos = self.rect.center
        self.hitbox = self.rect.inflate(-40, -40)

        self.array_image = [load_functions.load_image("furnace", f"furnace{i}.png", -1) for i in range(0, 2)]
        self.fire = load_functions.load_image("furnace", "fire.png", -1)
        self.fire.set_alpha(128)
        self.camera = group[0]
        self.display = pygame.display.get_surface()
        self.player = None

        self.time_work = 0
        self.work = False
        self.image = self.array_image[self.work]
        self.time = pygame.time.get_ticks()

    def check_inventory(self, player):
        stone, wood = 0, 0
        array = []
        for key, item in zip(player.inventory.inventory.keys(), player.inventory.inventory.values()):
            if item is None:
                continue

            if item.item.type_obj == "stone":
                stone += item.count
                array.append(key)
            if item.item.type_obj == "wood":
                wood += item.count
                array.append(key)
        return stone, wood, array

    def player_active(self, player: Player):
        if self.player is None:
            self.player = player
        stone, wood, array = self.check_inventory(player)
        if stone >= 5 and wood >= 5:
            self.time_work += 10
            for key in array:
                for _ in range(5):
                    player.inventory.use_item(key)

        super().player_active(player)

    def create_effect(self):
        if self.time_work > 0:
            x, y = self.rect.center - self.camera.offset
            self.display.blit(self.fire, (x - 180, y - 180))

    def update(self) -> None:
        if self.time_work > 0:
            if (pygame.time.get_ticks() - self.time) // 1000 >= 1:
                self.time_work -= 1
                self.time = pygame.time.get_ticks()
        self.create_effect()
        self.work = self.time_work > 0
        self.image = self.array_image[self.work]
        super().update()
