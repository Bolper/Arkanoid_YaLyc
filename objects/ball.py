import pygame

from objects.blocks.blocks import Block
from objects.enemies.enemies import Enemy
from objects.load_game_image import load_image
from objects.paddle import Paddle
from objects.doh import Doh


class Ball(pygame.sprite.Sprite):
    MAX_SPEED_X = 5
    START_SPEED = 2

    SLOWDOWN_POWERUP_VALUE = 1

    def __init__(self, screen: pygame.surface.Surface, paddle: 'Paddle', enemies: list, game: 'game.Game'):
        super().__init__()
        self.catching = False
        self.is_catched = False
        self.game = game

        self.paddle = paddle
        self.enemies: list[pygame.sprite.Sprite] = enemies

        self.surface = screen

        self.image: pygame.surface.Surface = load_image("ball.png")

        self.rect = self.image.get_rect()

        self.rect.x = self.game.paddle.rect.x + self.game.paddle.rect.width // 2
        self.rect.y = self.surface.get_height() - self.paddle.PADDLE_HEIGHT - self.rect.width - 11

        self.speed_x = self.START_SPEED
        self.speed_y = -self.START_SPEED

    def _configure_speed(self):
        self.speed_x = max(min(self.speed_x, self.MAX_SPEED_X), -self.MAX_SPEED_X)

        if -1 < self.speed_x < 1:
            try:
                self.speed_x = self.speed_x + self.speed_x / abs(self.speed_x)

            except ZeroDivisionError:
                self.speed_x = 1

    def _collide_with_paddle(self, x):
        self.speed_y *= -1
        self.speed_x += (x - (self.paddle.rect.x + self.paddle.PADDLE_WIDTH / 2)) / 15

        self._configure_speed()

        self.rect.y = self.surface.get_height() - self.paddle.PADDLE_HEIGHT - self.rect.width - 11

        if self.catching:
            self.is_catched = True
            self.catching = False
            self.game.stop_balls_catching()

    def _collide_with_block(self, block):
        # Вычисление расстояний между центрами мяча и блока
        ball_center_x = self.rect.centerx
        ball_center_y = self.rect.centery

        # Пределы блока
        block_left = block.rect.left
        block_right = block.rect.right
        block_top = block.rect.top
        block_bottom = block.rect.bottom

        self.rect.move_ip(-self.speed_x, -self.speed_y)

        if ball_center_x > block_right and ball_center_y > block_bottom:
            self.speed_x = abs(self.speed_x)
            self.speed_y = abs(self.speed_y)

        elif ball_center_x > block_right and ball_center_y < block_top:
            self.speed_x = abs(self.speed_x)
            self.speed_y = -abs(self.speed_y)

        elif ball_center_x < block_left and ball_center_y < block_top:
            self.speed_x = -abs(self.speed_x)
            self.speed_y = -abs(self.speed_y)

        elif ball_center_x < block_left and ball_center_y > block_bottom:
            self.speed_x = -abs(self.speed_x)
            self.speed_y = abs(self.speed_y)

        # Отскок по горизонтали
        elif ball_center_x < block_left or ball_center_x > block_right:
            self.speed_x = -self.speed_x

        # Отскок по вертикали
        elif ball_center_y < block_top or ball_center_y > block_bottom:
            self.speed_y = -self.speed_y

    def _handle_collide(self):
        x, y = self.rect.x, self.rect.y

        if self.rect.colliderect(self.paddle.rect):
            self._collide_with_paddle(x)

        if x + self.rect.width >= self.surface.get_width():
            self.rect.move(self.surface.get_width() - self.rect.width, y)
            self.speed_x = -abs(self.speed_x)

        elif x <= 0:
            self.rect.move(1, y)
            self.speed_x = abs(self.speed_x)

        elif y <= 0:
            self.rect.move(x, 1)
            self.speed_y = abs(self.speed_y)

        else:
            for sprite in self.enemies:
                if sprite.rect.colliderect(self.rect):
                    if isinstance(sprite, Block):
                        self._collide_with_block(sprite)
                        if sprite.try_destroy():
                            powerup = sprite.destroy()
                            self.enemies.remove(sprite)
                            return powerup
                    elif isinstance(sprite, Enemy):
                        self._collide_with_block(sprite)

                        if sprite.try_destroy():
                            powerup = sprite.destroy()
                            self.enemies.remove(sprite)
                            return powerup
                    elif isinstance(sprite, Doh):
                        self._collide_with_block(sprite)
                        if sprite.try_destroy():
                            sprite.destroy()
                            self.enemies.remove(sprite)

    def update(self):
        if self.rect.y > self.surface.get_height():
            self.kill()
            self.game.balls.remove(self)

        if self.is_catched:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.is_catched = False

            x, y, speed = self.paddle.rect.x, self.paddle.rect.y, self.paddle.speed

            if keys[pygame.K_LEFT] and x > 0:
                self.rect.move_ip(-speed, 0)

            if keys[pygame.K_RIGHT] and x < self.surface.get_width() - self.paddle.rect.w - speed:
                self.rect.move_ip(speed, 0)

            return

        powerup = self._handle_collide()
        self.rect.move_ip(self.speed_x, self.speed_y)

        return powerup if powerup else None

    def reset(self):
        self.rect.x = self.paddle.rect.x + self.paddle.PADDLE_WIDTH // 2
        self.rect.y = self.surface.get_height() - self.paddle.PADDLE_HEIGHT - self.rect.width - 11

        self.speed_x = self.START_SPEED
        self.speed_y = -self.START_SPEED

    def switch_catching(self):
        self.catching = True

    def stop_catching(self):
        self.catching = False

    def slow(self):
        self.speed_x = (abs(self.speed_x) - 1) * self.speed_x / (abs(self.speed_x))
        self._configure_speed()

    def set_speed(self, speed):
        self.speed_x = speed

    def get_speed(self) -> float | int:
        return self.speed_x
