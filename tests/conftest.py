"""Shared pytest fixtures."""

from __future__ import annotations

import pytest

CHESS_PROFILE = {
    "username": "hikaru",
    "player_id": 15448422,
    "title": "GM",
    "status": "premium",
    "avatar": "https://images.chesscomfiles.com/uploads/v1/user/15448422.jpg",
    "country": "https://api.chess.com/pub/country/US",
    "followers": 1000000,
    "joined": 1389043258,
    "league": "Legend",
}

CHESS_STATS = {
    "chess_rapid": {
        "last": {"rating": 2800, "date": 1700000000, "rd": 30},
        "best": {"rating": 2850, "date": 1690000000},
        "record": {"win": 100, "loss": 20, "draw": 10},
    },
    "chess_blitz": {
        "last": {"rating": 3200, "date": 1700000000, "rd": 30},
        "record": {"win": 500, "loss": 100, "draw": 50},
    },
    "tactics": {"highest": {"rating": 3000}},
    "puzzle_rush": {"best": {"score": 80}},
}

CHESS_ARCHIVES = {
    "archives": [
        "https://api.chess.com/pub/player/hikaru/games/2024/01",
        "https://api.chess.com/pub/player/hikaru/games/2024/02",
    ]
}

CHESS_GAMES_PAGE = {
    "games": [
        {
            "url": "https://www.chess.com/game/live/1",
            "time_class": "blitz",
            "end_time": 1706000000,
            "white": {"username": "hikaru", "result": "win"},
            "black": {"username": "opponent1", "result": "checkmated"},
        },
        {
            "url": "https://www.chess.com/game/live/2",
            "time_class": "blitz",
            "end_time": 1706003600,
            "white": {"username": "opponent2", "result": "resigned"},
            "black": {"username": "hikaru", "result": "win"},
        },
    ]
}

CHESS_LEADERBOARDS = {
    "live_blitz": [
        {"rank": 1, "username": "hikaru", "score": 3200},
        {"rank": 2, "username": "magnus", "score": 3150},
    ]
}

LICHESS_USER = {
    "id": "drnykterstein",
    "username": "DrNykterstein",
    "title": "GM",
    "perfs": {
        "blitz": {"games": 1234, "rating": 2800, "rd": 50, "prog": 10},
        "bullet": {"games": 500, "rating": 2900, "rd": 45, "prog": -5},
    },
    "count": {"all": 5000, "rated": 4000, "win": 2500, "loss": 1500, "draw": 1000, "ai": 0},
    "playTime": {"total": 360000},
    "profile": {"country": "NO", "location": "Oslo"},
}

LICHESS_LEADERBOARD = {
    "users": [
        {"username": "DrNykterstein", "perfs": {"blitz": {"rating": 2800}}},
        {"username": "penguingm1", "perfs": {"blitz": {"rating": 2750}}},
    ]
}


@pytest.fixture
def chess_profile():
    return dict(CHESS_PROFILE)


@pytest.fixture
def chess_stats():
    return dict(CHESS_STATS)


@pytest.fixture
def chess_archives():
    return dict(CHESS_ARCHIVES)


@pytest.fixture
def chess_games_page():
    return dict(CHESS_GAMES_PAGE)


@pytest.fixture
def chess_leaderboards():
    return dict(CHESS_LEADERBOARDS)


@pytest.fixture
def lichess_user():
    return dict(LICHESS_USER)


@pytest.fixture
def lichess_leaderboard():
    return dict(LICHESS_LEADERBOARD)


OSU_TOKEN = {
    "token_type": "Bearer",
    "expires_in": 86400,
    "access_token": "test-access-token",
}

OSU_USER = {
    "id": 7562902,
    "username": "mrekk",
    "avatar_url": "https://a.ppy.sh/7562902",
    "country_code": "AU",
    "playmode": "osu",
    "is_supporter": True,
    "follower_count": 50000,
    "statistics": {
        "pp": 18000.5,
        "global_rank": 1,
        "country_rank": 1,
        "hit_accuracy": 99.1,
        "play_count": 200000,
        "play_time": 12000000,
        "ranked_score": 90000000000,
        "total_score": 200000000000,
        "level": {"current": 107, "progress": 42},
        "grade_counts": {"ssh": 100, "ss": 200, "sh": 500, "s": 1500, "a": 3000},
    },
}

OSU_RECENT_SCORES = [
    {
        "id": 123456789,
        "mode": "osu",
        "passed": True,
        "accuracy": 0.9987,
        "pp": 320.5,
        "max_combo": 1500,
        "score": 950000,
        "rank": "S",
        "mods": ["HD", "DT"],
        "created_at": "2026-08-20T12:34:56+00:00",
        "beatmap": {"id": 111, "version": "Insane"},
        "beatmapset": {"title": "Some Song", "artist": "Some Artist"},
    }
]

OSU_RANKINGS = {
    "ranking": [
        {"global_rank": 1, "pp": 18000.5, "user": {"username": "mrekk"}},
        {"global_rank": 2, "pp": 17500.0, "user": {"username": "WhiteCat"}},
    ]
}


@pytest.fixture
def osu_token():
    return dict(OSU_TOKEN)


@pytest.fixture
def osu_user():
    return dict(OSU_USER)


@pytest.fixture
def osu_recent_scores():
    return [dict(score) for score in OSU_RECENT_SCORES]


@pytest.fixture
def osu_rankings():
    return dict(OSU_RANKINGS)