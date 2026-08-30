"""osu! game integration.

Data source: the official osu! API v2 (https://osu.ppy.sh/docs/index.html).

Unlike Chess.com and Lichess, the osu! API requires OAuth2 credentials.
Create a free OAuth application at https://osu.ppy.sh/home/account/edit
(you only need "New OAuth Application" — no redirect URI is used here since
this integration relies on the client-credentials grant, which only ever
grants access to public data). Pass the resulting Client ID and Client
Secret to gameapi as a single ``api_key`` string in the form
``"<client_id>:<client_secret>"``:

    api = GameAPI(api_key="12345:abcDEF123...")
    player = api.player(game="osu", identifier="mrekk")

The client-credentials access token is fetched lazily on first use, cached
in-memory for its lifetime (osu! tokens are valid for 24h), and
transparently refreshed once it expires.

osu! has no head-to-head "match" concept comparable to chess, so
``matches()`` returns the player's recent play history instead, with
``result`` set to ``"win"`` for passed plays and ``"loss"`` for failed ones.
"""

from __future__ import annotations

import time
from datetime import datetime, timezone
from typing import Any

from ...exceptions import AuthenticationError, InvalidResponseError, PlayerNotFoundError
from ...models import Leaderboard, LeaderboardEntry, Match, Player, PlayerStats, Rank
from ..base import GameIntegration
from . import endpoints
from .models import OsuPlayerData, OsuScoreData

_USER_AGENT = "gameapi/0.2.1 (+https://github.com/F0xyN0xy/universal-game-api)"
_TOKEN_EXPIRY_SAFETY_MARGIN = 30  # seconds; refresh a little before actual expiry


class OsuIntegration(GameIntegration):
    """Game integration for osu!."""

    slug = "osu"
    requires_api_key = True
    source_name = "osu! API v2"
    source_url = "https://osu.ppy.sh/docs/index.html"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._access_token: str | None = None
        self._token_expires_at: float = 0.0

    # -- Authentication -----------------------------------------------------

    def _credentials(self) -> tuple[str, str]:
        if not self.api_key or ":" not in self.api_key:
            raise AuthenticationError(
                "osu! requires an OAuth client id and secret. Create one at "
                "https://osu.ppy.sh/home/account/edit and pass it as "
                'api_key="<client_id>:<client_secret>".'
            )
        client_id, _, client_secret = self.api_key.partition(":")
        if not client_id or not client_secret:
            raise AuthenticationError(
                'Malformed osu! api_key. Expected "<client_id>:<client_secret>".'
            )
        return client_id, client_secret

    def _token_headers(self) -> dict[str, str]:
        return {
            "User-Agent": _USER_AGENT,
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    def _token_payload(self) -> dict[str, str]:
        client_id, client_secret = self._credentials()
        return {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "client_credentials",
            "scope": "public",
        }

    def _store_token(self, payload: dict[str, Any]) -> str:
        token: str = payload["access_token"]
        expires_in = payload.get("expires_in", 3600)
        self._access_token = token
        self._token_expires_at = time.time() + expires_in - _TOKEN_EXPIRY_SAFETY_MARGIN
        return token

    def _get_token(self) -> str:
        if self._access_token and time.time() < self._token_expires_at:
            return self._access_token
        payload = self.http.request(
            "POST", endpoints.TOKEN_URL, json=self._token_payload(), headers=self._token_headers()
        )
        return self._store_token(payload)

    async def _get_token_async(self) -> str:
        if self._access_token and time.time() < self._token_expires_at:
            return self._access_token
        payload = await self.http.request_async(
            "POST", endpoints.TOKEN_URL, json=self._token_payload(), headers=self._token_headers()
        )
        return self._store_token(payload)

    def _headers(self, token: str) -> dict[str, str]:
        return {
            "User-Agent": _USER_AGENT,
            "Accept": "application/json",
            "Authorization": f"Bearer {token}",
        }

    # -- Player ---------------------------------------------------------

    def get_player(self, identifier: str) -> Player:
        cached = self._cache_get(f"player:{identifier}")
        if cached is not None:
            return cached  # type: ignore[return-value]

        token = self._get_token()
        data = self._fetch_user(identifier, token)
        player = self._build_player(identifier, data)
        self._cache_set(f"player:{identifier}", player, ttl=60)
        return player

    async def get_player_async(self, identifier: str) -> Player:
        cached = self._cache_get(f"player:{identifier}")
        if cached is not None:
            return cached  # type: ignore[return-value]

        token = await self._get_token_async()
        data = await self._fetch_user_async(identifier, token)
        player = self._build_player(identifier, data)
        self._cache_set(f"player:{identifier}", player, ttl=60)
        return player

    def _fetch_user(self, identifier: str, token: str) -> dict[str, Any]:
        try:
            return self.http.request(
                "GET", endpoints.user_url(identifier), headers=self._headers(token)
            )
        except InvalidResponseError as exc:
            raise PlayerNotFoundError(self.slug, identifier) from exc

    async def _fetch_user_async(self, identifier: str, token: str) -> dict[str, Any]:
        try:
            return await self.http.request_async(
                "GET", endpoints.user_url(identifier), headers=self._headers(token)
            )
        except InvalidResponseError as exc:
            raise PlayerNotFoundError(self.slug, identifier) from exc

    def _build_player(self, identifier: str, data: dict[str, Any]) -> Player:
        stats = data.get("statistics", {}) or {}
        grades = stats.get("grade_counts", {}) or {}
        level = stats.get("level", {}) or {}

        player_stats = PlayerStats(
            games_played=stats.get("play_count"),
            wins=None,
            losses=None,
            draws=None,
            win_rate=None,
        )

        rank = Rank(
            tier=data.get("rank_highest", {}).get("rank") if isinstance(data.get("rank_highest"), dict) else None,
            rating=stats.get("pp"),
            position=stats.get("global_rank"),
            raw={"grade_counts": grades},
        )

        game_data = OsuPlayerData(
            mode=data.get("playmode", endpoints.DEFAULT_MODE),
            country_code=data.get("country_code"),
            global_rank=stats.get("global_rank"),
            country_rank=stats.get("country_rank"),
            hit_accuracy=stats.get("hit_accuracy"),
            play_count=stats.get("play_count"),
            play_time_seconds=stats.get("play_time"),
            ranked_score=stats.get("ranked_score"),
            total_score=stats.get("total_score"),
            level_current=level.get("current"),
            level_progress=level.get("progress"),
            ss_count=(grades.get("ssh", 0) or 0) + (grades.get("ss", 0) or 0),
            s_count=(grades.get("sh", 0) or 0) + (grades.get("s", 0) or 0),
            a_count=grades.get("a"),
            is_supporter=data.get("is_supporter"),
            follower_count=data.get("follower_count"),
        )

        return Player(
            name=data.get("username", identifier),
            game=self.slug,
            identifier=identifier,
            stats=player_stats,
            rank=rank,
            game_data=game_data,
            avatar_url=data.get("avatar_url"),
        )

    # -- Matches (recent play history) -----------------------------------

    def get_matches(self, identifier: str, limit: int = 20) -> list[Match]:
        token = self._get_token()
        user = self._fetch_user(identifier, token)
        scores = self.http.request(
            "GET",
            endpoints.user_scores_url(user["id"], score_type="recent"),
            params={"mode": endpoints.DEFAULT_MODE, "limit": min(limit, 100), "include_fails": 1},
            headers=self._headers(token),
        )
        return self._build_matches(scores, limit) # type: ignore

    async def get_matches_async(self, identifier: str, limit: int = 20) -> list[Match]:
        token = await self._get_token_async()
        user = await self._fetch_user_async(identifier, token)
        scores = await self.http.request_async(
            "GET",
            endpoints.user_scores_url(user["id"], score_type="recent"),
            params={"mode": endpoints.DEFAULT_MODE, "limit": min(limit, 100), "include_fails": 1},
            headers=self._headers(token),
        )
        return self._build_matches(scores, limit) # type: ignore

    def _build_matches(self, scores: list[dict[str, Any]], limit: int) -> list[Match]:
        matches: list[Match] = []
        for raw in scores[:limit]:
            played_at = None
            created_at = raw.get("created_at")
            if created_at:
                played_at = datetime.fromisoformat(created_at.replace("Z", "+00:00")).astimezone(
                    timezone.utc
                )

            beatmapset = raw.get("beatmapset", {}) or {}
            beatmap = raw.get("beatmap", {}) or {}

            matches.append(
                Match(
                    id=str(raw.get("id", "")),
                    game=self.slug,
                    played_at=played_at,
                    result="win" if raw.get("passed") else "loss",
                    opponent=None,
                    game_data=OsuScoreData(
                        beatmap_id=beatmap.get("id"),
                        beatmapset_title=beatmapset.get("title"),
                        beatmapset_artist=beatmapset.get("artist"),
                        difficulty_name=beatmap.get("version"),
                        mode=raw.get("mode"),
                        mods=list(raw.get("mods", []) or []),
                        grade=raw.get("rank"),
                        accuracy=raw.get("accuracy"),
                        pp=raw.get("pp"),
                        max_combo=raw.get("max_combo"),
                        score=raw.get("score") if isinstance(raw.get("score"), int) else raw.get("legacy_total_score"),
                        passed=raw.get("passed"),
                    ),
                )
            )
        return matches

    # -- Leaderboard ------------------------------------------------------

    def get_leaderboard(self, region: str | None = None) -> Leaderboard:
        token = self._get_token()
        params = {"country": region} if region else None
        payload = self.http.request(
            "GET", endpoints.rankings_url(), params=params, headers=self._headers(token)
        )
        return self._build_leaderboard(payload, region)

    async def get_leaderboard_async(self, region: str | None = None) -> Leaderboard:
        token = await self._get_token_async()
        params = {"country": region} if region else None
        payload = await self.http.request_async(
            "GET", endpoints.rankings_url(), params=params, headers=self._headers(token)
        )
        return self._build_leaderboard(payload, region)

    def _build_leaderboard(self, payload: dict[str, Any], region: str | None) -> Leaderboard:
        rows = payload.get("ranking", [])
        entries = [
            LeaderboardEntry(
                position=row.get("global_rank", idx + 1),
                name=(row.get("user") or {}).get("username", "unknown"),
                rating=row.get("pp"),
            )
            for idx, row in enumerate(rows)
        ]
        return Leaderboard(game=self.slug, entries=entries, region=region)