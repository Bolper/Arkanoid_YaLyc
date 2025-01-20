import pygame


from objects.load_game_image import load_image


class Ball(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.surface.Surface, paddle: 'Paddle', blocks: list['Block']):
        super().__init__()

        self.paddle = paddle
        self.blocks = blocks

        self.surface = screen

        self.image: pygame.surface.Surface = load_image("ball.png")

        self.rect = self.image.get_rect()

        self.rect.x = self.surface.get_width() // 2
        self.rect.y = self.surface.get_height() - self.paddle.PADDLE_HEIGHT - self.rect.width - 11

        self.speed_x = 2
        self.speed_y = -2

    def _handle_collide(self):
        x, y = self.rect.x, self.rect.y

        if self.rect.colliderect(self.paddle.rect):

            self.speed_y *= -1
            self.speed_x += (x - (self.paddle.rect.x + self.paddle.PADDLE_WIDTH / 2)) / 15
            self.speed_x = max(min(self.speed_x, 5), -5)

            if -1 < self.speed_x < 1:
                try:
                    self.speed_x = self.speed_x + self.speed_x / abs(self.speed_x)

                except ZeroDivisionError:
                    self.speed_x = 1

            self.rect.y = self.surface.get_height() - self.paddle.PADDLE_HEIGHT - self.rect.width - 11

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
            for block in self.blocks:
                if block.rect.colliderect(self.rect):

                    if self.rect.colliderect(block.rect):
                        # Вычисление расстояний между центрами мяча и блока
                        ball_center_x = self.rect.centerx
                        ball_center_y = self.rect.centery
                        block_center_x = block.rect.centerx
                        block_center_y = block.rect.centery

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

                    block.kill()
                    self.blocks.remove(block)

    def update(self):
        self._handle_collide()
        self.rect.move_ip(self.speed_x, self.speed_y)

        return self

    def reset(self):
        self.rect.x = self.paddle.rect.x + self.paddle.PADDLE_WIDTH // 2
        self.rect.y = self.surface.get_height() - self.paddle.PADDLE_HEIGHT - self.rect.width - 11

        self.speed_x = 2
        self.speed_y = -2
