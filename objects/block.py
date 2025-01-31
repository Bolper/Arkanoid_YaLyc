import random

import pygame

from objects.load_game_image import load_image
from objects.powerups.powerups import PowerupCatch, PowerupSlow, PowerupLife, PowerupExpand, PowerupLaser, \
    PowerupDuplicate


class Block(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.surface.Surface, color: str, x: float, y: float):
        super().__init__()

        self.chance_to_spawn_powerup = 30

        self.image = load_image(
            f'blocks/brick_{color}.png')

        self.rect: pygame.rect.Rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.screen = screen

    def destroy(self):
        self.kill()

        if self.chance_to_spawn_powerup >= random.randrange(1, 101):
            powerup_init_data: tuple = self.screen, self.rect.x, self.rect.y
            powerup = random.choice(
                [PowerupCatch, PowerupSlow, PowerupLife, PowerupExpand, PowerupLaser, PowerupDuplicate])(
                *powerup_init_data)

            return powerup
