import pygame
from constants import VERTICAL, HORIZONTAL


class Player(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, image: pygame.Surface, obstacles_sprites: pygame.sprite.Group, *groups):
        super().__init__(*groups)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

        self.direction = pygame.math.Vector2()
        self.speed = 5

        self.obstacles_sprites = obstacles_sprites

        self.main_score = 1000

    def __lt__(self, other):
        return self.main_score < other.main_score

    def set_direction(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_a]:
            self.direction.x = -1
        elif keys[pygame.K_d]:
            self.direction.x = 1
        else:
            self.direction.x = 0

    def move(self, speed: int):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.rect.x += self.direction.x * speed
        self.collision(HORIZONTAL)
        self.rect.y += self.direction.y * speed
        self.collision(VERTICAL)

    def collision(self, direction):
        if direction == HORIZONTAL:
            for sprite in self.obstacles_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.x > 0:
                        self.rect.right = sprite.rect.left
                    if self.direction.x < 0:
                        self.rect.left = sprite.rect.right

        if direction == VERTICAL:
            for sprite in self.obstacles_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.y > 0:
                        self.rect.bottom = sprite.rect.top
                    if self.direction.y < 0:
                        self.rect.top = sprite.rect.bottom

    def update(self) -> None:
        self.set_direction()
        self.move(self.speed)