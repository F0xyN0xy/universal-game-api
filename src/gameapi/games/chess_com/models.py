"""Chess.com-specific data that doesn't fit gameapi's common models.

Chess.com tracks separate ratings per time control (bullet/blitz/rapid/daily),
which has no natural equivalent in other games, so it's exposed here rather
than forced into the common :class:`~gameapi.models.Rank` model.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
class ChessComRatingSummary:
    """A single time-control's rating summary (e.g. "chess_blitz").

    Attributes:
        rating: Current rating in this time control.
        wins: Total wins in this time control.
        losses: Total losses in this time control.
        draws: Total draws in this time control.
    """

    rating: Optional[int] = None
    wins: Optional[int] = None
    losses: Optional[int] = None
    draws: Optional[int] = None


@dataclass
class ChessComPlayerData:
    """Chess.com-specific fields for a player, exposed via ``Player.game_data``.

    Attributes:
        title: Chess title, e.g. "GM", "IM", "NM" — ``None`` if untitled.
        country: Country name or code as reported by the Chess.com profile.
        followers: Number of followers on Chess.com.
        joined_timestamp: Unix timestamp of account creation.
        league: Chess.com's internal league name, if any.
        ratings: Per-time-control rating summaries, keyed by time control
            (e.g. "bullet", "blitz", "rapid", "daily").
        puzzle_rush_best: Best Puzzle Rush score, if available.
    """

    title: Optional[str] = None
    country: Optional[str] = None
    followers: Optional[int] = None
    joined_timestamp: Optional[int] = None
    league: Optional[str] = None
    ratings: Dict[str, ChessComRatingSummary] = field(default_factory=dict)
    puzzle_rush_best: Optional[int] = None


@dataclass
class ChessComMatchData:
    """Chess.com-specific fields for a match, exposed via ``Match.game_data``.

    Attributes:
        time_class: "bullet", "blitz", "rapid", or "daily".
        white: Username of the player with the white pieces.
        black: Username of the player with the black pieces.
        white_result: Chess.com's result string for white (e.g. "win",
            "checkmated", "resigned", "timeout", "agreed").
        black_result: Chess.com's result string for black.
        pgn_url: URL to the game on Chess.com.
    """

    time_class: Optional[str] = None
    white: Optional[str] = None
    black: Optional[str] = None
    white_result: Optional[str] = None
    black_result: Optional[str] = None
    pgn_url: Optional[str] = None
