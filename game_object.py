import random

import pygame

import load_functions
from player import Player


class GameObject(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, image: pygame.surface.Surface, *group):

        super().__init__(*group)
        self.image = image
        self.rect = image.get_rect()

        self.rect.x = pos[0]
        self.rect.y = pos[1]

        self.hitbox = self.rect.inflate(-20, -20)

        self.main_score = 100

    def __lt__(self, other):
        return self.main_score < other.main_score

    def player_active(self, player: Player):
        ...
