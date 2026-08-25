# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] — 2026-08-25

### Added
- **Lichess integration** (`lichess` slug) — player profiles and leaderboards via the public Lichess API.
- **`compare_players(game, identifiers)`** — batch-fetch multiple players in one call (sync + async).
- **`game_info(game)`** — introspect integration metadata (slug, auth requirements, source URL).
- **Model helpers**:
  - `Match.is_win`, `Match.is_loss`, `Match.is_draw`
  - `Player.win_rate_pct()` — returns win rate as a 0–100 percentage
  - `Leaderboard.top(n)` — slice the top N entries
- **Live test suite** (`tests/test_live.py`) — run with `pytest -m live` to test against real APIs.
- **Demo project** (`demo-project/`) — CLI tool and Rich dashboard built on top of `gameapi`.
- **Examples** (`examples/`) — `basic_usage.py`, `async_usage.py`, `compare_players.py`.

### Fixed
- **HTTP base headers** — `HTTPClient` now correctly forwards `base_headers` to `httpx.Client` and `httpx.AsyncClient` (fixes missing `User-Agent` on requests).
- **Retry-After handling** — 429 responses now respect the `Retry-After` header instead of always using exponential backoff.
- **Missing import** — `GameAPI.__repr__` now properly imports `supported_games`.
- **Pylance warnings** — guarded `game_data` access in tests to satisfy `reportOptionalMemberAccess`.

### Changed
- Bumped version to `0.1.0`.
- `pyproject.toml` now includes `lichess` in keywords and classifiers.
- `pytest.ini_options` adds a `live` marker for optional live API tests.

### Added
- Initial release with Chess.com integration.
- Unified models: `Player`, `PlayerStats`, `Rank`, `Match`, `Leaderboard`, `LeaderboardEntry`.
- Sync (`GameAPI`) and async (`AsyncGameAPI`) clients.
- In-memory TTL cache (`MemoryCache`).
- Retry logic with exponential backoff for 429/500/502/503/504.
- Exception hierarchy: `GameAPIError`, `PlayerNotFoundError`, `RateLimitError`, etc.
