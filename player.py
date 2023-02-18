import math

import pygame

import load_functions
from constants import VERTICAL, HORIZONTAL, ATTACK, MOVE, STAND


class Player(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, image: pygame.Surface, obstacles_sprites: pygame.sprite.Group, *groups):
        super().__init__(*groups)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.origin_image = image
        self.offset = pygame.math.Vector2()

        self.direction = pygame.math.Vector2()
        self.speed = 5

        self.status = "stating"

        self.obstacles_sprites = obstacles_sprites
        self.camera = groups[0]

        self.hitbox = self.rect.inflate(-30, -30)
        # (196, 216)
        self.main_score = 1000

        self.right_hand = PlayerHand(self, 1, load_functions.load_image("hands", "starver_hand.png"), *groups)
        self.left_hand = PlayerHand(self, 0, load_functions.load_image("hands", "starver_hand.png"), *groups)

    def __lt__(self, other):
        return self.main_score < other.main_score

    def animation_player_see(self):
        offset_pos = self.rect.center - self.camera.offset
        angel = load_functions.rotate(pygame.mouse.get_pos(), (offset_pos.x, offset_pos.y)) + 90
        last_x, last_y = self.rect.centerx, self.rect.centery
        self.right_hand.set_position(self.camera.offset)
        self.left_hand.set_position(self.camera.offset)
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

    def set_status(self):
        actives = []
        if pygame.mouse.get_pressed()[0]:
            actives.append(ATTACK)

        if self.direction.x == 0 and self.direction.y == 0:
            actives.append(STAND)
        else:
            actives.append(MOVE)

        self.status = "_".join(actives)

    def attack(self):
        ...

    def animation_hands(self):
        ...

    def update(self) -> None:
        self.animation_player_see()
        self.set_direction()
        self.set_status()
        self.move(self.speed)


class PlayerHand(pygame.sprite.Sprite):
    def __init__(self, player: Player, type_hand: int, image: pygame.Surface, *groups):
        super().__init__(*groups)

        self.player = player
        self.image = image
        self.rect = self.image.get_rect()

        self.main_score = player.main_score

        self.x, self.y = self.player.rect.center
        self.distance = 70
        if type_hand:
            self.rect.center = (self.x + self.distance, self.y)
        else:
            self.rect.center = (self.x - self.distance, self.y)
        self.type_hand = type_hand

    def __lt__(self, other):
        return self.main_score < other.main_score

    def set_position(self, offset):
        m_x, m_y = pygame.mouse.get_pos()[0] + offset.x, pygame.mouse.get_pos()[1] + offset.y
        p_x, p_y = self.player.rect.center

        if self.type_hand:
            k = math.radians(90)
        else:
            k = -math.radians(90)

        a = math.atan2((p_y - m_y), (p_x - m_x)) + k

        self.rect.centerx = int(p_x + self.distance * math.cos(a))
        self.rect.centery = int(p_y + self.distance * math.sin(a))

    def animation_attack(self):
        ...

    def update(self) -> None:
        ...
