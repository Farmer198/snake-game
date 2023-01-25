from __future__ import annotations

import pygame
from typing import List, TYPE_CHECKING
from cube import Cube

__all__ = (
    'Snake'
)

if TYPE_CHECKING:
    from main import Game

class Snake:
    """
    The Snake
    """
    __slots__ = (
        'body',
        'turns',
        'head',
        'dirx',
        'diry',
        '_game',
        'color'
    )

    def __init__(self, color: List, pos: List, game: Game) -> None:
        self.body: List[Cube] = []
        self.turns: dict = {}
        self._game = game

        self.color = color
        self.head: Cube = Cube(pos, game = game, color = color)
        self.body.append(self.head)
        self.dirx = 0
        self.diry = 1

    @property
    def length(self) -> int:
        return len(self.body)

    def add_cupe(self) -> None:
        tail = self.body[-1]
        dx, dy = tail.dirx, tail.diry

        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.pos[0]-1, tail.pos[1]), self._game))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0]+1,tail.pos[1]), self._game))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0],tail.pos[1]-1), self._game))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0],tail.pos[1]+1), self._game))

        self.body[-1].dirx = dx
        self.body[-1].diry = dy

    def remove_cube(self) -> None:
        # removes the last body part
        if self.body:
            self.body.pop()

    def draw(self, screen) -> None:
        for i in self.body:
            i.draw(screen)

    def move(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if self.length == 1 or not self.dirx == 1 and self.length > 1:
                        self.dirx = -1# goes left on x
                        self.diry = 0
                        self.turns[self.head.pos[:]] = [self.dirx,self.diry]
                elif event.key == pygame.K_RIGHT:
                    if self.length == 1 or not self.dirx == -1 and self.length > 1:
                        self.dirx = 1# goes right on x
                        self.diry = 0
                        self.turns[self.head.pos[:]] = [self.dirx,self.diry]
                elif event.key == pygame.K_UP:
                    if self.length == 1 or not self.diry == 1 and self.length > 1:
                        self.dirx = 0
                        self.diry = -1# goes up on y
                        self.turns[self.head.pos[:]] = [self.dirx,self.diry]
                elif event.key == pygame.K_DOWN:
                    if self.length == 1 or not self.diry == -1 and self.length > 1:
                        self.dirx = 0
                        self.diry = 1# goes down on y
                        self.turns[self.head.pos[:]] = [self.dirx,self.diry]
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
                cube.move(cube.dirx,cube.diry)

    def reset(self, pos):
        self.body.clear()
        self.turns.clear()
        self.head = Cube(pos, game = self._game, color = self.color)
        self.body.append(self.head)
        self.dirx = 0
        self.diry = 1
