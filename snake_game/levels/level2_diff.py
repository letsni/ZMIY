class Level2Difficulty:
    name = "Средний"
    speed = 10
    score_multiplier = 3.0  # коэффициент для очков

    @classmethod
    def get_speed(cls):
        return cls.speed

    @classmethod
    def get_score_multiplier(cls):
        return cls.score_multiplier