import pygame
import math
import os


def rotate(array_pos1: tuple, array_pos2: tuple) -> int:
    mouse_x, mouse_y = array_pos1
    rel_x, rel_y = mouse_x - array_pos2[0], mouse_y - array_pos2[1]
    angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
    return int(angle)


def load_level(filename) -> list:
    """Function for get map level in str formate"""
    filename = os.path.join("data", "map", filename)

    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))

    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def load_image(dir_: str, name: str, colorkey=None) -> pygame.Surface:
    """Function for get Surface image"""

    fullname = os.path.join("data", "image", dir_, name)

    if not os.path.isfile(fullname):
        raise FileNotFoundError(f"File {fullname} not found")

    image = pygame.image.load(fullname)

    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image.convert_alpha()

    return image
