import math

import pygame

import load_functions
from constants import VERTICAL, HORIZONTAL


class Player(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, image: pygame.Surface, obstacles_sprites: pygame.sprite.Group, *groups):
        super().__init__(*groups)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.origin_image = image
        self.oofset = pygame.math.Vector2()

        self.direction = pygame.math.Vector2()
        self.speed = 5

        self.obstacles_sprites = obstacles_sprites
        self.camera = groups[0]

        self.hitbox = self.rect.inflate(0, -25)
        self.main_score = 1000

    def __lt__(self, other):
        return self.main_score < other.main_score

    def animation_player_see(self):
        offset_pos = self.rect.center - self.camera.offset
        angel = load_functions.rotate(pygame.mouse.get_pos(), (offset_pos.x, offset_pos.y)) + 90
        last_x, last_y = self.rect.centerx, self.rect.centery
        self.image = pygame.transform.rotate(self.origin_image, angel)
        self.rect = self.image.get_rect(center=(last_x, last_y))

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

        self.hitbox.x += self.direction.x * speed
        self.collision(HORIZONTAL)
        self.hitbox.y += self.direction.y * speed
        self.collision(VERTICAL)
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        if direction == HORIZONTAL:
            for sprite in self.obstacles_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right

        if direction == VERTICAL:
            for sprite in self.obstacles_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom

    def update(self) -> None:
        self.animation_player_see()
        self.set_direction()
        self.move(self.speed)