"""Universal Game API — a unified, developer-friendly interface for public
game data and statistics.

Quick start:

    >>> from gameapi import GameAPI
    >>> api = GameAPI()
    >>> player = api.player(game="chess_com", identifier="hikaru")
    >>> print(player.name, player.stats)

See the README for the full guide, supported games, and async usage.
"""

from .async_client import AsyncGameAPI
from .client import GameAPI
from .exceptions import (
    APIUnavailableError,
    AuthenticationError,
    GameAPIError,
    GameNotSupportedError,
    InvalidResponseError,
    PlayerNotFoundError,
    RateLimitError,
)
from .games.registry import supported_games
from .models import Leaderboard, LeaderboardEntry, Match, Player, PlayerStats, Rank

__version__ = "0.2.0"

__all__ = [
    "GameAPI",
    "AsyncGameAPI",
    "Player",
    "PlayerStats",
    "Rank",
    "Match",
    "Leaderboard",
    "LeaderboardEntry",
    "GameAPIError",
    "GameNotSupportedError",
    "PlayerNotFoundError",
    "AuthenticationError",
    "RateLimitError",
    "APIUnavailableError",
    "InvalidResponseError",
    "supported_games",
    "__version__",
]
