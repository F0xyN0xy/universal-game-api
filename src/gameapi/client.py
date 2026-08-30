"""The synchronous public entry point for gameapi."""

from __future__ import annotations

from typing_extensions import Self

from ._base import _BaseGameAPI
from .games.registry import supported_games
from .models import Leaderboard, Match, Player


class GameAPI(_BaseGameAPI):
    """Synchronous client for accessing unified public game data."""

    def player(self, game: str, identifier: str) -> Player:
        """Fetch a unified player profile."""
        return self._resolve(game).get_player(identifier)

    def matches(self, game: str, identifier: str, limit: int = 20) -> list[Match]:
        """Fetch a player's recent matches, most recent first."""
        return self._resolve(game).get_matches(identifier, limit=limit)

    def leaderboard(self, game: str, region: str | None = None) -> Leaderboard:
        """Fetch a game's leaderboard."""
        return self._resolve(game).get_leaderboard(region=region)

    def compare_players(self, game: str, identifiers: list[str]) -> list[Player]:
        """Fetch multiple players at once (synchronous)."""
        integration = self._resolve(game)
        return [integration.get_player(ident) for ident in identifiers]

    def close(self) -> None:
        """Release the underlying HTTP connection pool."""
        self._http.close()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.close()

    def __repr__(self) -> str:
        return f"GameAPI(games={supported_games()}, cache={self.cache_enabled})"
