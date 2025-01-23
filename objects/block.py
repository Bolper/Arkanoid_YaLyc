import random

import pygame


from objects.load_game_image import load_image
from objects.powerups.powerups import PowerupCatch


class Block(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.surface.Surface, color: str, x: float, y: float):
        super().__init__()

        self.chance_to_spawn_powerup = 20

        self.image = load_image(
            f'blocks/brick_{color}.png')

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.screen = screen

    def destroy(self):
        if self.chance_to_spawn_powerup >= random.randrange(1, 101):
            powerup = PowerupCatch(self.screen, self.rect.x, self.rect.y)
            self.kill()
            return powerup

        self.kill()
