class Level1:
    name = "Лёгкий"
    speed = 4
    obstacles = []

    @classmethod
    def get_speed(cls):
        return cls.speed

    @classmethod
    def get_obstacles(cls):
        return cls.obstacles