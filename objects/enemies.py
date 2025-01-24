import random

import pygame


from objects.load_game_image import load_image
from objects.powerups.powerups import PowerupCatch


class Enemy(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.surface.Surface, x: float, y: float):
        super().__init__()

        self.chance_to_spawn_powerup = 20

        self.image = load_image(
            f'enemies/enemy/enemy_1.png')

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = 3
        self.speed_y = 0
        self.screen = screen

    def destroy(self):
        if self.chance_to_spawn_powerup >= random.randrange(1, 101):
            powerup = PowerupCatch(self.screen, self.rect.x, self.rect.y)
            self.kill()
            return powerup

        self.kill()

    def update(self):
        self.rect.move_ip(self.speed_x, self.speed_y)
        if self.rect.x + self.rect.width >= self.screen.get_width():
            self.rect.move(self.screen.get_width() - self.rect.width, self.rect.y)
            self.speed_x = -abs(self.speed_x)
        elif self.rect.x < 0:
            self.rect.move(1, self.rect.y)
            self.speed_x = abs(self.speed_x)
