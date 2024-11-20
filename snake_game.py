import pygame
import random
import numpy as np
from enum import Enum
from collections import namedtuple

pygame.init()
font = pygame.font.SysFont("arial", 25)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (225, 0, 0)
TEAL = (0, 128, 128)
CYAN = (0, 200, 200)

BLOCK_SIZE = 20
CLOCK_SPEED = 10

Point = namedtuple("Point", ['x', 'y'])


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


class SnakeGame:

    def __init__(self, w=1280, h=960):
        self.w = w
        self.h = h

        self.display = pygame.display.set_mode((self.w, self.h))
        self.clock = pygame.time.Clock()

        pygame.display.set_caption("Snake")
        self.reset()
        self.frame_iteration = 0

    def reset(self):
        self.score = 0
        self.food = Point(0, 0)

        self.direction = Direction.RIGHT

        self.head = Point(self.w / 2, self.h / 2)
        self.snake = [self.head,
                      Point(self.head.x - BLOCK_SIZE, self.head.y),
                      Point(self.head.x - (2 * BLOCK_SIZE), self.head.y)]

        self._place_food()

    def _place_food(self):
        x = random.randint(0, (self.w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE

        self.food = Point(x, y)

        if self.food in self.snake:
            self._place_food()

    def _update_ui(self):
        self.display.fill(BLACK)

        for pt in self.snake:
            pygame.draw.rect(self.display, TEAL, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, CYAN, pygame.Rect(pt.x + 4, pt.y + 4, 12, 12))

        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Score " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def _move(self, action):
        x = self.head.x
        y = self.head.y

        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        indx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            self.direction = clock_wise[indx]
        elif np.array_equal(action, [0, 1, 0]):
            self.direction = clock_wise[(indx + 1) % 4]
        else:
            self.direction = clock_wise[(indx - 1) % 4]

        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)

    def is_collision(self, pt=None):

        if pt is None:
            pt = self.head

        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True

        if pt in self.snake[1:]:
            return True

        return False

    def play_step(self, action):
        game_over = False
        reward = 0

        self.frame_iteration += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_LEFT and self.direction != Direction.RIGHT:
            #         self.direction = Direction.LEFT
            #     elif event.key == pygame.K_RIGHT and self.direction != Direction.LEFT:
            #         self.direction = Direction.RIGHT
            #     elif event.key == pygame.K_UP and self.direction != Direction.DOWN:
            #         self.direction = Direction.UP
            #     elif event.key == pygame.K_DOWN and self.direction != Direction.UP:
            #         self.direction = Direction.DOWN

        if self.is_collision() or self.frame_iteration > 200 * len(self.snake):
            game_over = True
            reward = -10
            return self.score, game_over, reward

        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()

        self._move(action)
        self.snake.insert(0, self.head)

        self._update_ui()
        self.clock.tick(CLOCK_SPEED)

        return self.score, game_over, reward
