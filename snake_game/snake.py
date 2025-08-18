import math
import pygame
from config import CELL_SIZE, GREEN

class Snake:
    def __init__(self, speed):
        self.speed = speed  # пикселей за кадр
        self.head_pos = [5 * CELL_SIZE, 5 * CELL_SIZE]

        self.length = 5
        self.body = [[self.head_pos[0] - (i+1) * CELL_SIZE, self.head_pos[1]] for i in range(self.length)]

        self.direction = [speed, 0]
        self.next_direction = self.direction.copy()

        # история пути головы в пикселях
        self.path = [self.head_pos.copy()]

    def change_direction(self, dx, dy):
        new_dir = [dx * self.speed, dy * self.speed]
        # запрет на разворот на 180
        if new_dir != [-self.direction[0], -self.direction[1]]:
            self.next_direction = new_dir

    def move(self):
        # Двигаем голову
        self.head_pos[0] += self.direction[0]
        self.head_pos[1] += self.direction[1]

        # Меняем направление только на сетке
        if self.head_pos[0] % CELL_SIZE == 0 and self.head_pos[1] % CELL_SIZE == 0:
            self.direction = self.next_direction.copy()

        # Добавляем текущую позицию в путь
        self.path.insert(0, self.head_pos.copy())

        # Ограничиваем длину пути
        max_distance = (self.length + 1) * CELL_SIZE * 2
        self._trim_path(max_distance)

        # Если длину увеличили, расширяем body
        while len(self.body) < self.length:
            self.body.append(self.body[-1].copy())

        # Обновляем сегменты тела по расстоянию
        for i in range(self.length):
            dist = (i + 1) * CELL_SIZE
            pos = self._sample_path_by_distance(dist)
            self.body[i][0], self.body[i][1] = pos[0], pos[1]

    def _trim_path(self, max_distance):
        """Обрезаем путь, чтобы хранить только нужное количество точек"""
        accumulated = 0
        new_path = [self.path[0]]
        for i in range(len(self.path)-1):
            p0 = self.path[i]
            p1 = self.path[i+1]
            segment_len = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
            accumulated += segment_len
            new_path.append(p1)
            if accumulated > max_distance:
                break
        self.path = new_path

    def _sample_path_by_distance(self, dist):
        """Возвращает точку на пути на 'dist' пикселей назад от головы"""
        accumulated = 0
        for i in range(len(self.path) - 1):
            p0 = self.path[i]
            p1 = self.path[i + 1]
            segment_len = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
            if accumulated + segment_len >= dist:
                t = (dist - accumulated) / segment_len
                return [p0[0] + (p1[0] - p0[0]) * t,
                        p0[1] + (p1[1] - p0[1]) * t]
            accumulated += segment_len
        return self.path[-1].copy()

    def draw(self, screen):
        # тело
        for pos in self.body:
            x, y = int(pos[0]), int(pos[1])
            pygame.draw.rect(screen, GREEN, (x, y, CELL_SIZE, CELL_SIZE))
        # голова
        hx, hy = int(self.head_pos[0]), int(self.head_pos[1])
        pygame.draw.rect(screen, GREEN, (hx, hy, CELL_SIZE, CELL_SIZE))

    def get_head_cell(self):
        return (self.head_pos[0] // CELL_SIZE, self.head_pos[1] // CELL_SIZE)

    def check_food_collision(self, food):
        hx, hy = self.get_head_cell()
        fx, fy = food.position[0] // CELL_SIZE, food.position[1] // CELL_SIZE
        return hx == fx and hy == fy

    def grow(self, cells=1):
        self.length += cells