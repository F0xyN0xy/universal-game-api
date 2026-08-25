from __future__ import annotations

import httpx
import pytest
import respx

from gameapi import (
    AsyncGameAPI,
    GameAPI,
    GameNotSupportedError,
    PlayerNotFoundError,
)
from gameapi.games.chess_com import endpoints


def test_unsupported_game_raises():
    api = GameAPI()
    with pytest.raises(GameNotSupportedError) as exc_info:
        api.player(game="not_a_real_game", identifier="someone")
    assert "not_a_real_game" in str(exc_info.value)
    api.close()


@respx.mock
def test_player_sync(chess_profile, chess_stats):
    respx.get(endpoints.player_profile_url("hikaru")).mock(
        return_value=httpx.Response(200, json=chess_profile)
    )
    respx.get(endpoints.player_stats_url("hikaru")).mock(
        return_value=httpx.Response(200, json=chess_stats)
    )

    api = GameAPI()
    player = api.player(game="chess_com", identifier="hikaru")

    assert player.name == "hikaru"
    assert player.game == "chess_com"
    assert player.rank.tier == "GM"
    assert player.rank.rating == 2800  # chess_rapid is the primary rank source
    assert player.stats.wins == 600  # 100 (rapid) + 500 (blitz)
    assert player.game_data.title == "GM"
    assert player.game_data.ratings["blitz"].rating == 3200
    api.close()


@pytest.mark.asyncio
@respx.mock
async def test_player_async(chess_profile, chess_stats):
    respx.get(endpoints.player_profile_url("hikaru")).mock(
        return_value=httpx.Response(200, json=chess_profile)
    )
    respx.get(endpoints.player_stats_url("hikaru")).mock(
        return_value=httpx.Response(200, json=chess_stats)
    )

    api = AsyncGameAPI()
    player = await api.player(game="chess_com", identifier="hikaru")

    assert player.name == "hikaru"
    assert player.rank.rating == 2800
    await api.aclose()


@respx.mock
def test_player_not_found(chess_stats):
    respx.get(endpoints.player_profile_url("ghost")).mock(return_value=httpx.Response(404))

    api = GameAPI()
    with pytest.raises(PlayerNotFoundError):
        api.player(game="chess_com", identifier="ghost")
    api.close()


@respx.mock
def test_matches(chess_archives, chess_games_page):
    respx.get(endpoints.player_archives_url("hikaru")).mock(
        return_value=httpx.Response(200, json=chess_archives)
    )
    for url in chess_archives["archives"]:
        respx.get(url).mock(return_value=httpx.Response(200, json=chess_games_page))

    api = GameAPI()
    matches = api.matches(game="chess_com", identifier="hikaru", limit=3)

    assert len(matches) == 3
    assert all(m.game == "chess_com" for m in matches)
    assert matches[0].result in {"win", "loss", "draw", "unknown"}
    api.close()


@respx.mock
def test_leaderboard(chess_leaderboards):
    respx.get(endpoints.leaderboards_url()).mock(
        return_value=httpx.Response(200, json=chess_leaderboards)
    )

    api = GameAPI()
    board = api.leaderboard(game="chess_com")

    assert len(board) == 2
    assert board.entries[0].name == "hikaru"
    assert board.entries[0].position == 1
    api.close()


@respx.mock
def test_caching_avoids_second_request(chess_profile, chess_stats):
    profile_route = respx.get(endpoints.player_profile_url("hikaru")).mock(
        return_value=httpx.Response(200, json=chess_profile)
    )
    respx.get(endpoints.player_stats_url("hikaru")).mock(
        return_value=httpx.Response(200, json=chess_stats)
    )

    api = GameAPI(cache=True, cache_ttl=60)
    api.player(game="chess_com", identifier="hikaru")
    api.player(game="chess_com", identifier="hikaru")

    assert profile_route.call_count == 1
    api.close()


def test_context_manager_closes():
    with GameAPI() as api:
        assert api is not None
