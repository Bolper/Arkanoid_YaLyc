import pygame
from objects.enemies._enemy import Enemy


class EnemyPyramid(Enemy):
    def __init__(self, screen: pygame.surface.Surface, x: float, y: float, speed_x: float = 2,
                 speed_y: float = 0):
        super().__init__(screen, x, y, "pyramid", speed_x, speed_y)


class EnemyCone(Enemy):
    def __init__(self, screen: pygame.surface.Surface, x: float, y: float, speed_x: float = 1,
                 speed_y: float = 0):
        super().__init__(screen, x, y, "cone", speed_x, speed_y)


class EnemyCube(Enemy):
    def __init__(self, screen: pygame.surface.Surface, x: float, y: float, speed_x: float = 3,
                 speed_y: float = 0):
        super().__init__(screen, x, y, "cube", speed_x, speed_y)


class EnemyMolecule(Enemy):
    def __init__(self, screen: pygame.surface.Surface, x: float, y: float, speed_x: float = 3,
                 speed_y: float = 2):
        super().__init__(screen, x, y, "molecule", speed_x, speed_y)
