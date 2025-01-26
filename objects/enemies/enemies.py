import pygame
from objects.enemies._enemy import Enemy


class EnemyPyramid(Enemy):
    def __init__(self, screen: pygame.surface.Surface, x: float, y: float, speed_x: float = 2,
                 speed_y: float = 0):
        super().__init__(screen, x, y, "pyramid")

