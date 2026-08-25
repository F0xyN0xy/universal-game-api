"""Common statistics and ranking models."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class Rank:
    """A player's competitive standing in a game."""

    tier: Optional[str] = None
    rating: Optional[float] = None
    position: Optional[int] = None
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PlayerStats:
    """Common, cross-game player statistics."""

    games_played: Optional[int] = None
    wins: Optional[int] = None
    losses: Optional[int] = None
    draws: Optional[int] = None
    win_rate: Optional[float] = None