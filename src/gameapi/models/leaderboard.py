"""The unified Leaderboard model."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class LeaderboardEntry:
    """A single row on a leaderboard."""

    position: int
    name: str
    rating: Optional[float] = None


@dataclass
class Leaderboard:
    """A ranked list of players for a game."""

    game: str
    entries: List[LeaderboardEntry] = field(default_factory=list)
    region: Optional[str] = None

    def __iter__(self):
        return iter(self.entries)

    def __len__(self) -> int:
        return len(self.entries)

    def top(self, n: int) -> List[LeaderboardEntry]:
        """Return the top ``n`` entries."""
        return self.entries[:n]
