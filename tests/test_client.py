from __future__ import annotations

import httpx
import pytest
import respx

from gameapi import AsyncGameAPI, GameAPI, GameNotSupportedError
from gameapi.games.chess_com import endpoints as chess_endpoints


@respx.mock
def test_compare_players(chess_profile, chess_stats):
    respx.get(chess_endpoints.player_profile_url("hikaru")).mock(
        return_value=httpx.Response(200, json=chess_profile)
    )
    respx.get(chess_endpoints.player_stats_url("hikaru")).mock(
        return_value=httpx.Response(200, json=chess_stats)
    )
    respx.get(chess_endpoints.player_profile_url("magnus")).mock(
        return_value=httpx.Response(200, json={**chess_profile, "username": "magnus"})
    )
    respx.get(chess_endpoints.player_stats_url("magnus")).mock(
        return_value=httpx.Response(200, json=chess_stats)
    )

    api = GameAPI()
    players = api.compare_players("chess_com", ["hikaru", "magnus"])
    assert len(players) == 2
    assert players[0].name == "hikaru"
    assert players[1].name == "magnus"
    api.close()


@pytest.mark.asyncio
@respx.mock
async def test_async_compare_players(chess_profile, chess_stats):
    respx.get(chess_endpoints.player_profile_url("hikaru")).mock(
        return_value=httpx.Response(200, json=chess_profile)
    )
    respx.get(chess_endpoints.player_stats_url("hikaru")).mock(
        return_value=httpx.Response(200, json=chess_stats)
    )

    api = AsyncGameAPI()
    players = await api.compare_players("chess_com", ["hikaru"])
    assert len(players) == 1
    await api.aclose()


def test_unsupported_game_raises():
    api = GameAPI()
    with pytest.raises(GameNotSupportedError) as exc_info:
        api.player(game="not_a_real_game", identifier="someone")
    assert "not_a_real_game" in str(exc_info.value)
    api.close()


def test_context_manager_closes():
    with GameAPI() as api:
        assert api is not None


@pytest.mark.asyncio
async def test_async_context_manager_closes():
    async with AsyncGameAPI() as api:
        assert api is not None


def test_repr():
    api = GameAPI()
    assert "GameAPI" in repr(api)
    api.close()