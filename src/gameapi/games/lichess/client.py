"""Lichess game integration.

Data source: the free, public Lichess API
(https://lichess.org/api). No API key is required.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from ...exceptions import InvalidResponseError, PlayerNotFoundError
from ...models import Leaderboard, LeaderboardEntry, Player, PlayerStats, Rank
from ..base import GameIntegration
from . import endpoints
from .models import LichessPlayerData, LichessRatingSummary

_USER_AGENT = "gameapi/0.2.0 (+https://github.com/F0xyN0xy/universal-game-api)"
_ACCEPT = "application/vnd.lichess.v5+json"


class LichessIntegration(GameIntegration):
    """Game integration for Lichess."""

    slug = "lichess"
    requires_api_key = False
    source_name = "Lichess Public API"
    source_url = "https://lichess.org/api"

    def _headers(self) -> Dict[str, str]:
        return {"User-Agent": _USER_AGENT, "Accept": _ACCEPT}

    def get_player(self, identifier: str) -> Player:
        cached = self._cache_get(f"player:{identifier}")
        if cached is not None:
            return cached  # type: ignore[return-value]

        data = self._fetch_user(identifier)
        player = self._build_player(identifier, data)
        self._cache_set(f"player:{identifier}", player, ttl=60)
        return player

    async def get_player_async(self, identifier: str) -> Player:
        cached = self._cache_get(f"player:{identifier}")
        if cached is not None:
            return cached  # type: ignore[return-value]

        data = await self._fetch_user_async(identifier)
        player = self._build_player(identifier, data)
        self._cache_set(f"player:{identifier}", player, ttl=60)
        return player

    def _fetch_user(self, identifier: str) -> Dict[str, Any]:
        try:
            return self.http.request(
                "GET", endpoints.user_profile_url(identifier), headers=self._headers()
            )
        except InvalidResponseError as exc:
            raise PlayerNotFoundError(self.slug, identifier) from exc

    async def _fetch_user_async(self, identifier: str) -> Dict[str, Any]:
        try:
            return await self.http.request_async(
                "GET", endpoints.user_profile_url(identifier), headers=self._headers()
            )
        except InvalidResponseError as exc:
            raise PlayerNotFoundError(self.slug, identifier) from exc

    def _build_player(self, identifier: str, data: Dict[str, Any]) -> Player:
        perfs = data.get("perfs", {})
        count = data.get("count", {})

        ratings: Dict[str, LichessRatingSummary] = {}
        for perf_name, perf_data in perfs.items():
            if isinstance(perf_data, dict):
                ratings[perf_name] = LichessRatingSummary(
                    rating=perf_data.get("rating"),
                    rd=perf_data.get("rd"),
                    prog=perf_data.get("prog"),
                    games=perf_data.get("games"),
                )

        blitz = perfs.get("blitz", {})
        rating = blitz.get("rating") if isinstance(blitz, dict) else None

        total_games = count.get("all") if isinstance(count, dict) else None
        wins = count.get("win") if isinstance(count, dict) else None
        losses = count.get("loss") if isinstance(count, dict) else None
        draws = count.get("draw") if isinstance(count, dict) else None
        win_rate = (wins / total_games) if total_games and wins is not None else None

        player_stats = PlayerStats(
            games_played=total_games,
            wins=wins,
            losses=losses,
            draws=draws,
            win_rate=win_rate,
        )

        rank = Rank(
            tier=data.get("title"),
            rating=rating,
            position=None,
            raw={"perfs": perfs, "patron": data.get("patron")},
        )

        profile_block = data.get("profile", {}) or {}
        game_data = LichessPlayerData(
            url=data.get("url"),
            playing=data.get("playing"),
            completion_rate=data.get("completionRate"),
            count_all=count.get("all"),
            count_rated=count.get("rated"),
            count_ai=count.get("ai"),
            count_draw=count.get("draw"),
            count_loss=count.get("loss"),
            count_win=count.get("win"),
            play_time_total=data.get("playTime", {}).get("total") if isinstance(data.get("playTime"), dict) else None,
            profile=profile_block if isinstance(profile_block, dict) else {},
            perfs=ratings,
        )

        return Player(
            name=data.get("username", identifier),
            game=self.slug,
            identifier=identifier,
            stats=player_stats,
            rank=rank,
            game_data=game_data,
            avatar_url=None,
        )

    def get_leaderboard(self, region: Optional[str] = None) -> Leaderboard:
        perf = region if region else "blitz"
        payload = self.http.request(
            "GET", endpoints.leaderboard_url(perf_type=perf, nb=10), headers=self._headers()
        )
        return self._build_leaderboard(payload, perf)

    async def get_leaderboard_async(self, region: Optional[str] = None) -> Leaderboard:
        perf = region if region else "blitz"
        payload = await self.http.request_async(
            "GET", endpoints.leaderboard_url(perf_type=perf, nb=10), headers=self._headers()
        )
        return self._build_leaderboard(payload, perf)

    def _build_leaderboard(self, payload: Dict[str, Any], perf: str) -> Leaderboard:
        users = payload.get("users", [])
        entries = [
            LeaderboardEntry(
                position=idx + 1,
                name=user.get("username", "unknown"),
                rating=user.get("perfs", {}).get(perf, {}).get("rating") if isinstance(user.get("perfs"), dict) else None,
            )
            for idx, user in enumerate(users)
        ]
        return Leaderboard(game=self.slug, entries=entries, region=perf)
