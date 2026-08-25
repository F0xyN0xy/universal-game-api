"""Chess.com-specific data models."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
class ChessComRatingSummary:
    rating: Optional[int] = None
    wins: Optional[int] = None
    losses: Optional[int] = None
    draws: Optional[int] = None


@dataclass
class ChessComPlayerData:
    title: Optional[str] = None
    country: Optional[str] = None
    followers: Optional[int] = None
    joined_timestamp: Optional[int] = None
    league: Optional[str] = None
    ratings: Dict[str, ChessComRatingSummary] = field(default_factory=dict)
    puzzle_rush_best: Optional[int] = None


@dataclass
class ChessComMatchData:
    time_class: Optional[str] = None
    white: Optional[str] = None
    black: Optional[str] = None
    white_result: Optional[str] = None
    black_result: Optional[str] = None
    pgn_url: Optional[str] = None
