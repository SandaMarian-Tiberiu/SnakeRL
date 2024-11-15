import pygame

pygame.init()


class SnakeGame:

    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h

        self.display = pygame.display.set_mode((self.w, self.h))
        self.clock = pygame.time.Clock()

        pygame.display.set_caption("Snake")

    def play_step(self):
        pass


if __name__ == "__main__":
    game = SnakeGame()

    while True:
        game.play_step()

        break

    pygame.quit()
