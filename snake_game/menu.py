import pygame
from config import WHITE, WINDOW_WIDTH, WINDOW_HEIGHT

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 40)

    def draw(self):
        self.screen.fill((0, 0, 0))
        text = self.font.render("Нажми ENTER чтобы играть", True, WHITE)
        rect = text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
        self.screen.blit(text, rect)
        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "EXIT"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return "GAME"
        return "MENU"