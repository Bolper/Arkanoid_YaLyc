import sys
from random import choice

from objects.ball import Ball
from objects.blocks.blocks import Block
from objects.blocks.block_factory import BlockFactory
from objects.enemies.enemies import Enemy
from objects.enemies.enemy_factory import EnemyFactory
from objects.doh import Doh
from objects.laser import Laser
from objects.paddle import Paddle
from objects.doh_bullet import DohBullet
import pygame

import sqlite3

from objects.powerups.powerups import Powerup


class Game:
    BACKGROUND = pygame.Color('black')

    def __init__(self, screen: pygame.surface.Surface, level: str, fps: int = 120, lives: int = 3):
        self.FPS: int = fps
        self.screen = screen
        self.lives: int = lives
        self.total_score: int = 0
        self.game_over_flag: bool = False
        self._is_paddle_catching: bool = False

        self.win: bool = False

        self._enemies: list = []
        self._get_enemies(screen, f"levels/{level}")

        self.paddle = Paddle(screen, self.FPS)
        self.balls: list[Ball] = [Ball(screen, self.paddle, self._enemies, self)]

        self.all_sprites = pygame.sprite.Group()
        self.lasers: list[Laser] = []
        self.doh_bullets: list[DohBullet] = []

        for sprite in (*self.balls, self.paddle, *self._enemies):
            self.all_sprites.add(sprite)

    def get_total_score(self) -> int:
        return self.total_score

    def _get_enemies(self, screen: pygame.surface.Surface, db_name: str) -> None:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        query = """SELECT * FROM enemies"""
        blocks_data = cursor.execute(query).fetchall()

        for t, color, x, y in blocks_data:
            if t == "enemy":
                self._enemies.append(EnemyFactory.create(color, screen, x, y))

            elif t == "block":
                self._enemies.append(BlockFactory.create(color, screen, x, y))
            elif t == "boss":
                self._enemies.append(Doh(screen, x, y))

        cursor.close()

    def _handle_collide_with_powerups(self) -> None:
        for sprite in self.all_sprites:
            if self.paddle.rect.colliderect(sprite.rect) and isinstance(sprite, Powerup):
                sprite.apply(self)

                sprite.kill()
                self.all_sprites.remove(sprite)

    def _handle_collide_with_lasers(self) -> None:
        for laser in self.lasers:
            for sprite in self._enemies:
                if laser.rect.colliderect(sprite.rect):
                    if isinstance(sprite, Block):
                        powerup = sprite.destroy()
                        self._enemies.remove(sprite)

                        if powerup:
                            self.all_sprites.add(powerup)

                    elif isinstance(sprite, Enemy):
                        if sprite.try_destroy():
                            sprite.destroy()
                            self._enemies.remove(sprite)

                    laser.kill()

    def _collide_with_doh_bullet(self) -> None:
        for bullet in self.doh_bullets:
            if bullet.rect.colliderect(self.paddle.rect):
                self.paddle.destroy()
                bullet.kill()

    def _reset_ball(self) -> None:
        ball = Ball(self.screen, self.paddle, self._enemies, self)

        self.balls.append(ball)
        self.all_sprites.add(ball)

        ball.reset()

    def _update_game(self) -> None:
        self._handle_collide_with_powerups()
        self._handle_collide_with_lasers()
        self._collide_with_doh_bullet()
        self.screen.fill(self.BACKGROUND)
        self.all_sprites.draw(self.screen)

        for sprite in self.all_sprites:
            new_sprite: pygame.sprite.Sprite | None | tuple = sprite.update()

            if new_sprite:
                self.all_sprites.add(new_sprite)
                if isinstance(new_sprite, DohBullet):
                    self.doh_bullets.append(new_sprite)

            if type(new_sprite) is tuple:
                for entity in new_sprite:
                    if isinstance(entity, Laser):
                        self.lasers.append(entity)

        if not self._enemies:
            self.win = True
            self.game_over_flag = True

        if self.paddle.is_destroyed():
            self.game_over_flag = True

        if not self.balls:
            self.lives -= 1

            if not self.lives:
                self.game_over_flag = True

            else:
                self._reset_ball()

    def spawn_extra_ball(self):
        ball = Ball(self.screen, self.paddle, self._enemies, self)
        ball.set_speed(self.balls[0].get_speed() * choice([1, -1]))

        self.balls.append(ball)
        self.all_sprites.add(ball)

    def stop_balls_catching(self) -> None:
        for ball in self.balls:
            ball.stop_catching()

    def start_ball_catching(self) -> None:
        self._is_paddle_catching = True

    def run(self) -> None:
        clock = pygame.time.Clock()

        stop_flag = False

        while not stop_flag:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()

            if not self.game_over_flag:
                self._update_game()

            else:
                self.screen.fill(self.BACKGROUND)
                return None

            pygame.display.flip()
            clock.tick(self.FPS)

    @property
    def is_win(self) -> bool:
        return self.win

    @staticmethod
    def terminate():
        pygame.quit()
        sys.exit()
