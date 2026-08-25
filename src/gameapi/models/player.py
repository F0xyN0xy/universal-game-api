"""The unified Player model."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from .stats import PlayerStats, Rank


@dataclass
class Player:
    """A player profile, normalized across games."""

    name: str
    game: str
    identifier: str
    stats: PlayerStats = field(default_factory=PlayerStats)
    rank: Rank = field(default_factory=Rank)
    game_data: Optional[Any] = None
    avatar_url: Optional[str] = None

    def win_rate_pct(self) -> Optional[float]:
        """Return win rate as a percentage (0-100), or None if unknown."""
        if self.stats.win_rate is None:
            return None
        return round(self.stats.win_rate * 100, 2)
