from __future__ import annotations

import pygame
import time

from food import Food
from snake import Snake
from enums import GameMode

pygame.init()


# Screen Information
width = 600 
height = 600

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('simplesnakegame')
font = pygame.font.SysFont('Roboto', 60)

GREEN = (0, 225, 0)
WHITE = (225, 225, 225)
RED = (225, 0, 0)
BLACK = (0, 0, 0)

# Clock
clock = pygame.time.Clock()

__all__ = (
    'Game'
)

class Game:
    def __init__(self, gamemode: GameMode) -> None:
        self.snake: Snake = None
        self.food: Food = None
        self.delay: float = gamemode.value
        self.max_length: int = 100

        # screen settings
        self.cols: int = 30
        self.rows: int = 30
        self.cell_width: float = width / self.cols
        self.cell_height: float = height / self.rows

        # startet das spiel
        self.main()

    def game_end(self) -> None:
        screen.fill(BLACK)
        score = font.render(f'Score: {self.snake.length}', 1, WHITE)
        screen.blit(score, (10, 10))
        pygame.display.flip()
        time.sleep(1.5)
        self.snake.reset((10, 10))

    def place_food(self) -> None:
        self.food = Food(self)

    def create_snake(self) -> None:
        self.snake = Snake(RED, (10, 10), self)

    def check_game_over(self) -> None:
        if self.snake.head.pos[0] >= 30 or self.snake.head.pos[0] < 0 or self.snake.head.pos[1] >= 30 or self.snake.head.pos[1] < 0:
            self.game_end()

        for i in range(self.snake.length):
            if self.snake.body[i].pos in list(map(lambda z: z.pos, self.snake.body[i+1:])):
                self.game_end()

        if self.snake.length >= self.max_length:
            self.game_end()

    def main(self) -> None:
        stopped = False

        # creates the snake
        self.create_snake()
        self.place_food()

        while not stopped:
            self.snake.move()

            if self.snake.body[0].pos == self.food.pos:
                self.snake.add_cupe()
                self.place_food()

            # checks the snake
            self.check_game_over()

            screen.fill(BLACK)

            # placec the food
            self.food.draw(screen)

            # snake body
            self.snake.draw(screen)

            # updates the screen
            pygame.display.flip()

            time.sleep(self.delay)

if __name__ == '__main__':
    Game(GameMode.Hard)
