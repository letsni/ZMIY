class Level3Difficulty:
    name = "Сложный"
    speed = 20
    score_multiplier = 10.0

    @classmethod
    def get_speed(cls):
        return cls.speed

    @classmethod
    def get_score_multiplier(cls):
        return cls.score_multiplier