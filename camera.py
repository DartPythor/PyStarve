import pygame


class Camera(pygame.sprite.Group):
    def __init__(self, width_map: int, height_map: int):
        super().__init__()

        self.width_map = width_map
        self.height_map = height_map

        self.display_surface = pygame.display.get_surface()

        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2

        self.offset = pygame.math.Vector2()

    def custom_draw(self, obj: pygame.sprite.Sprite):

        if obj.rect.centerx + self.half_width <= self.width_map and obj.rect.centerx - self.half_width >= 0:
            self.offset.x = obj.rect.centerx - self.half_width

        if obj.rect.centery - self.half_height >= 0 and obj.rect.centery + self.half_height <= self.height_map:
            self.offset.y = obj.rect.centery - self.half_height

        self.display_surface.fill((1, 50, 32))

        for sprite in sorted(self.sprites()):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
