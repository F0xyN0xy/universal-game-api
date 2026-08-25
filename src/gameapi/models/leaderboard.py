"""The unified Leaderboard model returned by game integrations that expose rankings."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class LeaderboardEntry:
    """A single row on a leaderboard.

    Attributes:
        position: The player's rank position on this leaderboard (1-indexed).
        name: The player's display name/handle.
        rating: The numeric rating/score backing this position, if known.
    """

    position: int
    name: str
    rating: Optional[float] = None


@dataclass
class Leaderboard:
    """A ranked list of players for a game (optionally scoped to a region/mode).

    Attributes:
        game: The game identifier this leaderboard belongs to.
        entries: Ordered leaderboard rows, best rank first.
        region: The region this leaderboard is scoped to, if applicable.
    """

    game: str
    entries: List[LeaderboardEntry] = field(default_factory=list)
    region: Optional[str] = None

    def __iter__(self):
        return iter(self.entries)

    def __len__(self) -> int:
        return len(self.entries)
