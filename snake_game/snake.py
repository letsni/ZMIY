import pygame
from config import CELL_SIZE, GREEN


class Snake:
    def __init__(self, speed, initial_length=5):
        self.speed = speed
        self.head_pos = [5 * CELL_SIZE, 5 * CELL_SIZE]
        self.direction = [speed, 0]
        self.next_direction = self.direction.copy()

        self.length = initial_length
        self.body = [self.head_pos.copy() for _ in range(self.length)]
        self.path = [self.head_pos.copy()]
        self.segment_distance = CELL_SIZE / self.speed

        # Список клеток, где произошли повороты
        self.turn_cells = []

    def change_direction(self, dx, dy):
        new_dir = [dx * self.speed, dy * self.speed]
        if new_dir != [-self.direction[0], -self.direction[1]]:
            self.next_direction = new_dir

    def move(self):
        # Двигаем голову плавно
        self.head_pos[0] += self.direction[0]
        self.head_pos[1] += self.direction[1]

        # Поворот на сетке
        if self.head_pos[0] % CELL_SIZE == 0 and self.head_pos[1] % CELL_SIZE == 0:
            cell = (self.head_pos[0], self.head_pos[1])
            if cell not in self.turn_cells:
                self.turn_cells.append(cell)
            self.direction = self.next_direction.copy()

        # Добавляем в путь
        self.path.insert(0, self.head_pos.copy())
        max_path_length = int(self.length * self.segment_distance) + 10
        if len(self.path) > max_path_length:
            self.path.pop()

        # Убедимся, что body достаточно длинное
        while len(self.body) < self.length:
            self.body.append(self.body[-1].copy())

        # Обновляем тело
        for i in range(self.length):
            index = int(i * self.segment_distance)
            if index < len(self.path):
                self.body[i] = self.path[index].copy()

        # Убираем клетки поворота, через которые уже прошел хвост
        tail_pos = self.body[-1]
        self.turn_cells = [c for c in self.turn_cells if (abs(c[0] - tail_pos[0]) > 1 or abs(c[1] - tail_pos[1]) > 1)]

    def grow(self, cells=1):
        self.length += cells

    def draw(self, screen):
        # Рисуем тело плавно
        for pos in self.body:
            pygame.draw.rect(screen, GREEN, (*pos, CELL_SIZE, CELL_SIZE))
        # Голова
        pygame.draw.rect(screen, GREEN, (*self.head_pos, CELL_SIZE, CELL_SIZE))
        # Рисуем поворотные клетки
        for cell in self.turn_cells:
            pygame.draw.rect(screen, GREEN, (cell[0], cell[1], CELL_SIZE, CELL_SIZE))