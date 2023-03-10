import pygame

import load_functions
from settings import SIZE_TILE
from player import Player
from camera import Camera

from game_objects.tree import Tree
from game_objects.stone import Stone
from game_objects.berries import Berries
from game_objects.river import River
from game_objects.furnace import Furnace


class Map:
    def __init__(self, level: str, ui):
        self.level = load_functions.load_level(level)
        self.ui = ui

        self.screen = pygame.display.get_surface()

        width_map = len(self.level[0]) * SIZE_TILE
        height_map = len(self.level) * SIZE_TILE

        self.group_all_sprite = Camera(width_map, height_map)
        self.group_visible_sprite = Camera(width_map, height_map)
        self.group_obstacles_sprite = Camera(width_map, height_map)
        self.river_sprite_group = pygame.sprite.Group()
        self.furnace_sprite_group = pygame.sprite.Group()
        self._create_array_tile(self.level)

    def _create_array_tile(self, level: list) -> None:
        for y, column in enumerate(level):
            for x, item in enumerate(column):
                if item == "#":
                    Tree((x * SIZE_TILE, y * SIZE_TILE), self.group_all_sprite, self.group_obstacles_sprite)
                elif item == "p":
                    self.player = Player((x * SIZE_TILE, y * SIZE_TILE),
                                         load_functions.load_image("player", "starver.png"),
                                         self.group_obstacles_sprite, self.river_sprite_group, self.group_all_sprite)
                elif item == "S":
                    Stone((x * SIZE_TILE, y * SIZE_TILE), self.group_all_sprite, self.group_obstacles_sprite)
                elif item == "B":
                    Berries((x * SIZE_TILE, y * SIZE_TILE), self.group_all_sprite, self.group_obstacles_sprite)
                elif item == "F":
                    self.fire = Furnace((x * SIZE_TILE, y * SIZE_TILE), self.group_all_sprite, self.group_obstacles_sprite, self.furnace_sprite_group)
                elif item in "1234567":
                    River((x * SIZE_TILE, y * SIZE_TILE), f"river{item}.png", self.group_all_sprite, self.river_sprite_group)
        self.player.pos_fire = self.fire

    def run(self) -> None:
        self.group_all_sprite.custom_draw(self.player)
        self.group_all_sprite.update()
        self.ui.display(self.player)
