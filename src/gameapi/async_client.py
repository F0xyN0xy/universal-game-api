"""The asynchronous public entry point for gameapi."""

from __future__ import annotations

from typing_extensions import Self

from ._base import _BaseGameAPI
from .games.registry import supported_games
from .models import Leaderboard, Match, Player


class AsyncGameAPI(_BaseGameAPI):
    """Asynchronous client for accessing unified public game data."""

    async def player(self, game: str, identifier: str) -> Player:
        return await self._resolve(game).get_player_async(identifier)

    async def matches(self, game: str, identifier: str, limit: int = 20) -> list[Match]:
        return await self._resolve(game).get_matches_async(identifier, limit=limit)

    async def leaderboard(self, game: str, region: str | None = None) -> Leaderboard:
        return await self._resolve(game).get_leaderboard_async(region=region)

    async def compare_players(self, game: str, identifiers: list[str]) -> list[Player]:
        """Fetch multiple players concurrently."""
        integration = self._resolve(game)
        return [await integration.get_player_async(ident) for ident in identifiers]

    async def aclose(self) -> None:
        """Release the underlying HTTP connection pool."""
        await self._http.aclose()

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, *exc_info: object) -> None:
        await self.aclose()

    def __repr__(self) -> str:
        return f"AsyncGameAPI(games={supported_games()}, cache={self.cache_enabled})"
