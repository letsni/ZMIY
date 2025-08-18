import pygame
from config import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, BLACK, WHITE, CELL_SIZE
from snake import Snake
from food import Food

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "MENU"  # начальное состояние

        # Эти объекты создадим при reset()
        self.snake = None
        self.food = None
        self.font = pygame.font.SysFont("Arial", 40)

    def reset(self):
        """Начало новой игры"""
        self.snake = Snake(speed=10)
        self.food = Food(self.snake)

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
                elif event.key == pygame.K_ESCAPE:
                    self.state = "MENU"  # выход в меню

    def update(self):
        self.snake.move()
        # Проверка: съела ли змейка еду
        if self.food.check_collision(self.snake):
            self.snake.grow(1)
            self.food = Food(self.snake)

        # проверка: не врезалась ли змейка
        if self.snake.head_pos in self.snake.body[1:]:
            self.state = "GAME_OVER"

    def draw(self):
        self.screen.fill(BLACK)
        self.snake.draw(self.screen)
        self.food.draw(self.screen)
        pygame.display.flip()

    def draw_game_over(self):
        self.screen.fill(BLACK)
        text1 = self.font.render("Ты проиграл!", True, WHITE)
        text2 = self.font.render("Нажми ENTER чтобы рестартнуть", True, WHITE)

        rect1 = text1.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 40))
        rect2 = text2.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 40))

        self.screen.blit(text1, rect1)
        self.screen.blit(text2, rect2)
        pygame.display.flip()



    def run(self):
        from menu import Menu
        menu = Menu(self.screen)

        while self.running:
            if self.state == "MENU":
                next_state = menu.handle_events()
                menu.draw()
                if next_state == "GAME":
                    self.reset()
                    self.state = "GAME"
                elif next_state == "EXIT":
                    self.running = False

            elif self.state == "GAME":
                self.handle_events()
                self.update()
                self.draw()


            elif self.state == "GAME_OVER":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:  # рестарт
                            self.reset()
                            self.state = "GAME"
                        elif event.key == pygame.K_ESCAPE:  # выход в меню
                            self.state = "MENU"
                self.draw_game_over()


            self.clock.tick(FPS)