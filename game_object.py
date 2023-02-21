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
        self.trigger = 10
        self.delta_x = None
        self.delta_y = None

        self.move = 0

    def __lt__(self, other):
        return self.main_score < other.main_score

    def player_active(self, player: Player):
        if self.move not in (2, 3):
            self.move = 1
            self.delta_x = 1 if player.rect.centerx - self.rect.centerx > 0 else -1
            self.delta_y = 1 if player.rect.centery - self.rect.centery > 0 else -1

    def move_object(self):
        if self.move == 1:
            self.trigger -= 1
            self.rect.centerx -= self.delta_x
            self.rect.centery -= self.delta_y
            if self.trigger == 0:
                self.move = 2

        if self.move == 2:
            self.trigger += 1
            self.rect.centerx += self.delta_x
            self.rect.centery += self.delta_y
            if self.trigger == 10:
                self.move = 0

    def update(self) -> None:
        self.move_object()