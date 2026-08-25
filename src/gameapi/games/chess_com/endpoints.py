"""URL builders for the public Chess.com API.

Reference: https://www.chess.com/news/view/published-data-api

The Chess.com published-data API is free and requires no API key, but
Chess.com asks integrators to identify themselves with a descriptive
User-Agent (set by :class:`~gameapi.games.chess_com.client.ChessComIntegration`).
"""

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
