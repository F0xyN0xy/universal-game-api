"""The unified Match model."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional


@dataclass
class Match:
    """A single completed match/game, normalized across games."""

    id: str
    game: str
    played_at: Optional[datetime] = None
    result: str = "unknown"
    opponent: Optional[str] = None
    game_data: Optional[Any] = field(default=None)

    @property
    def is_win(self) -> bool:
        return self.result == "win"

    @property
    def is_loss(self) -> bool:
        return self.result == "loss"

    @property
    def is_draw(self) -> bool:
        return self.result == "draw"