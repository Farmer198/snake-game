from __future__ import annotations

from random import randint
from typing import TYPE_CHECKING
from cube import Cube
from enums import Colors

__all__ = (
    'Food'
)

if TYPE_CHECKING:
    from main import Game


class Food(Cube):
    """
    Represents the Food Cube for the Snake.
    """
    __slots__ = (
        'quality'
    )

    def __init__(
            self,
            game: Game,
            change_x: int = 1,
            change_y: int = 0,
            color: Colors = Colors.Red
    ) -> None:
        super().__init__((0, 0), game, change_x, change_y, color)

        # the quality of the food
        r = randint(1, 100)
        self.quality = 2 if r < 10 else 1
        if self.quality >= 2:
            self.color = Colors.Gold

        # the random position for the food
        x, y = randint(1, self._game.cols - 2), randint(1, self._game.rows - 2)
        self.pos = (x, y)
