from __future__ import annotations

from enum import Enum

__all__ = (
    'GameMode'
)

class GameMode(Enum):
    Hard = 0.1
    Default = 0.2
    Easy = 0.3