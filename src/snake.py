from __future__ import annotations

import pygame
from typing import List, TYPE_CHECKING, Tuple
from cube import Cube
from enums import Colors

__all__ = (
    'Snake'
)

if TYPE_CHECKING:
    from main import Game
    from pygame import Surface

class Snake:
    """
    Represents the Snake.
    """
    __slots__ = (
        'body',
        'turns',
        'head',
        'change_x',
        'change_y',
        'color',
        '_game'
    )

    def __init__(self, color: Colors, pos: Tuple, game: Game) -> None:
        self.body: List[Cube] = []
        self.turns: dict = {}
        self._game = game
        self.color: Colors = color

        self.head: Cube = Cube(pos, game = game, color = color)
        self.body.append(self.head)
        self.change_x = 0
        self.change_y = 1

    @property
    def length(self) -> int:
        return len(self.body)

    def add_cube(self) -> None:
        """Adds a cube to the Snake."""
        tail = self.body[-1]
        dx, dy = tail.change_x, tail.change_y

        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.pos[0]-1, tail.pos[1]), self._game))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0]+1, tail.pos[1]), self._game))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1]-1), self._game))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0], tail.pos[1]+1), self._game))

        self.body[-1].change_x = dx
        self.body[-1].change_y = dy

    def remove_cube(self) -> None:
        """Removes a cube from the Snake."""
        # removes the last body part
        if self.body:
            self.body.pop()

    def draw(self) -> None:
        """Draws all cubes from the Snake."""
        for i in self.body:
            i.draw()

    def move(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if self.length == 1 or not self.change_x == 1 and self.length > 1:
                        self.change_x = -1# goes left on x
                        self.change_y = 0
                        self.turns[self.head.pos[:]] = [self.change_x, self.change_y]
                elif event.key == pygame.K_RIGHT:
                    if self.length == 1 or not self.change_x == -1 and self.length > 1:
                        self.change_x = 1# goes right on x
                        self.change_y = 0
                        self.turns[self.head.pos[:]] = [self.change_x, self.change_y]
                elif event.key == pygame.K_UP:
                    if self.length == 1 or not self.change_y == 1 and self.length > 1:
                        self.change_x = 0
                        self.change_y = -1# goes up on y
                        self.turns[self.head.pos[:]] = [self.change_x, self.change_y]
                elif event.key == pygame.K_DOWN:
                    if self.length == 1 or not self.change_y == -1 and self.length > 1:
                        self.change_x = 0
                        self.change_y = 1# goes down on y
                        self.turns[self.head.pos[:]] = [self.change_x, self.change_y]
                elif event.key == pygame.K_ESCAPE:
                    self._game.game_end()
        
        for num, cube in enumerate(self.body):
            p = cube.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                cube.move(turn[0], turn[1])
                if num == self.length-1:
                    self.turns.pop(p)
            else:
                cube.move(cube.change_x, cube.change_y)

    def reset(self, pos: Tuple) -> None:
        """Resets the Snake."""
        self.body.clear()
        self.turns.clear()
        self.head = Cube(pos, game = self._game, color = self.color)
        self.body.append(self.head)
        self.change_x = 0
        self.change_y = 1
