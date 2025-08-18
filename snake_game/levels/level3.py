class Level3:
    name = "Сложный"
    speed = 8
    obstacles = []

    @classmethod
    def get_speed(cls):
        return cls.speed

    @classmethod
    def get_obstacles(cls):
        return cls.obstacles