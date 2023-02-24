import pygame
from settings import *
from constants import *


class UiGame:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        x, y = self.display_surface.get_size()

        size_set = x // 5 - 40
        y_delta = y - 120
        self.health_bar_rect = pygame.Rect(size_set, y_delta, BAR_WIDTH, BAR_HEIGHT)
        self.hungry_bar_rect = pygame.Rect(size_set * 2, y_delta, BAR_WIDTH, BAR_HEIGHT)
        self.temperature_bar_rect = pygame.Rect(size_set * 3, y_delta, BAR_WIDTH, BAR_HEIGHT)
        self.water_bar_rect = pygame.Rect(size_set * 4, y_delta, BAR_WIDTH, BAR_HEIGHT)

    def _show_bar(self, current, max_amount, bg_rect, color):
        pygame.draw.rect(self.display_surface, color, bg_rect, 1, border_radius=15)

        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        pygame.draw.rect(self.display_surface, color, current_rect, border_radius=15)

    def display(self, player):
        self._show_bar(player.health, player.stats[HEALTH], self.health_bar_rect, HEALTH_COLOR)
        self._show_bar(player.hungry, player.stats[HUNGRY], self.hungry_bar_rect, HUNGRY_COLOR)
        self._show_bar(player.temperature, player.stats[TEMPERATURE], self.temperature_bar_rect, TEMPERATURE_COLOR)
        self._show_bar(player.water, player.stats[WATER], self.water_bar_rect, WATER_COLOR)

    def start_game(self) -> bool:
        print("start game")
        return True

    def end_game(self) -> None:
        print("end game")

