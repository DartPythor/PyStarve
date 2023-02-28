import sys
import pygame

from settings import FPS
from Ui import UiGame
from map import Map


class Game:
    def __init__(self, title: str, size: tuple):
        pygame.init()

        if size is None:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(size)
        self.width, self.height = pygame.display.get_window_size()
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(title)
        self.stats_bar_group = pygame.sprite.Group()
        self.ui_game = UiGame()
        self.map = Map("big_map.txt", self.ui_game)
        self.start_events()

    @staticmethod
    def terminate() -> None:
        pygame.quit()
        sys.exit()

    def start_events(self):
        self.HUNGRY = pygame.USEREVENT + 1
        pygame.time.set_timer(self.HUNGRY, 5 * 1000)
        self.HEALTH = pygame.USEREVENT + 2
        pygame.time.set_timer(self.HEALTH, 5 * 1000)
        self.WATER = pygame.USEREVENT + 3
        pygame.time.set_timer(self.WATER, 8 * 1000)
        self.TEMPERATURE = pygame.USEREVENT + 4
        pygame.time.set_timer(self.TEMPERATURE, 10 * 1000)
        self.SCORE = pygame.USEREVENT + 5
        pygame.time.set_timer(self.SCORE, 1 * 1000)

    def run(self) -> None:
        running = self.ui_game.start_game()

        while running is True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == self.HUNGRY:
                    self.map.player.hungry_time()
                if event.type == self.HEALTH:
                    self.map.player.check_health()
                if event.type == self.WATER:
                    self.map.player.water_time()
                if event.type == self.TEMPERATURE:
                    self.map.player.temperature_time()
                if event.type == self.SCORE:
                    self.map.player.score += 10

            self.map.run()
            self.clock.tick(FPS)
            pygame.display.update()
            if self.map.player.live is False:
                running = False
        else:
            self.ui_game.end_game()


if __name__ == '__main__':
    game = Game("PyStarve Alpha 1.1", (1400, 720))
    game.run()
