from __future__ import annotations

from gameapi import GameAPI, GameNotSupportedError
from gameapi.games.registry import supported_games, register_game, GAME_REGISTRY
from gameapi.games.base import GameIntegration


def test_supported_games_includes_chess_com_and_lichess():
    games = supported_games()
    assert "chess_com" in games
    assert "lichess" in games


def test_game_info():
    api = GameAPI()
    info = api.game_info("chess_com")
    assert info["slug"] == "chess_com"
    assert info["requires_api_key"] is False
    api.close()


def test_game_info_unsupported_raises():
    api = GameAPI()
    with pytest.raises(GameNotSupportedError):
        api.game_info("not_real")
    api.close()


def test_register_game_decorator():
    class FakeIntegration(GameIntegration):
        slug = "fake_game"
        source_name = "Fake"
        source_url = "https://example.com"

        def get_player(self, identifier: str):
            pass

        async def get_player_async(self, identifier: str):
            pass

    register_game(FakeIntegration)
    assert "fake_game" in GAME_REGISTRY
    # cleanup
    del GAME_REGISTRY["fake_game"]


import pytest