import pygame


from objects.load_game_image import load_image


class Paddle(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.surface.Surface, fps: int):
        super().__init__()

        self.image = load_image("paddle.png")

        self.surface = screen

        self.rect = self.image.get_rect()

        self.PADDLE_WIDTH = self.rect.width
        self.PADDLE_HEIGHT = self.rect.height

        self.rect.x = (self.surface.get_width() - self.PADDLE_WIDTH) // 2
        self.rect.y = self.surface.get_height() - self.PADDLE_HEIGHT - 10

        self.speed = 5

        self.wide_ticks = fps * 15
        self.wide_ticks_cnt = 0

        self.wide_circle = 60
        self.current_wide_cnt = 1
        self.current_wide_img = 1
        self.wide_tag = 0

    def _wide(self):
        if self.wide_tag:
            match self.wide_tag:
                case 1:
                    if self.current_wide_cnt == self.wide_circle:
                        self.current_wide_cnt = 1
                        self.current_wide_img += 1

                    else:
                        self.current_wide_cnt += 1

                    if self.current_wide_img == 10:
                        self.current_wide_img = 9
                        self.wide_tag = 2

                case 2:
                    if self.wide_ticks_cnt < self.wide_ticks:
                        self.wide_ticks_cnt += 1
                    else:
                        self.wide_ticks_cnt = 0
                        self.wide_tag = 3

                case 3:
                    if self.current_wide_cnt == self.wide_circle:
                        self.current_wide_cnt = 1
                        self.current_wide_img -= 1

                    else:
                        self.current_wide_cnt += 1

                    if self.current_wide_img == 1:
                        self.image = load_image("paddle.png")
                        self.current_wide_img = 1
                        self.wide_tag = 0

            x, y = self.rect.x, self.rect.y

            self.image = load_image(f"wide_paddle/paddle_wide_{self.current_wide_img}.png")
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = x, y

    def start_expand(self):
        if not self.wide_tag:
            self.wide_tag = 1

        else:
            self.wide_ticks_cnt = 0


    def update(self):
        self._wide()
        x, y = self.rect.x, self.rect.y
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and x > 0:
            self.rect.move_ip(-self.speed, 0)

        if keys[pygame.K_RIGHT] and x < self.surface.get_width() - self.rect.width - self.speed:
            self.rect.move_ip(self.speed, 0)
