from config import WINDOW_WIDTH, WINDOW_HEIGHT, CELL_SIZE, HUD_HEIGHT

class Level3Map:
    name = "Коридоры"

    obstacles = []

    cols = WINDOW_WIDTH // CELL_SIZE
    rows = (WINDOW_HEIGHT - HUD_HEIGHT) // CELL_SIZE  # игровое поле без HUD

    for i in range(10):
        obstacles.append([i+1, 7])
        obstacles.append([25, i+1])
        obstacles.append([i+15, 21])

    for i in range(6):
        obstacles.append([i + 23, 15])
        obstacles.append([5, i + 20])
        obstacles.append([i + 4, 10])
        obstacles.append([i + 25, 5])
        obstacles.append([14, i + 14])

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
