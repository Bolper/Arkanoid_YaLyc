import pygame

from objects.load_game_image import load_image
import game


class DohBullet(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.surface.Surface, x: float, y: float, speed_x: float = 0,
                 speed_y: float = 1):
        super().__init__()
        self.image = load_image(f'doh_bullet.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.screen = screen
        self.destroyed = False

    def update(self):
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
            self.destroyed = True
            self.kill()

    def is_destroyed(self) -> bool:
        return self.destroyed
