from config import WINDOW_WIDTH, WINDOW_HEIGHT, CELL_SIZE, HUD_HEIGHT

class Level1Map:
    name = "Уровень 1"

    obstacles = []

    cols = WINDOW_WIDTH // CELL_SIZE
    rows = (WINDOW_HEIGHT - HUD_HEIGHT) // CELL_SIZE  # игровое поле без HUD

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
