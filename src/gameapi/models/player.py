"""The unified Player model returned by every game integration."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from .stats import PlayerStats, Rank


@dataclass
class Player:
    """A player profile, normalized across games.

    ``name``, ``game``, ``stats``, and ``rank`` are common fields every
    integration attempts to populate. Anything that doesn't fit the common
    model lives on ``game_data``, which is a game-specific dataclass (see
    each game's ``models.py``, e.g. ``games.chess_com.models.ChessComPlayerData``).

    Attributes:
        name: The player's display name or handle.
        game: The game identifier this profile belongs to, e.g. "chess_com".
        identifier: The original identifier used to look up this player.
        stats: Common cross-game statistics.
        rank: Common cross-game rank/rating information.
        game_data: Game-specific data that has no cross-game equivalent.
        avatar_url: URL to the player's avatar/profile picture, if available.
    """

    name: str
    game: str
    identifier: str
    stats: PlayerStats = field(default_factory=PlayerStats)
    rank: Rank = field(default_factory=Rank)
    game_data: Optional[Any] = None
    avatar_url: Optional[str] = None
