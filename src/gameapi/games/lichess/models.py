"""Lichess-specific data models."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class LichessRatingSummary:
    rating: int | None = None
    rd: int | None = None
    prog: int | None = None
    games: int | None = None


@dataclass
class LichessPlayerData:
    url: str | None = None
    playing: str | None = None
    completion_rate: int | None = None
    count_all: int | None = None
    count_rated: int | None = None
    count_ai: int | None = None
    count_draw: int | None = None
    count_loss: int | None = None
    count_win: int | None = None
    play_time_total: int | None = None
    profile: dict[str, str] = field(default_factory=dict)
    perfs: dict[str, LichessRatingSummary] = field(default_factory=dict)


@dataclass
class LichessMatchData:
    speed: str | None = None
    perf: str | None = None
    rated: bool | None = None
    status: str | None = None
    winner: str | None = None
    color: str | None = None
    opening: str | None = None
