"""The unified Match model."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class Match:
    """A single completed match/game, normalized across games."""

    id: str
    game: str
    played_at: datetime | None = None
    result: str = "unknown"
    opponent: str | None = None
    game_data: Any | None = field(default=None)

    @property
    def is_win(self) -> bool:
        return self.result == "win"

    @property
    def is_loss(self) -> bool:
        return self.result == "loss"

    @property
    def is_draw(self) -> bool:
        return self.result == "draw"
