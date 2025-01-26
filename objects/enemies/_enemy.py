import random

import pygame

from objects.load_game_image import load_image
from objects.powerups.powerups import PowerupCatch


class Enemy(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.surface.Surface, x: float, y: float, name: str, speed_x: float = 2,
                 speed_y: float = 0):
        super().__init__()
        self.chance_to_spawn_powerup = 20
        self.current_img = 1
        self.image = load_image(
            f'enemies/enemy_{name}/enemy_{name}_1.png')

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.screen = screen
        self.name = name
        self.circle = 6
        self.current_circle = 0

    def destroy(self):
        if self.chance_to_spawn_powerup >= random.randrange(1, 101):
            powerup = PowerupCatch(self.screen, self.rect.x, self.rect.y)
            self.kill()
            return powerup

        self.kill()

    def update(self):
        self.update_img()
        self.rect.move_ip(self.speed_x, self.speed_y)
        if self.rect.x + self.rect.width >= self.screen.get_width():
            self.rect.move(self.screen.get_width() - self.rect.width, self.rect.y)
            self.speed_x = -abs(self.speed_x)
        elif self.rect.x < 0:
            self.rect.move(1, self.rect.y)
            self.speed_x = abs(self.speed_x)
        elif self.rect.y <= 0:
            self.rect.move(self.speed_x, 1)
            self.speed_y = abs(self.speed_y)
        elif self.rect.y >= self.screen.get_height() - self.rect.height:
            self.rect.move(self.speed_y, 1)
            self.speed_y = -abs(self.speed_y)

    def update_img(self):
        if self.current_circle == self.circle:
            self.current_circle = 0
            self.current_img = self.current_img + 1 if self.current_img < 25 else 1
            self.image = load_image(f"enemies/enemy_{self.name}/enemy_{self.name}_{self.current_img}.png")
        else:
            self.current_circle += 1
