from __future__ import annotations

import pytest

from gameapi.exceptions import (
    AuthenticationError,
    GameAPIError,
    GameNotSupportedError,
    PlayerNotFoundError,
    RateLimitError,
)


def test_all_exceptions_are_game_api_error():
    assert issubclass(GameNotSupportedError, GameAPIError)
    assert issubclass(PlayerNotFoundError, GameAPIError)
    assert issubclass(AuthenticationError, GameAPIError)
    assert issubclass(RateLimitError, GameAPIError)


def test_rate_limit_error_exposes_retry_after():
    err = RateLimitError("slow down", retry_after=12.5)
    assert err.retry_after == 12.5
    assert "slow down" in str(err)


def test_player_not_found_message_includes_context():
    err = PlayerNotFoundError("chess_com", "ghost")
    assert "ghost" in str(err)
    assert "chess_com" in str(err)


def test_game_not_supported_lists_supported_games():
    err = GameNotSupportedError("foo", supported=["chess_com", "minecraft"])
    assert "foo" in str(err)
    assert "chess_com" in str(err)
    assert "minecraft" in str(err)


def test_catch_as_base_class():
    with pytest.raises(GameAPIError):
        raise PlayerNotFoundError("chess_com", "ghost")
