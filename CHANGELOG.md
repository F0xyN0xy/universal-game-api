# Changelog

All notable changes to this project are documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/).

## [0.1.0] - Unreleased

### Added

- Core `GameAPI` (sync) and `AsyncGameAPI` (async) clients with identical
  interfaces.
- Unified data models: `Player`, `PlayerStats`, `Rank`, `Match`,
  `Leaderboard`, `LeaderboardEntry`.
- Shared HTTP layer (`gameapi.http.HTTPClient`) with timeouts, conservative
  exponential-backoff retries on HTTP 429/500/502/503/504, and consistent
  error translation.
- Custom exception hierarchy rooted at `GameAPIError`: `GameNotSupportedError`,
  `PlayerNotFoundError`, `AuthenticationError`, `RateLimitError`,
  `APIUnavailableError`, `InvalidResponseError`.
- Optional in-process TTL caching (`gameapi.cache.MemoryCache`).
- First game integration: **Chess.com** (`chess_com`), covering player
  profiles, stats, match history, and leaderboards via the free, public
  Chess.com Published-Data API. No API key required.
- Extensible game-integration architecture (`gameapi.games.base.GameIntegration`
  + `gameapi.games.registry`) so new games can be added without touching
  the core client.
- Test suite with mocked HTTP responses (`respx`) covering the HTTP layer,
  cache, exceptions, and the Chess.com integration.
