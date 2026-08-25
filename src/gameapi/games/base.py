"""Abstract base class every game integration must implement."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional

from ..cache import MemoryCache
from ..http import HTTPClient
from ..models import Leaderboard, Match, Player


class GameIntegration(ABC):
    """Base class for a single game's integration."""

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

    @abstractmethod
    def get_player(self, identifier: str) -> Player:
        """Fetch a player profile synchronously."""

    @abstractmethod
    async def get_player_async(self, identifier: str) -> Player:
        """Fetch a player profile asynchronously."""

    def get_matches(self, identifier: str, limit: int = 20) -> List[Match]:
        raise NotImplementedError(f"'{self.slug}' does not support match history.")

    async def get_matches_async(self, identifier: str, limit: int = 20) -> List[Match]:
        raise NotImplementedError(f"'{self.slug}' does not support match history.")

    def get_leaderboard(self, region: Optional[str] = None) -> Leaderboard:
        raise NotImplementedError(f"'{self.slug}' does not support leaderboards.")

    async def get_leaderboard_async(self, region: Optional[str] = None) -> Leaderboard:
        raise NotImplementedError(f"'{self.slug}' does not support leaderboards.")

    def _cache_get(self, key: str) -> Optional[object]:
        if self.cache is None:
            return None
        return self.cache.get(f"{self.slug}:{key}")

    def _cache_set(self, key: str, value: object, ttl: Optional[float] = None) -> None:
        if self.cache is None:
            return
        self.cache.set(f"{self.slug}:{key}", value, ttl=ttl)