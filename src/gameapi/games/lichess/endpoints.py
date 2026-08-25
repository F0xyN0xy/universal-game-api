"""URL builders for the public Lichess API."""

from __future__ import annotations

BASE_URL = "https://lichess.org/api"


def user_profile_url(username: str) -> str:
    return f"{BASE_URL}/user/{username}"


def user_rating_history_url(username: str) -> str:
    return f"{BASE_URL}/user/{username}/rating-history"


def user_games_url(username: str) -> str:
    return f"{BASE_URL}/games/user/{username}"


def leaderboard_url(perf_type: str = "blitz", nb: int = 10) -> str:
    return f"{BASE_URL}/player/top/{nb}/{perf_type}"