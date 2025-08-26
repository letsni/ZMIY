import pygame
from config import WHITE, WINDOW_WIDTH, WINDOW_HEIGHT
from levels.level1 import Level1
from levels.level2 import Level2
from levels.level3 import Level3

class Menu:
    def __init__(self, screen):
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
        self.levels = [Level1, Level2, Level3]
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