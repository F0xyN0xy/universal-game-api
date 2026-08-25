"""The synchronous public entry point for gameapi."""

from __future__ import annotations

from typing import List, Optional

from ._base import _BaseGameAPI
from .models import Leaderboard, Match, Player


class GameAPI(_BaseGameAPI):
    """Synchronous client for accessing unified public game data."""

    def player(self, game: str, identifier: str) -> Player:
        """Fetch a unified player profile."""
        return self._resolve(game).get_player(identifier)

    def matches(self, game: str, identifier: str, limit: int = 20) -> List[Match]:
        """Fetch a player's recent matches, most recent first."""
        return self._resolve(game).get_matches(identifier, limit=limit)

    def leaderboard(self, game: str, region: Optional[str] = None) -> Leaderboard:
        """Fetch a game's leaderboard."""
        return self._resolve(game).get_leaderboard(region=region)

    def compare_players(self, game: str, identifiers: List[str]) -> List[Player]:
        """Fetch multiple players at once (synchronous)."""
        integration = self._resolve(game)
        return [integration.get_player(ident) for ident in identifiers]

    def close(self) -> None:
        """Release the underlying HTTP connection pool."""
        self._http.close()

    def __enter__(self) -> "GameAPI":
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.close()

    def __repr__(self) -> str:
        games = supported_games()
        return f"GameAPI(games={games}, cache={self.cache_enabled})"