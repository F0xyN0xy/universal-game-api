from __future__ import annotations

import httpx
import pytest
import respx

from gameapi import AsyncGameAPI, GameAPI, PlayerNotFoundError
from gameapi.games.lichess import endpoints as lichess_endpoints


@respx.mock
def test_lichess_player_sync(lichess_user):
    respx.get(lichess_endpoints.user_profile_url("drnykterstein")).mock(
        return_value=httpx.Response(200, json=lichess_user)
    )

    api = GameAPI()
    player = api.player(game="lichess", identifier="drnykterstein")

    assert player.name == "DrNykterstein"
    assert player.rank.tier == "GM"
    assert player.rank.rating == 2800
    assert player.stats.wins == 2500
    api.close()


@respx.mock
def test_lichess_player_not_found():
    respx.get(lichess_endpoints.user_profile_url("ghost")).mock(return_value=httpx.Response(404))

    api = GameAPI()
    with pytest.raises(PlayerNotFoundError):
        api.player(game="lichess", identifier="ghost")
    api.close()


@respx.mock
def test_lichess_leaderboard(lichess_leaderboard):
    respx.get(lichess_endpoints.leaderboard_url("blitz", 10)).mock(
        return_value=httpx.Response(200, json=lichess_leaderboard)
    )

    api = GameAPI()
    board = api.leaderboard(game="lichess")

    assert len(board) == 2
    assert board.entries[0].name == "DrNykterstein"
    api.close()


@pytest.mark.asyncio
@respx.mock
async def test_lichess_player_async(lichess_user):
    respx.get(lichess_endpoints.user_profile_url("drnykterstein")).mock(
        return_value=httpx.Response(200, json=lichess_user)
    )

    api = AsyncGameAPI()
    player = await api.player(game="lichess", identifier="drnykterstein")
    assert player.name == "DrNykterstein"
    await api.aclose()
