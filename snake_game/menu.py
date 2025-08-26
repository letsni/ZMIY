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
            "Кастомизация",
            "Выход"
        ]
        self.selected_index = 0

        # Уровни сложности
        self.levels = [Level1Difficulty, Level2Difficulty, Level3Difficulty]
        self.selected_level = 0
        self.menu_items[1] = f"Сложность: {self.levels[self.selected_level].name}"

    def draw(self):
        self.screen.fill((0, 0, 0))
        for i, item in enumerate(self.menu_items):
            color = WHITE if i != self.selected_index else (200, 200, 50)
            text = self.font.render(item, True, color)
            rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + i * 60))
            self.screen.blit(text, rect)
        pygame.display.flip()

    def draw_map_selection(self):
        self.screen.fill((0, 0, 0))
        text = self.font.render("Выберите карту:", True, (255, 255, 255))
        self.screen.blit(text, (50, 50))

        for i, map_cls in enumerate(self.maps):
            color = (200, 200, 0) if i == self.selected_map_index else (255, 255, 255)
            level_text = self.font.render(f"{i + 1}. {map_cls.name}", True, color)
            self.screen.blit(level_text, (100, 100 + i * 40))

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
                elif event.key == pygame.K_RETURN:
                    if self.selected_index == 0:  # Играть
                        return "GAME", self.levels[self.selected_level]
                    elif self.selected_index == 1:  # Сложность
                        self.selected_level = (self.selected_level + 1) % len(self.levels)
                        self.menu_items[1] = f"Сложность: {self.levels[self.selected_level].name}"
                    elif self.selected_index == 2:  # Кастомизация
                        # пока заглушка
                        print("Кастомизация (пока не реализована)")
                    elif self.selected_index == 3:  # Выход
                        return "EXIT", None
        return "MENU", None

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