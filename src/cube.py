from __future__ import annotations

import pygame
from typing import TYPE_CHECKING, Tuple
from enums import Colors

__all__ = (
    'Cube'
)

if TYPE_CHECKING:
    from main import Game
    from pygame import Surface


class Cube:
    """
    Represents a PyGame Cube.
    """

    __slots__ = (
        '_game',
        'pos',
        'change_x',
        'change_y',
        'color'
    )

    def __init__(
            self,
            start: Tuple[int],
            game: Game,
            change_x: int = 1,
            change_y: int = 0,
            color: Colors = Colors.Green
    ) -> None:
        self._game: Game = game
        self.pos: Tuple[int] = start  # [x, y]
        self.change_x: int = change_x
        self.change_y: int = change_y
        self.color: Colors = color

    def __repr__(self) -> str:
        return "<Cube pos_x={} pos_y={}".format(self.pos_x, self.pos_y)

    @property
    def pos_x(self) -> int:
        return self.pos[0]

    @property
    def pos_y(self) -> int:
        return self.pos[1]

    def move(self, change_x: int, change_y: int) -> None:
        """
        Moves the Cube with the given Parameters.

        Parameters
        -----------
        change_x: :class:`ìnt`
            The Change for x position.
        change_y: :class:`int`
            The Change for y position.
        """
        self.change_x, self.change_y = change_x, change_y
        # changes the position with the change parameters
        self.pos = (self.pos[0] + self.change_x, self.pos[1] + self.change_y)

    def draw(self) -> None:
        """
        Draws the cube to PyGame.

        """
        x, y = self.pos
        width = self._game.cell_width
        height = self._game.cell_height

        pygame.draw.rect(self._game.surface, self.color.value, (x * height + 1, y * width + 1, height - 1, width - 1))
