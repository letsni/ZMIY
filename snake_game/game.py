import pygame
from config import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, BLACK
from snake import Snake
from food import Food

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()

        # Создаём объекты
        self.snake = Snake(speed=4)
        self.food = Food(self.snake)
        self.running = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.snake.change_direction(0, -1)
                elif event.key == pygame.K_DOWN:
                    self.snake.change_direction(0, 1)
                elif event.key == pygame.K_LEFT:
                    self.snake.change_direction(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    self.snake.change_direction(1, 0)

    def update(self):
        self.snake.move()

        # Проверка: съела ли змейка еду
        if self.snake.head_pos == self.food.position:
            self.snake.length += 1
            self.food = Food(self.snake)

    def draw(self):
        self.screen.fill(BLACK)
        self.snake.draw(self.screen)
        self.food.draw(self.screen)
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)