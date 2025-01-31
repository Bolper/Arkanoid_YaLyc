import pygame

from objects.powerups._powerup import Powerup


class PowerupCatch(Powerup):
    def __init__(self, screen: pygame.surface.Surface, x: int | float, y: int | float):
        super().__init__(screen, x, y, "powerup_catch")

    def apply(self, game: 'game.Game') -> None:
        for ball in game.balls:
            ball.switch_catching()


class PowerupSlow(Powerup):
    def __init__(self, screen: pygame.surface.Surface, x: int | float, y: int | float):
        super().__init__(screen, x, y, "powerup_slow")

    def apply(self, game: 'game.Game') -> None:
        game.stop_balls_catching()
        for ball in game.balls:
            ball.slow()


class PowerupLife(Powerup):
    def __init__(self, screen: pygame.surface.Surface, x: int | float, y: int | float):
        super().__init__(screen, x, y, "powerup_life")

    def apply(self, game: 'game.Game') -> None:
        game.stop_balls_catching()
        game.lives += 1


class PowerupExpand(Powerup):
    def __init__(self, screen: pygame.surface.Surface, x: int | float, y: int | float):
        super().__init__(screen, x, y, "powerup_expand")

    def apply(self, game: 'game.Game') -> None:
        game.stop_balls_catching()
        game.paddle.start_expand()


class PowerupLaser(Powerup):
    def __init__(self, screen: pygame.surface.Surface, x: int | float, y: int | float):
        super().__init__(screen, x, y, "powerup_laser")

    def apply(self, game: 'game.Game') -> None:
        game.stop_balls_catching()
        game.paddle.start_laser()


class PowerupDuplicate(Powerup):
    def __init__(self, screen: pygame.surface.Surface, x: int | float, y: int | float):
        super().__init__(screen, x, y, "powerup_duplicate")

    def apply(self, game: 'game.Game') -> None:
        game.stop_balls_catching()
        game.spawn_extra_ball()
