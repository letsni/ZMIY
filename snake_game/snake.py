import pygame
from config import CELL_SIZE, GREEN

class Snake:
    def __init__(self, speed):
        # Позиция головы в пикселях
        self.head_pos = [5 * CELL_SIZE, 5 * CELL_SIZE]
        # Длина змейки в клетках
        self.length = 20
        # Список сегментов (позиции в пикселях)
        self.body = [self.head_pos.copy() for _ in range(self.length)]
        # Текущее направление движения (dx, dy) в пикселях за кадр
        self.direction = [speed, 0]
        # Направление, которое игрок хочет установить
        self.next_direction = self.direction.copy()
        self.speed = speed

    def move(self):
        # Поворот только если голова стоит на сетке
        if self.head_pos[0] % CELL_SIZE == 0 and self.head_pos[1] % CELL_SIZE == 0:
            self.direction = self.next_direction.copy()

        # Двигаем голову
        self.head_pos[0] += self.direction[0]
        self.head_pos[1] += self.direction[1]

        # Обновляем тело
        self.body.insert(0, self.head_pos.copy())
        if len(self.body) > self.length:
            self.body.pop()

    def change_direction(self, dx, dy):
        # Разрешаем поворот, если не в противоположную сторону
        new_dir = [dx * self.speed, dy * self.speed]
        if new_dir != [-self.direction[0], -self.direction[1]]:
            self.next_direction = new_dir

    def draw(self, screen):
        for pos in self.body:
            pygame.draw.rect(screen, GREEN, (*pos, CELL_SIZE, CELL_SIZE))