import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, image: pygame.Surface, *groups):
        super().__init__(*groups)

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

        self.main_score = 1
    def __lt__(self, other):
        return self.main_score < other.main_score
