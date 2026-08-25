"""A minimal, dependency-free in-memory cache with per-entry TTL expiry.

This is intentionally simple: gameapi's caching goal is to avoid hammering
third-party APIs and help developers stay within rate limits, not to be a
general-purpose caching solution. Nothing sensitive (API keys, auth headers)
is ever stored in the cache — only parsed response payloads keyed by request
identity.
"""

from __future__ import annotations

import time
from typing import Any, Dict, Optional, Tuple


class MemoryCache:
    """A simple thread-unsafe, process-local TTL cache.

    Attributes:
        default_ttl: Default time-to-live (seconds) applied when ``set`` is
            called without an explicit ``ttl``.
    """

    def __init__(self, default_ttl: float = 60.0) -> None:
        self.default_ttl = default_ttl
        self._store: Dict[str, Tuple[float, Any]] = {}

    def get(self, key: str) -> Optional[Any]:
        """Return the cached value for ``key``, or ``None`` if missing/expired."""
        entry = self._store.get(key)
        if entry is None:
            return None
        expires_at, value = entry
        if expires_at < time.monotonic():
            del self._store[key]
            return None
        return value

    def set(self, key: str, value: Any, ttl: Optional[float] = None) -> None:
        """Store ``value`` under ``key`` for ``ttl`` seconds (or the default TTL)."""
        effective_ttl = self.default_ttl if ttl is None else ttl
        self._store[key] = (time.monotonic() + effective_ttl, value)

    def clear(self) -> None:
        """Remove all cached entries."""
        self._store.clear()

    def __contains__(self, key: str) -> bool:
        return self.get(key) is not None

    def __len__(self) -> int:
        # Note: does not prune expired entries; use for diagnostics only.
        return len(self._store)
