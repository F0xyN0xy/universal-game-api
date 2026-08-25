"""Common statistics and ranking models shared across game integrations."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class Rank:
    """A player's competitive standing in a game.

    Different games express rank differently (a numeric rating, a tier name,
    a division, etc.), so all fields are optional. Game integrations should
    populate whichever fields make sense and leave the rest as ``None``.

    Attributes:
        tier: Named tier or division, e.g. "Grand Champion", "Gold".
        rating: Numeric rating/MMR/Elo, if applicable.
        position: Global or regional leaderboard position, if known.
        raw: The unmodified game-specific rank payload, for advanced use.
    """

    tier: Optional[str] = None
    rating: Optional[float] = None
    position: Optional[int] = None
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PlayerStats:
    """Common, cross-game player statistics.

    Only fields that are meaningful for a given game are populated; the rest
    default to ``None``. Game-specific statistics that don't fit this common
    shape belong on ``Player.game_data`` instead.

    Attributes:
        games_played: Total games/matches played, if known.
        wins: Total wins, if known.
        losses: Total losses, if known.
        draws: Total draws/ties, if known.
        win_rate: Win rate as a fraction between 0 and 1, if known.
    """

    games_played: Optional[int] = None
    wins: Optional[int] = None
    losses: Optional[int] = None
    draws: Optional[int] = None
    win_rate: Optional[float] = None
