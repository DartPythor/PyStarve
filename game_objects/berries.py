import pygame

import load_functions
import random
from game_object import GameObject
from player import Player
from game_items.berries_item import BerriesItem


class Berries(GameObject):
    def __init__(self, pos: tuple, *group):
        super().__init__(pos, load_functions.load_image("berries", "berries.png"), *group)
        self.main_score += random.randint(1, 2)
        self.hitbox = self.rect.inflate(-38, -38)
        self.berries_count = 0
        self.time = pygame.time.get_ticks()

    def player_active(self, player: Player):
        times = pygame.time.get_ticks() - self.time
        count = times // 1000 // 3

        if self.berries_count + count >= 5:
            self.berries_count = 5
        else:
            self.berries_count += count
        if self.berries_count > 0:
            player.inventory.get_new_item(BerriesItem(), 1)
            self.berries_count -= 1
            self.time = pygame.time.get_ticks()
        super().player_active(player)
