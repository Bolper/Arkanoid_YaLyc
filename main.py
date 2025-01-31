import sys

import pygame
from gif_pygame import gif_pygame
import os

from game import Game

SIZE = WIDTH, HEIGHT = 500, 500
FPS = 120
pygame.init()
BACKGROUND = pygame.Color('black')
COLOR = pygame.Color('white')


def terminate() -> None:
    pygame.quit()
    sys.exit()


def get_levels() -> list[str]:
    levels_dir: str = 'levels'
    levels_list = [name for name in os.listdir(levels_dir)]
    return levels_list


def draw_start_screen(screen: pygame.surface.Surface) -> None:
    example_gif = gif_pygame.load("app_data/screens/start_screen.gif")  # Загружает файл .gif

    while True:
        screen.fill((0, 0, 0))
        example_gif.render(screen, (256 - example_gif.get_width() * 0.5, 256 - example_gif.get_height() * 0.5))
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                return None

            if event.type == pygame.QUIT:
                terminate()

        pygame.display.update()


def draw_game_over_screen(screen: pygame.surface.Surface, game: "Game") -> None:
    while True:
        font = pygame.font.Font(None, 36)

        screen.fill(BACKGROUND)
        end_text = font.render("Game Over!", True, COLOR)
        end_rect = end_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(end_text, end_rect)
        score_text = font.render(f"Final Score: {game.get_total_score()}", True, COLOR)
        score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        screen.blit(score_text, score_rect)

        restart_text = font.render("Press R to continue", True, COLOR)
        restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
        screen.blit(restart_text, restart_rect)

        for event in pygame.event.get():
            keys = pygame.key.get_pressed()

            if event.type == pygame.QUIT:
                terminate()
            if keys[pygame.K_r]:
                return None

        pygame.display.flip()


def main():
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption('')

    levels = get_levels()

    while True:
        draw_start_screen(screen)
        for level in levels:
            game = Game(screen, level, FPS)
            game.run()
            draw_game_over_screen(screen, game)

            if not game.is_win:
                break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return


if __name__ == '__main__':
    main()
    pygame.quit()
