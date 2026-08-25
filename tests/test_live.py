"""Optional live integration tests — run with: pytest -m live

These hit real APIs and may fail due to rate limits or network issues.
"""

from __future__ import annotations

import pytest

from gameapi import GameAPI, PlayerNotFoundError


@pytest.mark.live
def test_live_chess_com_player():
    api = GameAPI()
    try:
        player = api.player(game="chess_com", identifier="hikaru")
        assert player.name == "hikaru"
        assert player.game == "chess_com"
    finally:
        api.close()


@pytest.mark.live
def test_live_chess_com_player_not_found():
    api = GameAPI()
    with pytest.raises(PlayerNotFoundError):
        api.player(game="chess_com", identifier="this-user-should-not-exist-xyz123")
    api.close()


@pytest.mark.live
def test_live_lichess_player():
    api = GameAPI()
    try:
        player = api.player(game="lichess", identifier="drnykterstein")
        assert player.name == "DrNykterstein"
    finally:
        api.close()


@pytest.mark.live
def test_live_leaderboards():
    api = GameAPI()
    try:
        board = api.leaderboard(game="chess_com")
        assert len(board) > 0

        board2 = api.leaderboard(game="lichess")
        assert len(board2) > 0
    finally:
        api.close()