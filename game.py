import sys

from objects.ball import Ball
from objects.block import Block
from objects.enemies._enemy import Enemy
from objects.laser import Laser
from objects.paddle import Paddle
from objects.enemies.enemies import EnemyPyramid, EnemyCone, EnemyCube, EnemyMolecule
import pygame

import sqlite3

from objects.powerups._powerup import Powerup
from objects.powerups.powerups import PowerupCatch, PowerupSlow, PowerupLife, PowerupExpand, PowerupLaser


class Game:
    BACKGROUND = pygame.Color('black')

    def __init__(self, screen: pygame.surface.Surface, level: str, fps: int = 120, lives: int = 3):
        self.FPS: int = fps
        self.screen = screen
        self.lives: int = lives
        self.total_score: int = 0
        self.game_over_flag: bool = False

        self.win: bool = False

        self._enemies: list = []
        self._get_enemies(screen, f"levels/{level}")

        self.paddle = Paddle(screen, self.FPS)
        self.ball = Ball(screen, self.paddle, self._enemies)

        self.all_sprites = pygame.sprite.Group()
        self.lasers: list[Laser] = []

        for sprite in (self.ball, self.paddle, *self._enemies):
            self.all_sprites.add(sprite)

    def get_total_score(self) -> int:
        return self.total_score

    def _get_enemies(self, screen: pygame.surface.Surface, db_name: str):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        query = """SELECT * FROM blocks"""
        blocks_data = cursor.execute(query).fetchall()

        for t, color, x, y in blocks_data:
            if t == "enemy":
                if color == "pyramid":
                    self._enemies.append(EnemyPyramid(screen, x, y))
                elif color == "cone":
                    self._enemies.append(EnemyCone(screen, x, y))
                elif color == "molecule":
                    self._enemies.append(EnemyMolecule(screen, x, y))
                elif color == "cube":
                    self._enemies.append(EnemyCube(screen, x, y))
            elif t == "block":
                self._enemies.append(Block(screen, color, x, y))

        cursor.close()

    def _handle_collide_with_powerups(self):
        for sprite in self.all_sprites:
            if self.paddle.rect.colliderect(sprite.rect) and isinstance(sprite, Powerup):
                if isinstance(sprite, PowerupCatch):
                    self.ball.switch_catching()
                    self.all_sprites.remove(sprite)

                if isinstance(sprite, PowerupSlow):
                    self.ball.stop_catching()
                    self.ball.slow()

                if isinstance(sprite, PowerupLife):
                    self.ball.stop_catching()
                    self.lives += 1

                if isinstance(sprite, PowerupExpand):
                    self.ball.stop_catching()
                    self.paddle.start_expand()

                if isinstance(sprite, PowerupLaser):
                    self.ball.stop_catching()
                    self.paddle.start_laser()

                sprite.kill()

    def _handle_collide_with_lasers(self):
        for laser in self.lasers:
            for sprite in self._enemies:
                if laser.rect.colliderect(sprite.rect):
                    if isinstance(sprite, Block):
                        sprite.destroy()
                        self._enemies.remove(sprite)

                    elif isinstance(sprite, Enemy):
                        if sprite.tryDestroy():
                            sprite.destroy()
                            self._enemies.remove(sprite)

                    laser.kill()


    def _update_game(self) -> None:
        self._handle_collide_with_powerups()
        self._handle_collide_with_lasers()

        self.screen.fill(self.BACKGROUND)
        self.all_sprites.draw(self.screen)

        for sprite in self.all_sprites:
            new_sprite: pygame.sprite.Sprite | None | tuple = sprite.update()

            if new_sprite:
                self.all_sprites.add(new_sprite)

            if type(new_sprite) is tuple:
                for laser in new_sprite:
                    self.lasers.append(laser)

        if not self._enemies:
            self.win = True
            self.game_over_flag = True

        if self.ball.rect.y >= self.screen.get_height():
            self.lives -= 1

            if not self.lives:
                self.game_over_flag = True

            else:
                self.ball.reset()

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
