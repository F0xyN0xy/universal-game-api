"""The unified Leaderboard model."""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass, field


@dataclass
class LeaderboardEntry:
    """A single row on a leaderboard."""

    position: int
    name: str
    rating: float | None = None


@dataclass
class Leaderboard:
    """A ranked list of players for a game."""

    game: str
    entries: list[LeaderboardEntry] = field(default_factory=list)
    region: str | None = None

    def __iter__(self) -> Iterator[LeaderboardEntry]:
        return iter(self.entries)

    def __len__(self) -> int:
        return len(self.entries)

    def top(self, n: int) -> list[LeaderboardEntry]:
        """Return the top ``n`` entries."""
        return self.entries[:n]
