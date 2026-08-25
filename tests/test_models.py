from __future__ import annotations

from dataclasses import asdict

from gameapi.models import Leaderboard, LeaderboardEntry, Match, Player, PlayerStats, Rank


def test_leaderboard_top():
    board = Leaderboard(
        game="chess_com",
        entries=[
            LeaderboardEntry(position=1, name="a", rating=1000),
            LeaderboardEntry(position=2, name="b", rating=900),
            LeaderboardEntry(position=3, name="c", rating=800),
        ],
    )
    assert len(board.top(2)) == 2
    assert board.top(2)[0].name == "a"


def test_match_result_helpers():
    m_win = Match(id="1", game="chess_com", result="win")
    m_loss = Match(id="2", game="chess_com", result="loss")
    m_draw = Match(id="3", game="chess_com", result="draw")

    assert m_win.is_win is True
    assert m_win.is_loss is False
    assert m_loss.is_loss is True
    assert m_draw.is_draw is True


def test_player_win_rate_pct():
    player = Player(
        name="test",
        game="chess_com",
        identifier="test",
        stats=PlayerStats(win_rate=0.7534),
    )
    assert player.win_rate_pct() == 75.34


def test_player_win_rate_pct_none():
    player = Player(name="test", game="chess_com", identifier="test")
    assert player.win_rate_pct() is None


def test_player_asdict_roundtrip():
    player = Player(
        name="test",
        game="chess_com",
        identifier="test",
        rank=Rank(tier="GM", rating=2800),
    )
    d = asdict(player)
    assert d["name"] == "test"
    assert d["rank"]["tier"] == "GM"