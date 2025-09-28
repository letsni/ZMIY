import pygame
import random
from config import CELL_SIZE, RED, WINDOW_WIDTH, WINDOW_HEIGHT
from config import HUD_HEIGHT


class Food:
    def __init__(self, snake, level_map=None):
        self.level_map = level_map
        self.position = self.random_position(snake)

    def random_position(self, snake):
        """Случайная клетка, не занятая змейкой и не на препятствиях"""
        cols = WINDOW_WIDTH // CELL_SIZE
        rows = (WINDOW_HEIGHT - HUD_HEIGHT)  // CELL_SIZE

        # Преобразуем тело змейки в координаты клеток
        snake_cells = {(p[0] // CELL_SIZE, p[1] // CELL_SIZE) for p in snake.body}

        # Преобразуем препятствия карты в координаты клеток
        obstacle_cells = set()
        if self.level_map:
            obstacle_cells = {tuple(obs) for obs in self.level_map.get_obstacles()}

        while True:
            x_cell = random.randint(0, cols - 1)
            y_cell = random.randint(0, rows - 1)
            if (x_cell, y_cell) not in snake_cells and (x_cell, y_cell) not in obstacle_cells:
                return [x_cell * CELL_SIZE, y_cell * CELL_SIZE]

    def draw(self, screen):
        pygame.draw.rect(screen, RED, (*self.position, CELL_SIZE, CELL_SIZE))

    def check_collision(self, snake):
        """Проверка: змейка съела еду (по клетке)"""
        head_cell = (snake.head_pos[0] // CELL_SIZE, snake.head_pos[1] // CELL_SIZE)
        food_cell = (self.position[0] // CELL_SIZE, self.position[1] // CELL_SIZE)
        return head_cell == food_cell