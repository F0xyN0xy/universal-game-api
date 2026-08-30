"""osu!-specific data models."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class OsuPlayerData:
    mode: str | None = None
    country_code: str | None = None
    global_rank: int | None = None
    country_rank: int | None = None
    hit_accuracy: float | None = None
    play_count: int | None = None
    play_time_seconds: int | None = None
    ranked_score: int | None = None
    total_score: int | None = None
    level_current: int | None = None
    level_progress: int | None = None
    ss_count: int | None = None
    s_count: int | None = None
    a_count: int | None = None
    is_supporter: bool | None = None
    follower_count: int | None = None


@dataclass
class OsuScoreData:
    beatmap_id: int | None = None
    beatmapset_title: str | None = None
    beatmapset_artist: str | None = None
    difficulty_name: str | None = None
    mode: str | None = None
    mods: list[str] = None  # type: ignore[assignment]
    grade: str | None = None
    accuracy: float | None = None
    pp: float | None = None
    max_combo: int | None = None
    score: int | None = None
    passed: bool | None = None

    def __post_init__(self) -> None:
        if self.mods is None:
            self.mods = []