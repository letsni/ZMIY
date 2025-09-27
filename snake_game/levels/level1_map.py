from config import WINDOW_WIDTH, WINDOW_HEIGHT, CELL_SIZE
class Level1Map:
    name = "Уровень 1"

    # создаём прямоугольную рамку вокруг поля
    obstacles = []
    cols = WINDOW_WIDTH // CELL_SIZE
    rows = WINDOW_HEIGHT // CELL_SIZE

    # верх и низ
    for x in range(cols):
        obstacles.append([x, 0])              # верхняя граница
        obstacles.append([x, rows - 1])       # нижняя граница

    # лево и право
    for y in range(rows):
        obstacles.append([0, y])              # левая граница
        obstacles.append([cols - 1, y])       # правая граница

    @classmethod
    def get_obstacles(cls):
        return cls.obstacles