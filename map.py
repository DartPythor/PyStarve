import pygame

import load_functions
from game_object import Tree
from settings import SIZE_TILE
from player import Player


class Map:
    def __init__(self, level: str, tiles_types: dict):
        self.level = load_functions.load_level(level)
        self.tiles_types = tiles_types

        self.screen = pygame.display.get_surface()

        self.group_all_sprite = pygame.sprite.Group()
        self.group_visible_sprite = pygame.sprite.Group()
        self.group_obstacles_sprite = pygame.sprite.Group()

        self.array_tile = self._create_array_tile(self.level)

    def _create_array_tile(self, level: list) -> list:
        result = []

        for y, column in enumerate(level):
            column_result = []

            for x, item in enumerate(column):

                if item == "#":
                    Tree((x * SIZE_TILE, y * SIZE_TILE), self.group_all_sprite, self.group_obstacles_sprite)
                elif item == "p":
                    Player((x * SIZE_TILE, y * SIZE_TILE), load_functions.load_image("player", "starver.png"),
                           self.group_obstacles_sprite, self.group_all_sprite)

            result.append(column_result)

        return result

    def run(self) -> None:
        self.group_all_sprite.update()
        self.screen.fill((1, 50, 32))
        for sprite in sorted(self.group_all_sprite):
            self.screen.blit(sprite.image, sprite.rect)
