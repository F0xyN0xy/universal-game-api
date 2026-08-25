"""The synchronous public entry point for gameapi.

Example:
    >>> from gameapi import GameAPI
    >>> api = GameAPI()
    >>> player = api.player(game="chess_com", identifier="hikaru")
    >>> print(player.name, player.rank.rating)
"""

from __future__ import annotations

from typing import List, Optional

from ._base import _BaseGameAPI
from .models import Leaderboard, Match, Player


class GameAPI(_BaseGameAPI):
    """Synchronous client for accessing unified public game data.

    Args:
        api_key: Default API key used by integrations that require one.
            Falls back to the ``GAMEAPI_API_KEY`` environment variable.
        cache: Whether to cache responses in-process to reduce redundant
            requests and help stay within upstream rate limits.
        cache_ttl: Default cache lifetime in seconds (only relevant if
            ``cache=True``).
        timeout: Per-request HTTP timeout in seconds.
        max_retries: Number of retry attempts for transient HTTP failures
            (HTTP 429/500/502/503/504 and network errors).

    Example:
        >>> api = GameAPI(cache=True, cache_ttl=120)
        >>> player = api.player("chess_com", "hikaru")
        >>> matches = api.matches("chess_com", "hikaru", limit=5)
        >>> board = api.leaderboard("chess_com")
    """

    def player(self, game: str, identifier: str) -> Player:
        """Fetch a unified player profile.

        Args:
            game: Game slug, e.g. "chess_com".
            identifier: The player's handle/username for that game.

        Raises:
            GameNotSupportedError: If ``game`` has no registered integration.
            PlayerNotFoundError: If the player doesn't exist for that game.
            AuthenticationError: If the integration requires an API key that
                wasn't provided or was rejected.
            RateLimitError: If the upstream API's rate limit was exceeded.
            APIUnavailableError: If the upstream API is unreachable.
        """
        return self._resolve(game).get_player(identifier)

    def matches(self, game: str, identifier: str, limit: int = 20) -> List[Match]:
        """Fetch a player's recent matches, most recent first.

        Raises:
            NotImplementedError: If the game integration doesn't support
                match history.
            (See :meth:`player` for the other exceptions this can raise.)
        """
        return self._resolve(game).get_matches(identifier, limit=limit)

    def leaderboard(self, game: str, region: Optional[str] = None) -> Leaderboard:
        """Fetch a game's leaderboard.

        Raises:
            NotImplementedError: If the game integration doesn't support
                leaderboards.
            (See :meth:`player` for the other exceptions this can raise.)
        """
        return self._resolve(game).get_leaderboard(region=region)

    def close(self) -> None:
        """Release the underlying HTTP connection pool."""
        self._http.close()

    def __enter__(self) -> "GameAPI":
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.close()
