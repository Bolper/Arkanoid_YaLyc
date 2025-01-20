import pygame


from objects.load_game_image import load_image


class Paddle(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.surface.Surface):
        super().__init__()

        self.image = load_image("paddle.png")

        self.surface = screen

        self.rect = self.image.get_rect()

        self.PADDLE_WIDTH = self.rect.width
        self.PADDLE_HEIGHT = self.rect.height

        self.rect.x = (self.surface.get_width() - self.PADDLE_WIDTH) // 2
        self.rect.y = self.surface.get_height() - self.PADDLE_HEIGHT - 10

        self.speed = 5

    def update(self):
        x, y = self.rect.x, self.rect.y
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and x > 0:
            self.rect.move_ip(-self.speed, 0)

        if keys[pygame.K_RIGHT] and x < self.surface.get_width() - self.PADDLE_WIDTH - self.speed:
            self.rect.move_ip(self.speed, 0)
