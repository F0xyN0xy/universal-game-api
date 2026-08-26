"""URL builders for the public osu! API v2."""

from __future__ import annotations

BASE_URL = "https://osu.ppy.sh/api/v2"
TOKEN_URL = "https://osu.ppy.sh/oauth/token"

DEFAULT_MODE = "osu"  # osu! standard. Other modes: taiko, fruits, mania.


def user_url(user: str, mode: str = DEFAULT_MODE) -> str:
    return f"{BASE_URL}/users/{user}/{mode}"


def user_scores_url(user_id: int, score_type: str = "recent") -> str:
    return f"{BASE_URL}/users/{user_id}/scores/{score_type}"


def rankings_url(mode: str = DEFAULT_MODE, ranking_type: str = "performance") -> str:
    return f"{BASE_URL}/rankings/{mode}/{ranking_type}"