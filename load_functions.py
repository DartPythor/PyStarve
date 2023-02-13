import pygame
import os


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
