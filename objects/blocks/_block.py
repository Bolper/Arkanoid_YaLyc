import random

import pygame

from objects.load_game_image import load_image
from objects.powerups.powerups import PowerupCatch, PowerupSlow, PowerupLife, PowerupExpand, PowerupLaser, \
    PowerupDuplicate


class Block(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.surface.Surface, color: str, x: float, y: float, hp: int = 0):
        super().__init__()

        self.chance_to_spawn_powerup = 25

        self.image = load_image(
            f'blocks/brick_{color}.png')

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.screen = screen
        self.HP = hp
        self.current_HP = hp

    def destroy(self):
        self.kill()

        if self.chance_to_spawn_powerup >= random.randrange(1, 101):
            powerup_init_data: tuple = self.screen, self.rect.x, self.rect.y
            powerup = random.choice(
                [PowerupCatch, PowerupSlow, PowerupLife, PowerupExpand, PowerupLaser, PowerupDuplicate])(
                *powerup_init_data)

            return powerup

    def try_destroy(self):
        if self.current_HP <= 0:
            return True
        else:
            self.current_HP -= 1
            return False
