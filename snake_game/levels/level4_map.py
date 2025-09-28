from config import WINDOW_WIDTH, WINDOW_HEIGHT, CELL_SIZE, HUD_HEIGHT
import random

NUM_OBSTACLES = 26
class Level4Map:
    name = "Случайные препятствия"

    obstacles = []
    cols = WINDOW_WIDTH // CELL_SIZE
    rows = (WINDOW_HEIGHT - HUD_HEIGHT) // CELL_SIZE
    # генерируем препятствия
    used = set()
    while len(obstacles) < NUM_OBSTACLES:
        x = random.randint(1, cols - 2)  # не у самых краёв
        y = random.randint(1, rows - 2)  # не у самых краёв
        if (x, y) not in used:
            if not (y==5 and x<20):
                obstacles.append([x, y])
                used.add((x, y))



      # игровое поле без HUD

    # верхняя и нижняя границы
    for x in range(cols):
        obstacles.append([x, 0])           # верхняя граница поля (с учётом HUD в Game.py)
        obstacles.append([x, rows - 1])    # нижняя граница

    # левая и правая границы
    for y in range(rows):
        obstacles.append([0, y])           # левая граница
        obstacles.append([cols - 1, y])    # правая граница

    @classmethod
    def get_obstacles(cls):
        return cls.obstacles