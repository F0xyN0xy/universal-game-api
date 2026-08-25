"""Lichess-specific data models."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
class LichessRatingSummary:
    rating: Optional[int] = None
    rd: Optional[int] = None
    prog: Optional[int] = None
    games: Optional[int] = None


@dataclass
class LichessPlayerData:
    url: Optional[str] = None
    playing: Optional[str] = None
    completion_rate: Optional[int] = None
    count_all: Optional[int] = None
    count_rated: Optional[int] = None
    count_ai: Optional[int] = None
    count_draw: Optional[int] = None
    count_loss: Optional[int] = None
    count_win: Optional[int] = None
    play_time_total: Optional[int] = None
    profile: Dict[str, str] = field(default_factory=dict)
    perfs: Dict[str, LichessRatingSummary] = field(default_factory=dict)


@dataclass
class LichessMatchData:
    speed: Optional[str] = None
    perf: Optional[str] = None
    rated: Optional[bool] = None
    status: Optional[str] = None
    winner: Optional[str] = None
    color: Optional[str] = None
    opening: Optional[str] = None