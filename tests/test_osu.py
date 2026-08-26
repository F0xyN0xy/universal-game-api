from __future__ import annotations

import httpx
import pytest
import respx

from gameapi import AsyncGameAPI, AuthenticationError, GameAPI, PlayerNotFoundError
from gameapi.games.osu import endpoints as osu_endpoints


def _mock_token(osu_token):
    respx.post(osu_endpoints.TOKEN_URL).mock(return_value=httpx.Response(200, json=osu_token))


def test_osu_missing_api_key_raises():
    api = GameAPI()
    with pytest.raises(AuthenticationError):
        api.player(game="osu", identifier="mrekk")
    api.close()


@respx.mock
def test_osu_player_sync(osu_token, osu_user):
    _mock_token(osu_token)
    respx.get(osu_endpoints.user_url("mrekk")).mock(return_value=httpx.Response(200, json=osu_user))

    api = GameAPI(api_key="1234:secret")
    player = api.player(game="osu", identifier="mrekk")

    assert player.name == "mrekk"
    assert player.rank.rating == 18000.5
    assert player.rank.position == 1
    assert player.stats.games_played == 200000
    assert player.game_data is not None
    assert player.game_data.country_code == "AU"
    assert player.game_data.ss_count == 300
    api.close()


@respx.mock
def test_osu_player_not_found(osu_token):
    _mock_token(osu_token)
    respx.get(osu_endpoints.user_url("ghost")).mock(return_value=httpx.Response(404))

    api = GameAPI(api_key="1234:secret")
    with pytest.raises(PlayerNotFoundError):
        api.player(game="osu", identifier="ghost")
    api.close()


@respx.mock
def test_osu_matches(osu_token, osu_user, osu_recent_scores):
    _mock_token(osu_token)
    respx.get(osu_endpoints.user_url("mrekk")).mock(return_value=httpx.Response(200, json=osu_user))
    respx.get(osu_endpoints.user_scores_url(osu_user["id"], "recent")).mock(
        return_value=httpx.Response(200, json=osu_recent_scores)
    )

    api = GameAPI(api_key="1234:secret")
    matches = api.matches(game="osu", identifier="mrekk", limit=5)

    assert len(matches) == 1
    assert matches[0].result == "win"
    assert matches[0].game_data.beatmapset_title == "Some Song" # type: ignore
    api.close()


@respx.mock
def test_osu_leaderboard(osu_token, osu_rankings):
    _mock_token(osu_token)
    respx.get(osu_endpoints.rankings_url()).mock(return_value=httpx.Response(200, json=osu_rankings))

    api = GameAPI(api_key="1234:secret")
    board = api.leaderboard(game="osu")

    assert len(board) == 2
    assert board.entries[0].name == "mrekk"
    api.close()


@respx.mock
def test_osu_token_is_reused(osu_token, osu_user):
    token_route = respx.post(osu_endpoints.TOKEN_URL).mock(
        return_value=httpx.Response(200, json=osu_token)
    )
    respx.get(osu_endpoints.user_url("mrekk")).mock(return_value=httpx.Response(200, json=osu_user))

    api = GameAPI(api_key="1234:secret")
    api.player(game="osu", identifier="mrekk")
    api.player(game="osu", identifier="mrekk")

    # Second player() call hits the cache, but even without the cache the
    # token itself should only be fetched once per integration instance.
    assert token_route.call_count == 1
    api.close()


@pytest.mark.asyncio
@respx.mock
async def test_osu_player_async(osu_token, osu_user):
    _mock_token(osu_token)
    respx.get(osu_endpoints.user_url("mrekk")).mock(return_value=httpx.Response(200, json=osu_user))

    api = AsyncGameAPI(api_key="1234:secret")
    player = await api.player(game="osu", identifier="mrekk")
    assert player.name == "mrekk"
    await api.aclose()