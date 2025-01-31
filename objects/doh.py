import random

import pygame

from objects.load_game_image import load_image
from objects.doh_bullet import DohBullet


class Doh(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.surface.Surface, x: float, y: float, hp: int = 10):
        super().__init__()
        self.chance_to_spawn_powerup = 20
        self.current_img = 1
        self.image = load_image(f'doh.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.screen = screen
        self.HP = hp
        self.current_HP = self.HP
        self.circle = 240
        self.current_circle = 0

    def destroy(self):
        self.kill()

    def try_destroy(self):
        if self.current_HP <= 0:
            return True
        else:
            self.current_HP -= 1
            return False

    def update(self):
        if self.current_circle == self.circle:
            self.current_circle = 0
            return DohBullet(self.screen, 75, 20, random.randint(-2, 2), random.randint(1, 2))
        else:
            self.current_circle += 1
