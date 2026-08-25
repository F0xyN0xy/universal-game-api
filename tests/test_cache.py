from __future__ import annotations

import time

from gameapi.cache import MemoryCache


def test_set_and_get():
    cache = MemoryCache(default_ttl=60)
    cache.set("key", "value")
    assert cache.get("key") == "value"


def test_missing_key_returns_none():
    cache = MemoryCache()
    assert cache.get("missing") is None


def test_expired_entry_returns_none():
    cache = MemoryCache()
    cache.set("key", "value", ttl=0.01)
    time.sleep(0.05)
    assert cache.get("key") is None


def test_clear_removes_everything():
    cache = MemoryCache()
    cache.set("a", 1)
    cache.set("b", 2)
    cache.clear()
    assert cache.get("a") is None
    assert cache.get("b") is None


def test_contains():
    cache = MemoryCache()
    cache.set("key", "value")
    assert "key" in cache
    assert "other" not in cache


def test_default_ttl_used_when_not_specified():
    cache = MemoryCache(default_ttl=0.01)
    cache.set("x", 1)
    time.sleep(0.05)
    assert cache.get("x") is None


def test_custom_ttl_overrides_default():
    cache = MemoryCache(default_ttl=0.01)
    cache.set("x", 1, ttl=60)
    time.sleep(0.05)
    assert cache.get("x") == 1
