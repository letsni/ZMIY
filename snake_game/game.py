import pygame
from config import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, BLACK, WHITE, CELL_SIZE
from snake import Snake
from food import Food

class Game:
    def __init__(self, screen):
        self.game_over_selected = 0
        self.paused_frame = None
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "MENU"  # MENU, GAME, GAME_OVER, CUSTOMIZATION, PAUSE
        self.pause_selected = 0
        self.snake = None
        self.food = None
        self.font = pygame.font.SysFont("Arial", 40)
        self.selected_level = None

    def reset(self, level=None):
        """Начало новой игры"""
        if level is None:
            from levels.level1 import Level1
            level = Level1
        self.selected_level = level
        self.snake = Snake(speed=level.get_speed())
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
                    if self.state == "GAME":
                        self.state = "PAUSE"
                        self.pause_selected = 0
                        # сохраняем текущий кадр
                        self.paused_frame = self.screen.copy()
                    elif self.state == "PAUSE":
                        self.state = "GAME"

    def update(self):
        self.snake.move()
        if self.food.check_collision(self.snake):
            self.snake.grow(1)
            self.food = Food(self.snake)

        if self.snake.head_pos in self.snake.body[1:]:
            self.state = "GAME_OVER"

    def draw(self):
        self.screen.fill(BLACK)
        self.snake.draw(self.screen)
        self.food.draw(self.screen)
        pygame.display.flip()

    def draw_game_over(self, selected_option):
        self.screen.fill(BLACK)

        # затем полупрозрачный слой (можно убрать, если не нужно)
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        options = ["Перезапустить уровень", "Таблица лидеров", "Выйти в меню"]
        for i, option in enumerate(options):
            color = (200, 200, 0) if i == selected_option else WHITE
            text = self.font.render(option, True, color)
            rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 40 + i * 60))
            self.screen.blit(text, rect)

        pygame.display.flip()

    def draw_pause_menu(self):
        # используем сохранённый кадр
        if self.paused_frame:
            self.screen.blit(self.paused_frame, (0, 0))

        # накладываем полупрозрачный слой
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))

        # рисуем пункты меню
        options = ["Продолжить", "Главное меню", "Сохранить и выйти"]
        for i, option in enumerate(options):
            color = (200, 200, 0) if i == self.pause_selected else (255, 255, 255)
            text = self.font.render(option, True, color)
            rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 40 + i * 60))
            self.screen.blit(text, rect)

        pygame.display.flip()

    def run(self):
        from menu import Menu
        menu = Menu(self.screen)

        pause_selected = 0  # выбранный пункт паузы

        while self.running:
            if self.state == "MENU":
                next_state, selected_level = menu.handle_events()
                menu.draw()
                if next_state == "GAME" and selected_level:
                    self.reset(level=selected_level)
                    self.state = "GAME"
                elif next_state == "EXIT":
                    self.running = False
                elif next_state == "CUSTOMIZATION":
                    self.state = "CUSTOMIZATION"

            elif self.state == "GAME":
                self.handle_events()
                self.update()
                self.draw()

            elif self.state == "PAUSE":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            self.pause_selected = (self.pause_selected - 1) % 3
                        elif event.key == pygame.K_DOWN:
                            self.pause_selected = (self.pause_selected + 1) % 3
                        elif event.key == pygame.K_RETURN:
                            if self.pause_selected == 0:  # Продолжить
                                self.state = "GAME"
                            elif self.pause_selected == 1:  # Главное меню
                                self.state = "MENU"
                            elif self.pause_selected == 2:  # Сохранить и выйти
                                self.state = "MENU"
                        elif event.key == pygame.K_ESCAPE:
                            self.state = "GAME"

                self.draw_pause_menu()



            elif self.state == "GAME_OVER":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            self.game_over_selected = (self.game_over_selected - 1) % 3
                        elif event.key == pygame.K_DOWN:
                            self.game_over_selected = (self.game_over_selected + 1) % 3
                        elif event.key == pygame.K_RETURN:
                            if self.game_over_selected == 0:  # Перезапустить уровень
                                self.reset(level=self.selected_level)
                                self.state = "GAME"
                            elif self.game_over_selected == 1:  # Таблица лидеров (заглушка)
                                self.state = "LEADERBOARD"
                            elif self.game_over_selected == 2:  # Выйти в меню
                                self.state = "MENU"
                        elif event.key == pygame.K_ESCAPE:  # тоже можно выйти в меню
                            self.state = "MENU"
                self.draw_game_over(self.game_over_selected)

            elif self.state == "CUSTOMIZATION":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.state = "MENU"
                self.screen.fill((30, 30, 30))
                text = self.font.render("Кастомизация (пока заглушка)", True, WHITE)
                rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
                self.screen.blit(text, rect)
                pygame.display.flip()

            elif self.state == "LEADERBOARD":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.state = "GAME_OVER"  # возвращаемся обратно в меню Game Over

                # Рисуем заглушку
                self.screen.fill((30, 30, 30))
                text = self.font.render("Таблица лидеров (заглушка)", True, WHITE)
                rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
                self.screen.blit(text, rect)
                pygame.display.flip()

            self.clock.tick(FPS)