import pygame


from objects.load_game_image import load_image


class Block(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.surface.Surface, color: str, x: float, y: float):
        super().__init__()

        self.image = load_image(
            f'blocks/brick_{color}.png')

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.screen = screen

    def destroy(self):
        ...
