import pygame
from pygame import rect

from objects.laser import Laser
from objects.load_game_image import load_image


class Paddle(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.surface.Surface, fps: int):
        super().__init__()

        self.image = load_image("paddle.png")
        self.fps = fps

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

        self.laser_ticks_cnt = 0

        self.laser_interval = 2
        self.max_lasers = 3
        self.laser_ticks = fps * self.laser_interval * self.max_lasers

        self.laser_circle = 60
        self.current_laser_cnt = 1
        self.current_laser_img = 1
        self.laser_tag = 0

        self.default_transform_cnt = 1
        self.default_transform_circle = 60

    def _transform_to_default(self, name: str) -> bool:
        if self.default_transform_cnt == self.default_transform_circle:
            self.default_transform_cnt = 1
            exec(f"{name} -= 1")

        else:
            self.default_transform_cnt += 1

        if eval(f"{name} == 1"):
            self.image = load_image("paddle.png")
            exec(f"{name} = 1")
            tag_name = f"self.{name.split('_')[1]}_tag"
            exec(f"{tag_name} = 0")
            return True

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
                    if self._transform_to_default("self.current_wide_img"):
                        return None

            x, y = self.rect.x, self.rect.y

            self.image = load_image(f"wide_paddle/paddle_wide_{self.current_wide_img}.png")
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = x, y

    def _laser(self) -> bool:
        if self.laser_tag:
            match self.laser_tag:
                case 1:
                    if self.current_laser_cnt == self.laser_circle:
                        self.current_laser_cnt = 1
                        self.current_laser_img += 1

                    else:
                        self.current_laser_cnt += 1

                    if self.current_laser_img == 17:
                        self.current_laser_img = 16
                        self.laser_tag = 2

                case 2:
                    if not self.laser_ticks_cnt % (self.fps * self.laser_interval):
                        self.laser_ticks_cnt += 1
                        return True

                    if self.laser_ticks_cnt < self.laser_ticks:
                        self.laser_ticks_cnt += 1
                    else:
                        self.laser_ticks_cnt = 0
                        self.laser_tag = 3

                    return False

                case 3:
                    self._transform_to_default("self.current_laser_img")

            x, y = self.rect.x, self.rect.y

            self.image = load_image(f"laser_paddle/paddle_laser_{self.current_laser_img}.png")
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = x, y

            return False

    def start_expand(self) -> None:
        if not self.wide_tag and not self.laser_tag:
            self.wide_tag = 1

        else:
            self.wide_ticks_cnt = 0

    def start_laser(self) -> None:
        if not self.laser_tag and not self.wide_tag:
            self.laser_tag = 1

        else:
            self.laser_ticks_cnt = 0

    def update(self) -> tuple[Laser, Laser] | None:
        self._wide()
        laser = self._laser()
        x, y = self.rect.x, self.rect.y
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and x > 0:
            self.rect.move_ip(-self.speed, 0)

        if keys[pygame.K_RIGHT] and x < self.surface.get_width() - self.rect.width - self.speed:
            self.rect.move_ip(self.speed, 0)

        if laser:
            return Laser(self.rect.x, self.rect.y), Laser(self.rect.x + self.rect.w, self.rect.y)
