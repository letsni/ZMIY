import pygame
import os
from config import WHITE, WINDOW_WIDTH, WINDOW_HEIGHT

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 40)

        # Находим все файлы уровней
        self.level_files = sorted([f for f in os.listdir("levels") if f.startswith("level") and f.endswith(".py")])
        # Создаём имена уровней через классы
        self.level_classes = []
        for file in self.level_files:
            module_name = f"levels.{file[:-3]}"  # убираем .py
            level_module = __import__(module_name, fromlist=["*"])
            # ищем первый класс в модуле
            for attr in dir(level_module):
                obj = getattr(level_module, attr)
                if isinstance(obj, type):
                    self.level_classes.append(obj)
                    break

        self.options = [lvl.name for lvl in self.level_classes]
        self.options.append("Выход")
        self.selected = 0

    def draw(self):
        self.screen.fill((0, 0, 0))
        for i, option in enumerate(self.options):
            color = WHITE if i == self.selected else (100, 100, 100)
            text = self.font.render(option, True, color)
            rect = text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + i*50))
            self.screen.blit(text, rect)
        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "EXIT", None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected = (self.selected - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected = (self.selected + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    if self.selected == len(self.options) - 1:
                        return "EXIT", None
                    return "GAME", self.level_classes[self.selected]
        return "MENU", None