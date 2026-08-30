"""Chess.com-specific data models."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ChessComRatingSummary:
    rating: int | None = None
    wins: int | None = None
    losses: int | None = None
    draws: int | None = None


@dataclass
class ChessComPlayerData:
    title: str | None = None
    country: str | None = None
    followers: int | None = None
    joined_timestamp: int | None = None
    league: str | None = None
    ratings: dict[str, ChessComRatingSummary] = field(default_factory=dict)
    puzzle_rush_best: int | None = None


@dataclass
class ChessComMatchData:
    time_class: str | None = None
    white: str | None = None
    black: str | None = None
    white_result: str | None = None
    black_result: str | None = None
    pgn_url: str | None = None
