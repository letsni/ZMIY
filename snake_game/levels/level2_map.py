class Level2Map:
    name = "Уровень 2"
    obstacles = [
        [200, 200],
        [240, 200],
        [280, 200]
    ]

    @classmethod
    def get_obstacles(cls):
        return cls.obstacles