import random

import pygame

import load_functions


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

    def player_active(self):
        ...


class Tree(GameObject):
    def __init__(self, pos: tuple, *group):
        super().__init__(pos, load_functions.load_image("tree", "tree1.png"), *group)
        self.main_score += random.randint(1, 2)