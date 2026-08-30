"""Common statistics and ranking models."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Rank:
    """A player's competitive standing in a game."""

    tier: str | None = None
    rating: float | None = None
    position: int | None = None
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass
class PlayerStats:
    """Common, cross-game player statistics."""

    games_played: int | None = None
    wins: int | None = None
    losses: int | None = None
    draws: int | None = None
    win_rate: float | None = None
