"""Abstract base class every game integration must implement.

A game integration is responsible for translating between "the shape of one
game's public API" and gameapi's unified models (:mod:`gameapi.models`). It
should never be called directly by end users — it's reached through
:class:`~gameapi.client.GameAPI` / :class:`~gameapi.async_client.AsyncGameAPI`.

Not every game's public API exposes match history or leaderboards. Rather
than force every integration to implement every method, the base class
provides default implementations that raise ``NotImplementedError`` with a
clear message; integrations override only what the underlying API supports.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional

from ..cache import MemoryCache
from ..http import HTTPClient
from ..models import Leaderboard, Match, Player


class GameIntegration(ABC):
    """Base class for a single game's integration.

    Attributes:
        slug: The short, stable identifier used in ``api.player(game=slug, ...)``.
        requires_api_key: Whether this integration needs an API key to function.
        source_name: Human-readable name of the upstream API/data source.
        source_url: URL documenting the upstream API, for attribution.
    """

    slug: str
    requires_api_key: bool = False
    source_name: str = "unknown"
    source_url: str = ""

    def __init__(
        self,
        http: HTTPClient,
        *,
        api_key: Optional[str] = None,
        cache: Optional[MemoryCache] = None,
    ) -> None:
        self.http = http
        self.api_key = api_key
        self.cache = cache

    # -- required ---------------------------------------------------------------

    @abstractmethod
    def get_player(self, identifier: str) -> Player:
        """Fetch a player profile synchronously. Must be implemented."""

    @abstractmethod
    async def get_player_async(self, identifier: str) -> Player:
        """Fetch a player profile asynchronously. Must be implemented."""

    # -- optional, with sensible defaults ----------------------------------------

    def get_matches(self, identifier: str, limit: int = 20) -> List[Match]:
        """Fetch recent matches synchronously. Override if the API supports it."""
        raise NotImplementedError(f"'{self.slug}' does not support match history.")

    async def get_matches_async(self, identifier: str, limit: int = 20) -> List[Match]:
        """Fetch recent matches asynchronously. Override if the API supports it."""
        raise NotImplementedError(f"'{self.slug}' does not support match history.")

    def get_leaderboard(self, region: Optional[str] = None) -> Leaderboard:
        """Fetch a leaderboard synchronously. Override if the API supports it."""
        raise NotImplementedError(f"'{self.slug}' does not support leaderboards.")

    async def get_leaderboard_async(self, region: Optional[str] = None) -> Leaderboard:
        """Fetch a leaderboard asynchronously. Override if the API supports it."""
        raise NotImplementedError(f"'{self.slug}' does not support leaderboards.")

    # -- helpers for subclasses -------------------------------------------------

    def _cache_get(self, key: str) -> Optional[object]:
        if self.cache is None:
            return None
        return self.cache.get(f"{self.slug}:{key}")

    def _cache_set(self, key: str, value: object, ttl: Optional[float] = None) -> None:
        if self.cache is None:
            return
        self.cache.set(f"{self.slug}:{key}", value, ttl=ttl)
