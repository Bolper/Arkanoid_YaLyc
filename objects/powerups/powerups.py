import pygame

from objects.powerups._powerup import Powerup


class PowerupCatch(Powerup):
    def __init__(self, screen: pygame.surface.Surface, x: int | float, y: int | float):
        super().__init__(screen, x, y, "powerup_catch")