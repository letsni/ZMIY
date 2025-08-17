import pygame
import random
from config import CELL_SIZE, RED, WINDOW_WIDTH, WINDOW_HEIGHT

class Food:
    def __init__(self, snake):
        self.position = self.random_position(snake)

    def random_position(self, snake):
        """Случайная клетка, не занятая змейкой"""
        cols = WINDOW_WIDTH // CELL_SIZE
        rows = WINDOW_HEIGHT // CELL_SIZE

        while True:
            x = random.randint(0, cols - 1) * CELL_SIZE
            y = random.randint(0, rows - 1) * CELL_SIZE
            if [x, y] not in snake.body:  # не совпадает с телом змейки
                return [x, y]

    def draw(self, screen):
        pygame.draw.rect(screen, RED, (*self.position, CELL_SIZE, CELL_SIZE))