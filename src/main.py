from __future__ import annotations

import pygame
import time
import math

from pygame import Surface
from pygame.font import Font
from pygame.time import Clock
from typing import Optional
from json import load, dump
from food import Food
from snake import Snake
from cube import Cube
from enums import GameMode, Colors

pygame.init()

# Screen Information
width = 1000
height = 1000

pygame.display.set_caption('simplesnakegame')

# Clock
clock = pygame.time.Clock()

__all__ = (
    'Game'
)


class Game:
    def __init__(self, game_mode: GameMode, game_surface: Surface, game_font: Font, game_clock: Clock) -> None:
        self.snake: Optional[Snake] = None
        self.food: Optional[Food] = None
        self.cache: dict = {}
        self.stopped: bool = False

        # pygame stuff
        self.surface: Surface = game_surface
        self.font: Font = game_font
        self.clock: Clock = game_clock

        # game settings
        self.delay: float = game_mode.value
        self.max_length: int = 100
        self.show_fps: bool = True

        # screen settings
        self.cols: int = 60
        self.rows: int = 60
        self.cell_width: float = width / self.cols
        self.cell_height: float = height / self.rows

    def run(self) -> None:
        # starts the game
        self.get_savegame()
        self.main()

    def get_savegame(self) -> None:
        try:
            with open('./snake-save.json', 'r') as file:
                data = load(file)
                self.cache.update(data)
        # if the file dose not exists
        except Exception as exc:
            pass

    def update_savegame(self) -> None:
        with open('./snake-save.json', 'w') as file:
            dump(
                self.cache,
                file,
                # looks better
                indent=4
            )

    def game_end(self) -> None:
        if self.cache.get('highscore', 0) < self.snake.length:
            self.cache['highscore'] = self.snake.length
            self.update_savegame()
        self.surface.fill(Colors.Black.value)
        score = self.font.render(
            f"Score: {self.snake.length} | High-score: {self.cache.get('highscore', self.snake.length)}", True,
            Colors.White.value)
        self.surface.blit(score, (10, 10))
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
        self.snake = Snake(Colors.Pink, (10, 10), self)

    def check_game_over(self) -> None:
        if self.snake.head.pos[0] >= self.rows or self.snake.head.pos[0] < 0 or self.snake.head.pos[1] >= self.cols or \
                self.snake.head.pos[1] < 0:
            self.game_end()
            return

        for i in range(self.snake.length):
            if self.snake.body[i].pos in list(map(lambda z: z.pos, self.snake.body[i + 1:])):
                self.game_end()
                break

        if self.snake.length >= self.max_length:
            self.game_end()
            return

    def draw_fps(self, color: Colors = Colors.White) -> None:
        score = self.font.render(f"FPS: {math.ceil(self.clock.get_fps())}", True, color.value)
        self.surface.blit(score, (30, 30))

    def main(self) -> None:

        # creates the snake
        self.create_snake()
        self.place_food()

        while not self.stopped:
            self.clock.tick(30)
            self.snake.move()

            if self.snake.body[0].pos == self.food.pos:
                for i in range(self.food.quality):
                    self.snake.add_cube()
                self.place_food()

            # checks the snake
            self.check_game_over()

            self.surface.fill(Colors.Black.value)

            # places the food
            self.food.draw()

            # snake body
            self.snake.draw()

            if self.show_fps:
                self.draw_fps()

            # updates the screen
            pygame.display.flip()
            time.sleep(self.delay)


if __name__ == '__main__':
    game_mode = GameMode.Hard
    game_surface = pygame.display.set_mode((width, height))
    game_font = pygame.font.SysFont('Roboto', 60)
    game_clock = Clock()
    game = Game(
        game_mode,
        game_surface,
        game_font,
        game_clock
    )
    game.run()
