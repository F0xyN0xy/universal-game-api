# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] — 2026-08-26

### Added
- **osu! integration** (`osu` slug) — player profiles, recent score history, and leaderboards via the official osu! API v2.
  - Requires OAuth2 credentials (`client_id:client_secret`) passed as `api_key`.
  - Access tokens are fetched lazily, cached in-memory, and auto-refreshed before expiry.
  - `matches()` returns recent play history (passed plays = "win", failed plays = "loss").
  - `leaderboard()` supports optional `region` filtering by country code.
- **`test_osu.py`** — mocked test suite covering player lookup, score history, leaderboard, auth errors, and 404 handling.
- Added `osu` to package keywords and classifiers.

### Changed
- `supported_games()` now returns `['chess_com', 'lichess', 'osu']`.

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
- **CI/CD workflows** (`.github/workflows/`):
  - `ci.yml` — runs the test matrix on push/PR (Python 3.9–3.12).
  - `publish.yml` — builds and publishes to PyPI on GitHub Release (Trusted Publishing / OIDC).
- **Demo project** (`demo-project/`) — CLI tool and Rich dashboard built on top of `gameapi`.
- **Examples** (`examples/`) — `basic_usage.py`, `async_usage.py`, `compare_players.py`.

### Fixed
- **HTTP base headers** — `HTTPClient` now correctly forwards `base_headers` to `httpx.Client` and `httpx.AsyncClient` (fixes missing `User-Agent` on requests).
- **Retry-After handling** — 429 responses now respect the `Retry-After` header instead of always using exponential backoff.
- **Missing import** — `GameAPI.__repr__` now properly imports `supported_games`.
- **Pylance warnings** — guarded `game_data` access in tests to satisfy `reportOptionalMemberAccess`.

### Changed
- `pyproject.toml` now includes `lichess` in keywords and classifiers.
- `pytest.ini_options` adds a `live` marker for optional live API tests.

## [0.0.1] — 2026-08-25

### Added
- Initial release with **Chess.com integration** (`chess_com` slug).
- Unified models: `Player`, `PlayerStats`, `Rank`, `Match`, `Leaderboard`, `LeaderboardEntry`.
- Sync (`GameAPI`) and async (`AsyncGameAPI`) clients with identical method signatures.
- In-memory TTL cache (`MemoryCache`) for parsed response data.
- Retry logic with exponential backoff for transient HTTP failures (429/500/502/503/504).
- Exception hierarchy: `GameAPIError`, `PlayerNotFoundError`, `RateLimitError`, `AuthenticationError`, `APIUnavailableError`, `InvalidResponseError`.
