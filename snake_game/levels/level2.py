class Level2:
    name = "Средний"
    speed = 10
    obstacles = []

    @classmethod
    def get_speed(cls):
        return cls.speed

    @classmethod
    def get_obstacles(cls):
        return cls.obstacles