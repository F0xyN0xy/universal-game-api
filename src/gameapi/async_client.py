"""The asynchronous public entry point for gameapi.

Example:
    >>> from gameapi import AsyncGameAPI
    >>> import asyncio
    >>>
    >>> async def main():
    ...     api = AsyncGameAPI()
    ...     player = await api.player(game="chess_com", identifier="hikaru")
    ...     print(player.name, player.rank.rating)
    ...     await api.aclose()
    >>>
    >>> asyncio.run(main())
"""

from __future__ import annotations

from typing import List, Optional

from ._base import _BaseGameAPI
from .models import Leaderboard, Match, Player


class AsyncGameAPI(_BaseGameAPI):
    """Asynchronous client for accessing unified public game data.

    Mirrors :class:`~gameapi.client.GameAPI`'s configuration and method
    signatures exactly — every method is simply ``await``-ed instead.

    Example:
        >>> async with AsyncGameAPI() as api:
        ...     player = await api.player("chess_com", "hikaru")
    """

    async def player(self, game: str, identifier: str) -> Player:
        """Async counterpart to :meth:`GameAPI.player`. Same behavior and errors."""
        return await self._resolve(game).get_player_async(identifier)

    async def matches(self, game: str, identifier: str, limit: int = 20) -> List[Match]:
        """Async counterpart to :meth:`GameAPI.matches`. Same behavior and errors."""
        return await self._resolve(game).get_matches_async(identifier, limit=limit)

    async def leaderboard(self, game: str, region: Optional[str] = None) -> Leaderboard:
        """Async counterpart to :meth:`GameAPI.leaderboard`. Same behavior and errors."""
        return await self._resolve(game).get_leaderboard_async(region=region)

    async def aclose(self) -> None:
        """Release the underlying HTTP connection pool."""
        await self._http.aclose()

    async def __aenter__(self) -> "AsyncGameAPI":
        return self

    async def __aexit__(self, *exc_info: object) -> None:
        await self.aclose()
