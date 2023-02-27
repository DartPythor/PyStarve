import pygame

import load_functions
import random
from game_object import GameObject
from player import Player
from game_items.berries_item import BerriesItem


class Berries(GameObject):
    def __init__(self, pos: tuple, *group):
        super().__init__(pos, load_functions.load_image("berries", "berries0.png"), *group)
        self.main_score += random.randint(1, 2)
        self.hitbox = self.rect.inflate(-38, -38)
        self.berries_count = 5
        self.time = pygame.time.get_ticks()
        self.array_image = [load_functions.load_image("berries", f"berries{i}.png", -1) for i in range(0, 6)]

    def player_active(self, player: Player):
        if self.berries_count > 0:
            player.inventory.get_new_item(BerriesItem(), 1)
            self.berries_count -= 1
        self.image = self.array_image[self.berries_count]
        super().player_active(player)

    def update(self) -> None:
        super().update()
        time = (pygame.time.get_ticks() - self.time) // 1000
        if time >= 6:
            self.time = pygame.time.get_ticks()
            if self.berries_count + 1 <= 5:
                self.berries_count += 1
            else:
                self.berries_count = 5

        self.image = self.array_image[self.berries_count]
