"""URL builders for the public Chess.com API."""

from __future__ import annotations

BASE_URL = "https://api.chess.com/pub"


def player_profile_url(username: str) -> str:
    return f"{BASE_URL}/player/{username.lower()}"


def player_stats_url(username: str) -> str:
    return f"{BASE_URL}/player/{username.lower()}/stats"


def player_archives_url(username: str) -> str:
    return f"{BASE_URL}/player/{username.lower()}/games/archives"


def leaderboards_url() -> str:
    return f"{BASE_URL}/leaderboards"
