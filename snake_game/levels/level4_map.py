class Level4Map:
    name = "Уровень 4"
    obstacles = []  # список препятствий [[x1, y1], [x2, y2], ...]

    @classmethod
    def get_obstacles(cls):
        return cls.obstacles