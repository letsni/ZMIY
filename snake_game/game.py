import pygame
import datetime
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
        self.state = "MENU"  # MENU, MAP_SELECTION, GAME, GAME_OVER, NAME_INPUT, CUSTOMIZATION, PAUSE, LEADERBOARD
        self.pause_selected = 0
        self.snake = None
        self.food = None
        self.font = pygame.font.SysFont("Arial", 40)
        self.small_font = pygame.font.SysFont("Arial", 28)  # для таблицы
        self.selected_level = None
        self.score = 0
        self.player_name = ""
        self.cursor_visible = True
        self.cursor_timer = 0
        self.final_score = 0
        self.leaderboard_selected = 0

        # === Для таблицы лидеров ===
        from levels.level1_map import Level1Map
        from levels.level2_map import Level2Map
        from levels.level3_map import Level3Map
        from levels.level4_map import Level4Map
        self.all_maps = [Level1Map, Level2Map, Level3Map, Level4Map]
        self.selected_map_index = 0

    def reset(self, level=None, level_map=None):
        if level is None:
            from levels.level1_diff import Level1Difficulty
            level = Level1Difficulty
        self.selected_level = level
        self.selected_map = level_map
        self.snake = Snake(speed=level.get_speed())
        self.food = Food(self.snake)
        self.score = 0
        self.player_name = ""

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
                        self.paused_frame = self.screen.copy()
                    elif self.state == "PAUSE":
                        self.state = "GAME"

    def update(self):
        self.snake.move()

        # Проверка съеденной еды
        if self.food.check_collision(self.snake):
            self.snake.grow(1)
            self.food = Food(self.snake)
            points = int(10 * self.selected_level.get_score_multiplier())
            self.score += points

        head_pos = [self.snake.head_pos[0], self.snake.head_pos[1]]

        # Столкновение с телом змейки
        if head_pos in self.snake.body[1:]:
            self.final_score = self.score
            self.state = "NAME_INPUT"
            return

        # Столкновение с препятствиями карты
        if self.selected_map:
            obstacles = self.selected_map.get_obstacles()
            if [self.snake.head_pos[0], self.snake.head_pos[1]] in obstacles:
                self.final_score = self.score
                self.state = "NAME_INPUT"

    def draw(self):
        self.screen.fill(BLACK)
        # Рисуем рамку/препятствия карты
        if self.selected_map:
            for obs in self.selected_map.get_obstacles():
                rect = pygame.Rect(obs[0] * CELL_SIZE, obs[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, (100, 100, 100), rect)  # красная рамка
        self.snake.draw(self.screen)
        self.food.draw(self.screen)
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
            color = (200, 200, 0) if i == self.pause_selected else WHITE
            text = self.font.render(option, True, color)
            rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 40 + i * 60))
            self.screen.blit(text, rect)
        pygame.display.flip()

    # === ЛИДЕРБОРД ===
    def save_score(self):
        """Сохраняет результат в формате: name;map;score;date"""
        name = self.player_name.strip() or "Безымянный"
        date = datetime.date.today().isoformat()
        map_name = self.selected_map.name if self.selected_map else "DefaultMap"
        try:
            score_val = int(self.score)
        except Exception:
            score_val = 0
        with open("leaderboard.txt", "a", encoding="utf-8") as f:
            f.write(f"{name};{map_name};{score_val};{date}\n")

    def load_scores(self, map_name):
        """
        Загружает и возвращает список (name, score, date) для переданной map_name.
        Поддерживает оба формата строк в файле:
          - name;map;score;date
          - name;map;diff;score;date   (старый)
        """
        scores = []
        try:
            with open("leaderboard.txt", "r", encoding="utf-8") as f:
                for raw in f:
                    line = raw.strip()
                    if not line:
                        continue
                    parts = [p.strip() for p in line.split(";")]
                    # поддерживаем оба формата
                    if len(parts) == 4:
                        name, map_, score_str, date = parts
                    elif len(parts) == 5:
                        # старый формат: name;map;diff;score;date
                        name, map_, _diff, score_str, date = parts
                    else:
                        # нераспознанная / поврежденная строка — пропускаем
                        continue
                    try:
                        score_int = int(score_str)
                    except ValueError:
                        continue
                    if map_ == map_name:
                        scores.append((name, score_int, date))
        except FileNotFoundError:
            return []
        # сортируем по убыванию очков
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:10]

    def normalize_leaderboard_file(self):
        """
        (опционально) Приводит все записи leaderboard.txt к единому формату
        name;map;score;date. Перезаписывает файл. Выполнять один раз вручную при желании.
        """
        normalized = []
        try:
            with open("leaderboard.txt", "r", encoding="utf-8") as f:
                for raw in f:
                    line = raw.strip()
                    if not line:
                        continue
                    parts = [p.strip() for p in line.split(";")]
                    if len(parts) == 4:
                        name, map_, score_str, date = parts
                    elif len(parts) == 5:
                        name, map_, _diff, score_str, date = parts
                    else:
                        continue
                    try:
                        score_int = int(score_str)
                    except ValueError:
                        continue
                    normalized.append((name, map_, score_int, date))
        except FileNotFoundError:
            return  # нечего нормализовать

        # перезаписываем в единый формат
        with open("leaderboard.txt", "w", encoding="utf-8") as f:
            for name, map_, score_int, date in normalized:
                f.write(f"{name};{map_};{score_int};{date}\n")

    def draw_leaderboard(self):
        self.screen.fill((30, 30, 30))

        map_name = self.all_maps[self.selected_map_index].name if self.all_maps else "DefaultMap"

        # Заголовок со стрелками
        title_color = (200, 200, 0) if self.leaderboard_selected == 0 else WHITE
        title_text = f"<  {map_name}  >"
        title = self.font.render(title_text, True, title_color)
        self.screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 50))

        # Таблица
        scores = self.load_scores(map_name)
        if not scores:
            text = self.font.render("Нет данных", True, WHITE)
            self.screen.blit(text, (100, 150))
        else:
            headers = ["Имя", "Счёт", "Дата"]
            col_widths = [200, 100, 150]
            x_start = 150
            for i, header in enumerate(headers):
                text = self.small_font.render(header, True, WHITE)
                self.screen.blit(text, (x_start + sum(col_widths[:i]), 120))

            for row_idx, (name, score, date) in enumerate(scores):
                y = 160 + row_idx * 40
                row = [name, str(score), date]
                for col_idx, cell in enumerate(row):
                    text = self.small_font.render(cell, True, WHITE)
                    self.screen.blit(text, (x_start + sum(col_widths[:col_idx]), y))

        # Кнопка "Назад"
        back_color = (200, 200, 0) if self.leaderboard_selected == 1 else WHITE
        back_text = self.font.render("Назад", True, back_color)
        rect = back_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 80))
        self.screen.blit(back_text, rect)

        pygame.display.flip()

    # === ВВОД ИМЕНИ ===
    def draw_name_input(self):
        self.screen.fill((20, 20, 20))

        prompt = self.font.render("Введите имя (Enter для пропуска):", True, WHITE)
        self.screen.blit(prompt, (WINDOW_WIDTH // 2 - prompt.get_width() // 2, 180))

        score_text = self.font.render(f"Ваш счёт: {self.final_score}", True, (100, 200, 100))
        self.screen.blit(score_text, (WINDOW_WIDTH // 2 - score_text.get_width() // 2, 240))

        display_name = self.player_name
        if self.cursor_visible:
            display_name += "|"
        name_text = self.font.render(display_name, True, (200, 200, 0))
        self.screen.blit(name_text, (WINDOW_WIDTH // 2 - name_text.get_width() // 2, 320))

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
                    self.state = "MAP_SELECTION"
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
                            if self.pause_selected == 0:
                                self.state = "GAME"
                            elif self.pause_selected == 1:
                                self.state = "MENU"
                            elif self.pause_selected == 2:
                                self.state = "MENU"
                        elif event.key == pygame.K_ESCAPE:
                            self.state = "GAME"
                self.draw_pause_menu()

            elif self.state == "NAME_INPUT":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            self.save_score()
                            self.state = "GAME_OVER"
                        elif event.key == pygame.K_BACKSPACE:
                            self.player_name = self.player_name[:-1]
                        else:
                            if event.unicode.isprintable():
                                if len(self.player_name) < 10:
                                    test_text = self.font.render(self.player_name + event.unicode, True, (200, 200, 0))
                                    if test_text.get_width() < WINDOW_WIDTH - 100:
                                        self.player_name += event.unicode

                self.cursor_timer += 1
                if self.cursor_timer >= FPS // 2:
                    self.cursor_visible = not self.cursor_visible
                    self.cursor_timer = 0
                self.draw_name_input()

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
                            if self.game_over_selected == 0:
                                self.reset(level=self.selected_level)
                                self.state = "GAME"
                            elif self.game_over_selected == 1:
                                self.state = "LEADERBOARD"
                            elif self.game_over_selected == 2:
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
                            self.state = "GAME_OVER"
                        elif event.key == pygame.K_RIGHT and self.leaderboard_selected == 0:
                            self.selected_map_index = (self.selected_map_index + 1) % len(self.all_maps)
                        elif event.key == pygame.K_LEFT and self.leaderboard_selected == 0:
                            self.selected_map_index = (self.selected_map_index - 1) % len(self.all_maps)
                        elif event.key == pygame.K_DOWN:
                            self.leaderboard_selected = 1
                        elif event.key == pygame.K_UP:
                            self.leaderboard_selected = 0
                        elif event.key == pygame.K_RETURN:
                            if self.leaderboard_selected == 1:
                                self.state = "GAME_OVER"
                self.draw_leaderboard()

            self.clock.tick(FPS)
