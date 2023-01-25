from __future__ import annotations

from enum import Enum

__all__ = (
    'GameMode'
)

class GameMode(Enum):
    Hard = 0.1
    Default = 0.2
    Easy = 0.3

class Colors(Enum):
    White = (255, 255, 255)
    Green = (0, 225, 0)
    Red = (225, 0, 0)
    Black = (0, 0, 0)
    Gold = (255, 215, 0)
    Pink = (255, 20, 147)
