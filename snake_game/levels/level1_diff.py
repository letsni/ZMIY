class Level1Difficulty:
    name = "Лёгкая (x1.0)"
    speed = 5          # пикселей за кадр
    score_multiplier = 1.0  # коэффициент для очков

    @classmethod
    def get_speed(cls):
        return cls.speed

    @classmethod
    def get_score_multiplier(cls):
        return cls.score_multiplier