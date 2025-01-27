import pygame

from objects.load_game_image import load_image


class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image('laser_bullet.png')
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.speed = 1

    def update(self):
        self.rect.move_ip(0, -self.speed)

        if self.rect.y < 0:
            self.kill()
