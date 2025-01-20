import os
import sys

import pygame

pygame.init()


def load_image(name: str, colorkey=None):
    fullname = os.path.join('objects/game_objects_data', name)

    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        sys.exit()

    image = pygame.image.load(fullname)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()

    return image
