import pygame
from config import WHITE, WINDOW_WIDTH, WINDOW_HEIGHT
from levels.level1_diff import Level1Difficulty
from levels.level2_diff import Level2Difficulty
from levels.level3_diff import Level3Difficulty
from levels.level1_map import Level1Map
from levels.level2_map import Level2Map
from levels.level3_map import Level3Map
from levels.level4_map import Level4Map

class Menu:
    def __init__(self, screen):
        self.maps = [Level1Map, Level2Map, Level3Map, Level4Map]
        self.selected_map_index = 0
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 40)

        self.menu_items = [
            "Играть",
            "Сложность: Лёгкая",
            "Об игре",
            "Выход"
        ]
        self.selected_index = 0

        # Уровни сложности
        self.levels = [Level1Difficulty, Level2Difficulty, Level3Difficulty]
        self.selected_level = 0
        self.menu_items[1] = f"Сложность: {self.levels[self.selected_level].name}"

    def draw(self):
        self.screen.fill((0, 0, 0))

        # --- название игры ---
        title_font = pygame.font.SysFont("Arial", 80, bold=True)
        title_text = title_font.render("Змейка", True, (10, 200, 20))
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 120))
        self.screen.blit(title_text, title_rect)

        # --- пункты меню ---
        start_y = WINDOW_HEIGHT // 2 - 60
        spacing = 60
        for i, item in enumerate(self.menu_items):
            color = (200, 200, 50) if i == self.selected_index else WHITE

            # Если пункт "Сложность", добавим стрелки
            if i == 1:
                difficulty_name = self.levels[self.selected_level].name
                item_text = f"< {difficulty_name} >"
            else:
                item_text = item

            text = self.font.render(item_text, True, color)
            rect = text.get_rect(center=(WINDOW_WIDTH // 2, start_y + i * spacing))
            self.screen.blit(text, rect)

        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "EXIT", None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_index = (self.selected_index - 1) % len(self.menu_items)
                elif event.key == pygame.K_DOWN:
                    self.selected_index = (self.selected_index + 1) % len(self.menu_items)
                elif event.key == pygame.K_LEFT and self.selected_index == 1:
                    # переключение сложности влево
                    self.selected_level = (self.selected_level - 1) % len(self.levels)
                elif event.key == pygame.K_RIGHT and self.selected_index == 1:
                    # переключение сложности вправо
                    self.selected_level = (self.selected_level + 1) % len(self.levels)
                elif event.key == pygame.K_RETURN:
                    if self.selected_index == 0:  # Играть
                        return "GAME", self.levels[self.selected_level]
                    elif self.selected_index == 2:  # Об игре
                        return "ABOUT", self.levels[self.selected_level]
                    elif self.selected_index == 3:  # Выход
                        return "EXIT", None
        return "MENU", None

    def draw_map_selection(self):
        self.screen.fill((0, 0, 0))
        text = self.font.render("Выберите карту:", True, WHITE)
        self.screen.blit(text, (50, 50))

        for i, map_cls in enumerate(self.maps):
            color = (200, 200, 0) if i == self.selected_map_index else WHITE
            level_text = self.font.render(f"{i + 1}. {map_cls.name}", True, color)
            self.screen.blit(level_text, (100, 100 + i * 40))

        pygame.display.flip()

    def handle_map_selection(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "EXIT", None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_map_index = (self.selected_map_index - 1) % len(self.maps)
                elif event.key == pygame.K_DOWN:
                    self.selected_map_index = (self.selected_map_index + 1) % len(self.maps)
                elif event.key == pygame.K_RETURN:
                    return "GAME", self.maps[self.selected_map_index]
        return "MAP_SELECTION", None