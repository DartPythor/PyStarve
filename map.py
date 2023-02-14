import pygame

import load_functions
from errorsTypes import MapFormatError
from tile import Tile
from game_object import Tree
from settings import SIZE_TILE


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
                if item not in self.tiles_types:
                    raise MapFormatError(f"Invalid format map '{item}'")
                column_result.append(
                    Tile((x * SIZE_TILE, y * SIZE_TILE), load_functions.load_image("background", "green.png"),
                         self.group_all_sprite))

                if item == "#":
                    Tree((x * SIZE_TILE, y * SIZE_TILE), self.group_all_sprite)

            result.append(column_result)

        return result

    def run(self) -> None:
        for sprite in sorted(self.group_all_sprite):
            self.screen.blit(sprite.image, sprite.rect)


if __name__ == '__main__':
    map = Map("test_map.txt", {"#": 1, ".": 2, "p": 3})
    print(map.array_tile)
