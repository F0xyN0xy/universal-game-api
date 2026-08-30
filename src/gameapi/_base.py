"""Shared setup/resolution logic for GameAPI and AsyncGameAPI."""

from __future__ import annotations

import os

from .cache import MemoryCache
from .exceptions import GameNotSupportedError
from .games.base import GameIntegration
from .games.registry import GAME_REGISTRY, supported_games
from .http import HTTPClient

_ENV_API_KEY = "GAMEAPI_API_KEY"


class _BaseGameAPI:
    """Common configuration and integration resolution for both clients."""

    def __init__(
        self,
        api_key: str | None = None,
        cache: bool = False,
        cache_ttl: float = 60.0,
        timeout: float = 10.0,
        max_retries: int = 2,
    ) -> None:
        self.api_key = api_key or os.environ.get(_ENV_API_KEY)
        self.cache_enabled = cache
        self.cache_ttl = cache_ttl

        self._http = HTTPClient(timeout=timeout, max_retries=max_retries)
        self._cache = MemoryCache(default_ttl=cache_ttl) if cache else None
        self._integrations: dict[str, GameIntegration] = {}

    def _resolve(self, game: str) -> GameIntegration:
        integration = self._integrations.get(game)
        if integration is not None:
            return integration

        integration_cls = GAME_REGISTRY.get(game)
        if integration_cls is None:
            raise GameNotSupportedError(game, supported=supported_games())

        integration = integration_cls(self._http, api_key=self.api_key, cache=self._cache)
        self._integrations[game] = integration
        return integration

    def game_info(self, game: str) -> dict[str, str | bool]:
        """Return metadata about a registered integration."""
        integration_cls = GAME_REGISTRY.get(game)
        if integration_cls is None:
            raise GameNotSupportedError(game, supported=supported_games())
        return {
            "slug": integration_cls.slug,
            "requires_api_key": integration_cls.requires_api_key,
            "source_name": integration_cls.source_name,
            "source_url": integration_cls.source_url,
        }
