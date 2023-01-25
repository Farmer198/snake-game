from __future__ import annotations

from random import randrange, randint
from typing import TYPE_CHECKING
from cube import Cube

__all__ = (
    'Food'
)

if TYPE_CHECKING:
    from .main import Game

class Food(Cube):
    """
    The Food

    """
    __slots__ = (
        'quality'
    )
    def __init__(self, game: Game, dirx: int = 1, diry: int = 0, color = (0, 225, 0)) -> None:
        super().__init__((0, 0), game, dirx, diry, color)

        self.quality = randrange(1, 2)
        self.pos = (randint(1, self._game.cols - 2), randint(1, self._game.rows - 2))
