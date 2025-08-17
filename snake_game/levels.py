LEVELS = [
    # Уровень 1: рамка
    [(x, 0) for x in range(40)] +
    [(x, 29) for x in range(40)] +
    [(0, y) for y in range(30)] +
    [(39, y) for y in range(30)],

    # Уровень 2: две вертикальные стены
    [(10, y) for y in range(5, 25)] +
    [(30, y) for y in range(5, 25)]
]