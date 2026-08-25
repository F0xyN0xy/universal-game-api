"""The unified Match model returned by game integrations that expose match history."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional


@dataclass
class Match:
    """A single completed match/game, normalized across games.

    Attributes:
        id: A stable identifier for the match, if the source API provides one
            (e.g. a game URL or UUID). May be a URL for some games.
        game: The game identifier this match belongs to.
        played_at: When the match was played, if known.
        result: One of "win", "loss", "draw", or "unknown" from the
            perspective of the queried player.
        opponent: The opponent's name/handle, if known and applicable.
        game_data: Game-specific match details that don't fit the common model.
    """

    id: str
    game: str
    played_at: Optional[datetime] = None
    result: str = "unknown"
    opponent: Optional[str] = None
    game_data: Optional[Any] = field(default=None)
