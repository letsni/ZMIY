import pygame
import sys
from config import WINDOW_WIDTH, WINDOW_HEIGHT
from game import Game

def main():
    pygame.init()
    pygame.display.set_caption("Snake Game")

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    game = Game(screen)
    game.run()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()