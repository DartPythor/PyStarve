import pygame as pygame


class Item(pygame.sprite.Sprite):
    def __init__(self, pos, image, *group):
        super().__init__(*group)
        self.image = image
        self.rect = image.get_rect()

        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.main_score = 100

    def __lt__(self, other):
        return self.main_score < other.main_score

    def player_active(self, player):
        pass
