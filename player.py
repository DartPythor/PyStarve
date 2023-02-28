import math
import pygame

import load_functions
from constants import *
from inventory import Inventory


class Player(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, image: pygame.Surface, obstacles_sprites: pygame.sprite.Group,
                 river_group: pygame.sprite.Group, *groups):
        super().__init__(*groups)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.origin_image = image
        self.offset = pygame.math.Vector2()

        self.direction = pygame.math.Vector2()

        self.status = "stating"

        self.obstacles_sprites = obstacles_sprites
        self.water_group = river_group
        self.camera = groups[0]

        self.hitbox = self.rect.inflate(-30, -30)

        self.main_score = 1000

        self.right_hand = PlayerHand(self, 0, load_functions.load_image("hands", "starver_hand.png"), *groups)
        self.left_hand = PlayerHand(self, 1, load_functions.load_image("hands", "starver_hand.png"), *groups)

        self.attacking = False
        self.attack_cooldown = 500
        self.attack_time = None

        self.get_point_cooldown = False

        self.stats = {HEALTH: 100, DAMAGE: 10, SPEED: 5, WATER: 100, HUNGRY: 100, TEMPERATURE: 100}
        self.health = self.stats[HEALTH]
        self.damage = self.stats[DAMAGE]
        self.speed = self.stats[SPEED]
        self.water = self.stats[WATER]
        self.hungry = self.stats[HUNGRY]
        self.temperature = self.stats[TEMPERATURE]
        self.inventory = Inventory(self)
        self.inventory_use = False
        self.last_use_inv = None
        self.live = True

        self.pos_fire = None

    def __lt__(self, other):
        return self.main_score < other.main_score

    def get_sprite(self, point):
        for sprite in self.obstacles_sprites:
            if sprite.rect.collidepoint(point):
                return sprite

    def sprite_active(self, sprite):
        sprite.player_active(self)

    def animation_player_see(self):
        offset_pos = self.rect.center - self.camera.offset
        angel = load_functions.rotate(pygame.mouse.get_pos(), (offset_pos.x, offset_pos.y)) + 90
        last_x, last_y = self.rect.centerx, self.rect.centery
        self.right_hand.set_position(self.camera.offset)
        if self.attacking:
            point_active = self.right_hand.attack(self.camera.offset)
            if self.get_point_cooldown:
                sprite = self.get_sprite(point_active)
                if sprite is not None: self.sprite_active(sprite)

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

        gets_hit = self.get_water_collision()

        if gets_hit is True:
            self.speed = self.stats[SPEED] // 2
        else:
            self.speed = self.stats[SPEED]

        if pygame.mouse.get_pressed()[0] and not self.attacking:
            self.attack_time = pygame.time.get_ticks()
            self.attacking = True
            self.get_point_cooldown = True
        if self.inventory_use is False:
            self.set_inventory()

    def set_inventory(self):
        keys = pygame.key.get_pressed()
        for i in (
                pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8,
                pygame.K_9):
            if keys[i] is True:
                self.inventory_use = True
                self.last_use_inv = pygame.time.get_ticks()
                self.inventory.use_item(i - 48)

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

    def get_water_collision(self):
        for sprite in self.water_group:
            if sprite.hitbox.colliderect(self.hitbox):
                return True
        return False

    def set_status(self):
        actives = []
        if pygame.mouse.get_pressed()[0]:
            actives.append(ATTACK)

        if self.direction.x == 0 and self.direction.y == 0:
            actives.append(STAND)
        else:
            actives.append(MOVE)

        self.status = "_".join(actives)

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
        if self.get_point_cooldown:
            if current_time - self.attack_time >= 1:
                self.get_point_cooldown = False
        if self.inventory_use:
            if current_time - self.last_use_inv >= 200:
                self.inventory_use = False

    def update(self) -> None:
        self.animation_player_see()
        self.set_direction()
        self.set_status()
        self.cooldowns()
        self.move(self.speed)
        self.check_live()

    def hungry_time(self):
        if self.hungry > 0:
            self.hungry -= 10

    def water_time(self):
        gets_hit = self.get_water_collision()

        if gets_hit is True and self.water < 100:
            self.water += 10
        if self.water > 0 and gets_hit is False:
            self.water -= 10

    def temperature_time(self):
        x, y = self.pos_fire.rect.center
        x1, y1 = self.rect.center
        k = math.sqrt((x1 - x) ** 2 + (y1 - y) ** 2)
        if k <= 140 and self.pos_fire.time_work > 0:
            if self.temperature < 100:
                self.temperature += 10
        else:
            if self.temperature > 0:
                self.temperature -= 10

    def check_health(self):
        if all((self.hungry > 0, self.water > 0, self.temperature > 0)) is False:
            self.health -= 10

        elif self.health + 10 > 100:
            self.health = 100

        elif self.health < 100:
            self.health += 10

    def check_live(self):
        if self.health <= 0:
            self.live = False

    def eat(self, count):
        if self.hungry + count > 100:
            self.hungry = 100
        if self.hungry < 100:
            self.hungry += count


class PlayerHand(pygame.sprite.Sprite):
    def __init__(self, player: Player, type_hand: int, image: pygame.Surface, *groups):
        super().__init__(*groups)

        self.player = player
        self.image = image
        self.rect = self.image.get_rect()

        self.main_score = player.main_score

        self.x, self.y = self.player.rect.center
        self.distance = 70
        self.distance_active = 50
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

    def attack(self, offset) -> tuple:
        self.animation_attack()
        m_x, m_y = pygame.mouse.get_pos()[0] + offset.x, pygame.mouse.get_pos()[1] + offset.y
        p_x, p_y = self.player.rect.center
        if self.type_hand:
            k = math.radians(180)
        else:
            k = -math.radians(180)
        a = math.atan2((p_y - m_y), (p_x - m_x)) + k
        return int(p_x + self.distance_active * math.cos(a)), int(p_y + self.distance_active * math.sin(a))

    def animation_attack(self):
        p_x, p_y = self.player.rect.center

        if self.type_hand:
            k = math.radians(162)
        else:
            k = -math.radians(162)

        for i in range(1, 4):
            a = math.atan2((p_y - self.rect.centery), (p_x - self.rect.centerx)) - k
            self.rect.centerx = int(p_x + self.distance * math.cos(a))
            self.rect.centery = int(p_y + self.distance * math.sin(a))

    def update(self) -> None:
        ...
