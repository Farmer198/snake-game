from __future__ import annotations

import pygame
import time
import math

from json import load, dump
from food import Food
from snake import Snake
from cube import Cube
from enums import GameMode

pygame.init()


# Screen Information
width = 1000
height = 1000

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
        self.show_fps: bool = True
        self.cache: dict = {}

        # screen settings
        self.cols: int = 60
        self.rows: int = 60
        self.cell_width: float = width / self.cols
        self.cell_height: float = height / self.rows

        # startet das spiel
        self.get_savegame()
        self.main()

    def get_savegame(self) -> None:
        try:
            with open('./snake-save.json', 'r') as file:
                data = load(file)
                self.cache.update(data)
        # if the file dose not exists
        except:
            pass 

    def update_savegame(self) -> None:
        with open('./snake-save.json', 'w') as file:
            dump(
                self.cache,
                file,
                # looks better
                indent = 4
            )

    def game_end(self) -> None:
        if self.cache.get('highscore', 0) < self.snake.length:
            self.cache['highscore'] = self.snake.length
            self.update_savegame()
        screen.fill(BLACK)
        score = font.render(f"Score: {self.snake.length} | Highscore: {self.cache.get('highscore', self.snake.length)}", 1, WHITE)
        screen.blit(score, (10, 10))
        pygame.display.flip()
        time.sleep(1.5)
        self.snake.reset((10, 10))

    def place_food(self) -> None:
        self.food = Food(self)

        def get_pos(cube: Cube):
            return cube.pos

        while self.food.pos in list(map(get_pos, self.snake.body)):
            self.food = Food(self)

    def create_snake(self) -> None:
        self.snake = Snake(RED, (10, 10), self)

    def check_game_over(self) -> None:
        if self.snake.head.pos[0] >= self.rows or self.snake.head.pos[0] < 0 or self.snake.head.pos[1] >= self.cols or self.snake.head.pos[1] < 0:
            self.game_end()
            return

        for i in range(self.snake.length):
            if self.snake.body[i].pos in list(map(lambda z: z.pos, self.snake.body[i+1:])):
                self.game_end()
                break

        if self.snake.length >= self.max_length:
            self.game_end()
            return

    def draw_fps(self, screen):
        score = font.render(f"FPS: {math.ceil(clock.get_fps())}", 1, WHITE)
        screen.blit(score, (30, 30))

    def main(self) -> None:
        stopped = False

        # creates the snake
        self.create_snake()
        self.place_food()

        while not stopped:
            clock.tick(30)
            self.snake.move()

            if self.snake.body[0].pos == self.food.pos:
                for i in range(self.food.quality):
                    self.snake.add_cupe()
                self.place_food()

            # checks the snake
            self.check_game_over()

            screen.fill(BLACK)

            # placec the food
            self.food.draw(screen)

            # snake body
            self.snake.draw(screen)

            if self.show_fps:
                self.draw_fps(screen)

            # updates the screen
            pygame.display.flip()
            time.sleep(self.delay)

if __name__ == '__main__':
    Game(GameMode.Hard)
