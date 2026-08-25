"""Chess.com game integration."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from ...exceptions import InvalidResponseError, PlayerNotFoundError
from ...models import Leaderboard, LeaderboardEntry, Match, Player, PlayerStats, Rank
from ..base import GameIntegration
from . import endpoints
from .models import ChessComMatchData, ChessComPlayerData, ChessComRatingSummary

_USER_AGENT = "gameapi/0.2.0 (+https://github.com/F0xyN0xy/universal-game-api)"

_TIME_CONTROL_KEYS = {
    "chess_bullet": "bullet",
    "chess_blitz": "blitz",
    "chess_rapid": "rapid",
    "chess_daily": "daily",
}

_PRIMARY_TIME_CONTROL = "chess_rapid"
_DEFAULT_LEADERBOARD_CATEGORY = "live_blitz"


class ChessComIntegration(GameIntegration):
    """Game integration for Chess.com."""

    slug = "chess_com"
    requires_api_key = False
    source_name = "Chess.com Published-Data API"
    source_url = "https://www.chess.com/news/view/published-data-api"

    def _headers(self) -> Dict[str, str]:
        return {"User-Agent": _USER_AGENT, "Accept": "application/json"}

    def get_player(self, identifier: str) -> Player:
        cached = self._cache_get(f"player:{identifier}")
        if cached is not None:
            return cached  # type: ignore[return-value]

        profile = self._fetch_profile(identifier)
        stats = self._fetch_stats(identifier)
        player = self._build_player(identifier, profile, stats)
        self._cache_set(f"player:{identifier}", player, ttl=60)
        return player

    async def get_player_async(self, identifier: str) -> Player:
        cached = self._cache_get(f"player:{identifier}")
        if cached is not None:
            return cached  # type: ignore[return-value]

        profile = await self._fetch_profile_async(identifier)
        stats = await self._fetch_stats_async(identifier)
        player = self._build_player(identifier, profile, stats)
        self._cache_set(f"player:{identifier}", player, ttl=60)
        return player

    def _fetch_profile(self, identifier: str) -> Dict[str, Any]:
        try:
            return self.http.request(
                "GET", endpoints.player_profile_url(identifier), headers=self._headers()
            )
        except InvalidResponseError as exc:
            raise PlayerNotFoundError(self.slug, identifier) from exc

    async def _fetch_profile_async(self, identifier: str) -> Dict[str, Any]:
        try:
            return await self.http.request_async(
                "GET", endpoints.player_profile_url(identifier), headers=self._headers()
            )
        except InvalidResponseError as exc:
            raise PlayerNotFoundError(self.slug, identifier) from exc

    def _fetch_stats(self, identifier: str) -> Dict[str, Any]:
        try:
            return self.http.request(
                "GET", endpoints.player_stats_url(identifier), headers=self._headers()
            )
        except InvalidResponseError:
            return {}

    async def _fetch_stats_async(self, identifier: str) -> Dict[str, Any]:
        try:
            return await self.http.request_async(
                "GET", endpoints.player_stats_url(identifier), headers=self._headers()
            )
        except InvalidResponseError:
            return {}

    def _build_player(
        self, identifier: str, profile: Dict[str, Any], stats: Dict[str, Any]
    ) -> Player:
        ratings: Dict[str, ChessComRatingSummary] = {}
        total_wins = total_losses = total_draws = 0
        has_record = False

        for stats_key, label in _TIME_CONTROL_KEYS.items():
            block = stats.get(stats_key)
            if not block:
                continue
            last = block.get("last", {})
            record = block.get("record", {})
            summary = ChessComRatingSummary(
                rating=last.get("rating"),
                wins=record.get("win"),
                losses=record.get("loss"),
                draws=record.get("draw"),
            )
            ratings[label] = summary
            if record:
                has_record = True
                total_wins += record.get("win", 0) or 0
                total_losses += record.get("loss", 0) or 0
                total_draws += record.get("draw", 0) or 0

        games_played = total_wins + total_losses + total_draws if has_record else None
        win_rate = (total_wins / games_played) if games_played else None

        player_stats = PlayerStats(
            games_played=games_played,
            wins=total_wins if has_record else None,
            losses=total_losses if has_record else None,
            draws=total_draws if has_record else None,
            win_rate=win_rate,
        )

        primary = ratings.get(_TIME_CONTROL_KEYS[_PRIMARY_TIME_CONTROL])
        rank = Rank(
            tier=profile.get("title"),
            rating=primary.rating if primary else None,
            raw={"tactics": stats.get("tactics"), "puzzle_rush": stats.get("puzzle_rush")},
        )

        game_data = ChessComPlayerData(
            title=profile.get("title"),
            country=profile.get("country"),
            followers=profile.get("followers"),
            joined_timestamp=profile.get("joined"),
            league=profile.get("league"),
            ratings=ratings,
            puzzle_rush_best=(stats.get("puzzle_rush", {}) or {})
            .get("best", {})
            .get("score"),
        )

        return Player(
            name=profile.get("username", identifier),
            game=self.slug,
            identifier=identifier,
            stats=player_stats,
            rank=rank,
            game_data=game_data,
            avatar_url=profile.get("avatar"),
        )

    def get_matches(self, identifier: str, limit: int = 20) -> List[Match]:
        archives = self._fetch_archives(identifier)
        games: List[Dict[str, Any]] = []
        for archive_url in reversed(archives):
            if len(games) >= limit:
                break
            payload = self.http.request("GET", archive_url, headers=self._headers())
            games.extend(payload.get("games", []))
        return self._build_matches(identifier, games, limit)

    async def get_matches_async(self, identifier: str, limit: int = 20) -> List[Match]:
        archives = await self._fetch_archives_async(identifier)
        games: List[Dict[str, Any]] = []
        for archive_url in reversed(archives):
            if len(games) >= limit:
                break
            payload = await self.http.request_async("GET", archive_url, headers=self._headers())
            games.extend(payload.get("games", []))
        return self._build_matches(identifier, games, limit)

    def _fetch_archives(self, identifier: str) -> List[str]:
        try:
            payload = self.http.request(
                "GET", endpoints.player_archives_url(identifier), headers=self._headers()
            )
        except InvalidResponseError as exc:
            raise PlayerNotFoundError(self.slug, identifier) from exc
        return payload.get("archives", [])

    async def _fetch_archives_async(self, identifier: str) -> List[str]:
        try:
            payload = await self.http.request_async(
                "GET", endpoints.player_archives_url(identifier), headers=self._headers()
            )
        except InvalidResponseError as exc:
            raise PlayerNotFoundError(self.slug, identifier) from exc
        return payload.get("archives", [])

    def _build_matches(
        self, identifier: str, games: List[Dict[str, Any]], limit: int
    ) -> List[Match]:
        matches: List[Match] = []
        lowered = identifier.lower()
        for raw in reversed(games):
            if len(matches) >= limit:
                break
            white = raw.get("white", {})
            black = raw.get("black", {})
            is_white = white.get("username", "").lower() == lowered
            mine, opponent = (white, black) if is_white else (black, white)

            result = _normalize_result(mine.get("result"))
            played_at = None
            if raw.get("end_time"):
                played_at = datetime.fromtimestamp(raw["end_time"], tz=timezone.utc)

            matches.append(
                Match(
                    id=raw.get("url", ""),
                    game=self.slug,
                    played_at=played_at,
                    result=result,
                    opponent=opponent.get("username"),
                    game_data=ChessComMatchData(
                        time_class=raw.get("time_class"),
                        white=white.get("username"),
                        black=black.get("username"),
                        white_result=white.get("result"),
                        black_result=black.get("result"),
                        pgn_url=raw.get("url"),
                    ),
                )
            )
        return matches

    def get_leaderboard(self, region: Optional[str] = None) -> Leaderboard:
        payload = self.http.request("GET", endpoints.leaderboards_url(), headers=self._headers())
        return self._build_leaderboard(payload, region)

    async def get_leaderboard_async(self, region: Optional[str] = None) -> Leaderboard:
        payload = await self.http.request_async(
            "GET", endpoints.leaderboards_url(), headers=self._headers()
        )
        return self._build_leaderboard(payload, region)

    def _build_leaderboard(self, payload: Dict[str, Any], region: Optional[str]) -> Leaderboard:
        rows = payload.get(_DEFAULT_LEADERBOARD_CATEGORY, [])
        entries = [
            LeaderboardEntry(
                position=row.get("rank", idx + 1),
                name=row.get("username", "unknown"),
                rating=row.get("score"),
            )
            for idx, row in enumerate(rows)
        ]
        return Leaderboard(game=self.slug, entries=entries, region=region)


def _normalize_result(chess_com_result: Optional[str]) -> str:
    if chess_com_result is None:
        return "unknown"
    if chess_com_result == "win":
        return "win"
    if chess_com_result in {
        "agreed", "repetition", "stalemate", "insufficient", "50move", "timevsinsufficient"
    }:
        return "draw"
    return "loss"