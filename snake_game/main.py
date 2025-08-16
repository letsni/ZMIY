import pygame
import sys
from config import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, BLACK, CELL_SIZE, GREEN
from snake import Snake

def main():
    pygame.init()
    pygame.display.set_caption("Snake Game")

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()

    # Скорость змейки в пикселях за кадр
    snake_speed = 4
    snake = Snake(snake_speed)

    running = True
    while running:
        # --- Обработка событий ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction(0, -1)
                elif event.key == pygame.K_DOWN:
                    snake.change_direction(0, 1)
                elif event.key == pygame.K_LEFT:
                    snake.change_direction(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction(1, 0)

        # --- Логика ---
        snake.move()

        # --- Отрисовка ---
        screen.fill(BLACK)
        snake.draw(screen)
        pygame.display.flip()

        # --- Ограничение FPS ---
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()