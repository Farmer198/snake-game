from __future__ import annotations

import pygame
from typing import List, TYPE_CHECKING

__all__ = (
    'Cube'
)

if TYPE_CHECKING:
    from .main import Game

class Cube:
    """
    A Cube of the Snake.
    """

    __slots__ = (
        '_game',
        'pos',
        'dirx',
        'diry',
        'color'
    )
    def __init__(self, start: List, game: Game, dirx: int = 1, diry: int = 0, color = (255, 0, 0)) -> None:
        self._game: Game = game
        self.pos: List = start # [x, y]
        self.dirx: int = dirx
        self.diry: int = diry
        self.color: List = color

    def move(self, dirx: int, diry: int) -> None:
        self.dirx = dirx
        self.diry = diry
        self.pos = (self.pos[0] + self.dirx, self.pos[1] + self.diry)

    def draw(self, screen) -> None:
        x = self.pos[0]
        y = self.pos[1]
        disw = self._game.cell_width
        dish = self._game.cell_height

        pygame.draw.rect(screen, self.color, (x*dish+1, y*disw+1, dish-1, disw-1))


    def __repr__(self) -> str:
        return "<Cube pos_x={} pos_y={}".format(self.pos_x, self.pos_y)
