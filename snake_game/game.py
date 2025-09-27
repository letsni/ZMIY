import pygame
from config import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, BLACK, WHITE, CELL_SIZE
from snake import Snake
from food import Food

class Game:
    def __init__(self, screen):
        self.selected_map = None
        self.game_over_selected = 0
        self.paused_frame = None
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "MENU"  # MENU, MAP_SELECTION, GAME, GAME_OVER, CUSTOMIZATION, PAUSE, LEADERBOARD
        self.pause_selected = 0
        self.snake = None
        self.food = None
        self.font = pygame.font.SysFont("Arial", 40)
        self.selected_level = None
        self.score = 0  # ← ДОБАВЛЕНО: счёт игрока

    def reset(self, level=None, level_map=None):
        """Начало новой игры"""
        if level is None:
            from levels.level1_diff import Level1Difficulty
            level = Level1Difficulty
        self.selected_level = level
        self.selected_map = level_map  # сохраняем выбранную карту
        self.snake = Snake(speed=level.get_speed())
        self.food = Food(self.snake)
        self.score = 0  # ← ДОБАВЛЕНО: обнуляем счёт
        # TODO: в будущем можно использовать level_map для расстановки препятствий

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
                        self.paused_frame = self.screen.copy()  # сохраняем текущий кадр
                    elif self.state == "PAUSE":
                        self.state = "GAME"

    def update(self):
        self.snake.move()
        if self.food.check_collision(self.snake):
            self.snake.grow(1)
            self.food = Food(self.snake)
            # ← ДОБАВЛЕНО: начисляем очки за еду
            points = int(10 * self.selected_level.get_score_multiplier())
            self.score += points

        if self.snake.head_pos in self.snake.body[1:]:
            self.state = "GAME_OVER"
            self.save_score()  # ← ДОБАВЛЕНО: сохраняем результат в таблицу лидеров

    def draw(self):
        self.screen.fill(BLACK)
        self.snake.draw(self.screen)
        self.food.draw(self.screen)

        # ← ДОБАВЛЕНО: рисуем счёт в левом верхнем углу
        score_text = self.font.render(f"Счёт: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

        pygame.display.flip()

    def draw_game_over(self, selected_option):
        self.screen.fill(BLACK)
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
        if self.paused_frame:
            self.screen.blit(self.paused_frame, (0, 0))
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))

        options = ["Продолжить", "Главное меню", "Сохранить и выйти"]
        for i, option in enumerate(options):
            color = (200, 200, 0) if i == self.pause_selected else (255, 255, 255)
            text = self.font.render(option, True, color)
            rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 40 + i * 60))
            self.screen.blit(text, rect)

        pygame.display.flip()

    # ← ДОБАВЛЕНО: метод сохранения очков в файл
    def save_score(self):
        with open("leaderboard.txt", "a", encoding="utf-8") as f:
            f.write(f"{self.selected_level.name}: {self.score}\n")

    # ← ДОБАВЛЕНО: метод отображения таблицы лидеров
    def draw_leaderboard(self):
        self.screen.fill((30, 30, 30))
        try:
            with open("leaderboard.txt", "r", encoding="utf-8") as f:
                lines = f.readlines()[-5:]  # показываем последние 5 игр
        except FileNotFoundError:
            lines = ["Нет данных"]

        title = self.font.render("Таблица лидеров", True, WHITE)
        self.screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 50))

        for i, line in enumerate(reversed(lines)):
            text = self.font.render(line.strip(), True, WHITE)
            self.screen.blit(text, (100, 150 + i * 50))

        pygame.display.flip()

    def run(self):
        from menu import Menu
        menu = Menu(self.screen)

        while self.running:
            if self.state == "MENU":
                next_state, selected_level = menu.handle_events()
                menu.draw()
                if next_state == "GAME" and selected_level:
                    self.selected_level_difficulty = selected_level
                    self.state = "MAP_SELECTION"  # после выбора уровня — карта
                elif next_state == "EXIT":
                    self.running = False
                elif next_state == "CUSTOMIZATION":
                    self.state = "CUSTOMIZATION"

            elif self.state == "MAP_SELECTION":
                next_state, selected_map = menu.handle_map_selection()
                menu.draw_map_selection()
                if next_state == "GAME" and selected_map:
                    self.reset(level=self.selected_level_difficulty, level_map=selected_map)
                    self.state = "GAME"
                elif next_state == "EXIT":
                    self.state = "MENU"

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
                            elif self.game_over_selected == 1:  # Таблица лидеров
                                self.state = "LEADERBOARD"
                            elif self.game_over_selected == 2:  # Выйти в меню
                                self.state = "MENU"
                        elif event.key == pygame.K_ESCAPE:
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
                self.draw_leaderboard()  # ← ЗАМЕНА заглушки на реальную таблицу

            self.clock.tick(FPS)