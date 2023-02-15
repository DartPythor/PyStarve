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

        self.ui_game = UiGame()
        self.map = Map("big_map.txt")

    @staticmethod
    def terminate() -> None:
        pygame.quit()
        sys.exit()

    def run(self) -> None:
        running = self.ui_game.start_game()

        while running is True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.map.run()
            self.clock.tick(FPS)
            pygame.display.update()
        else:
            self.ui_game.end_game()


if __name__ == '__main__':
    game = Game("PyStarve Alpha 0.1", None)
    game.run()
