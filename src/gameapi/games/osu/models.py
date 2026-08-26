"""osu!-specific data models."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class OsuPlayerData:
    mode: Optional[str] = None
    country_code: Optional[str] = None
    global_rank: Optional[int] = None
    country_rank: Optional[int] = None
    hit_accuracy: Optional[float] = None
    play_count: Optional[int] = None
    play_time_seconds: Optional[int] = None
    ranked_score: Optional[int] = None
    total_score: Optional[int] = None
    level_current: Optional[int] = None
    level_progress: Optional[int] = None
    ss_count: Optional[int] = None
    s_count: Optional[int] = None
    a_count: Optional[int] = None
    is_supporter: Optional[bool] = None
    follower_count: Optional[int] = None


@dataclass
class OsuScoreData:
    beatmap_id: Optional[int] = None
    beatmapset_title: Optional[str] = None
    beatmapset_artist: Optional[str] = None
    difficulty_name: Optional[str] = None
    mode: Optional[str] = None
    mods: List[str] = None  # type: ignore[assignment]
    grade: Optional[str] = None
    accuracy: Optional[float] = None
    pp: Optional[float] = None
    max_combo: Optional[int] = None
    score: Optional[int] = None
    passed: Optional[bool] = None

    def __post_init__(self) -> None:
        if self.mods is None:
            self.mods = []