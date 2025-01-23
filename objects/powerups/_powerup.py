import pygame

from objects.load_game_image import load_image


class Powerup(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.surface.Surface, x: int | float, y: int | float, name: str) -> None:
        super().__init__()
        self.screen = screen

        self.current_img = 1

        self.image = load_image(fr"powerups/{name}/{name}_1.png")

        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.speed = 1

        self.circle = 6
        self.current_circle = 0


    def update_img(self):
        if self.current_circle == self.circle:
            self.current_img = self.current_img + 1 if self.current_img < 8 else 1
            self.current_circle = 0

        else:
            self.current_circle += 1

        self.image = load_image(f"powerups/powerup_catch/powerup_catch_{self.current_img}.png")

    def update(self):
        self.update_img()
        self.rect.y += self.speed

        if self.rect.y >= self.screen.get_height():
            self.kill()