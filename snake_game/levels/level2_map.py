from config import WINDOW_WIDTH, WINDOW_HEIGHT, CELL_SIZE, HUD_HEIGHT

class Level2Map:
    name = "Мелкий шум"
    obstacles = [[2,2],[10,4],[18,18],[20,15],[2,8],[3,20],[30,21],[35,5],[25,15],[16, 6],[20,4],]

    cols = WINDOW_WIDTH // CELL_SIZE
    rows = (WINDOW_HEIGHT - HUD_HEIGHT) // CELL_SIZE  # игровое поле без HUD

    # верхняя и нижняя границы
    for x in range(cols):
        obstacles.append([x, 0])  # верхняя граница поля (с учётом HUD в Game.py)
        obstacles.append([x, rows - 1])  # нижняя граница

    # левая и правая границы
    for y in range(rows):
        obstacles.append([0, y])  # левая граница
        obstacles.append([cols - 1, y])  # правая граница

    @classmethod
    def get_obstacles(cls):
        return cls.obstacles