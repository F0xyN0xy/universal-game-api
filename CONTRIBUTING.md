# Contributing to gameapi

Thanks for considering a contribution! The most common contribution is a
new game integration, so that's covered in detail below.

## Development setup

```bash
git clone https://github.com/F0xyN0xy/universal-game-api
cd gameapi
pip install -e ".[dev]"
pytest
```

## Adding a new game integration

1. **Confirm there's a legitimate public data source.** Only integrate APIs
   that developers are permitted to access under their terms of service —
   don't scrape sites in ways that violate their terms, and don't bypass
   auth, rate limits, or anti-bot systems. If a game doesn't have a
   suitable public API, don't add a fake/partial integration for it.

2. **Create a new module** under `src/gameapi/games/<your_game>/`:

   ```text
   games/
   └── your_game/
       ├── __init__.py
       ├── client.py      # subclasses GameIntegration
       ├── models.py       # game-specific dataclasses (exposed via game_data)
       └── endpoints.py     # URL builders
   ```

   Use `games/chess_com/` as the reference implementation.

3. **Subclass `GameIntegration`** (`gameapi.games.base.GameIntegration`) and
   implement at minimum `get_player` and `get_player_async`. Implement
   `get_matches`/`get_matches_async` and `get_leaderboard`/
   `get_leaderboard_async` only if the underlying API actually supports
   them — the base class already raises a clear `NotImplementedError`
   otherwise.

   All HTTP calls should go through `self.http` (a shared `HTTPClient`) —
   never call `httpx`/`requests` directly from a game integration. This
   keeps retries, timeouts, and error translation consistent everywhere.

4. **Map the game's data onto the unified models** (`Player`, `PlayerStats`,
   `Rank`, `Match`, `Leaderboard`) wherever a field genuinely corresponds.
   Don't force a field that doesn't generalize — put it on `game_data`
   instead (a dataclass you define in your integration's `models.py`).

5. **Register your integration** in `src/gameapi/games/registry.py`:

   ```python
   from .your_game.client import YourGameIntegration

   GAME_REGISTRY["your_game"] = YourGameIntegration
   ```

6. **Translate errors.** Catch the upstream API's "not found" signal (often
   an HTTP 404) and re-raise it as `PlayerNotFoundError(self.slug, identifier)`
   with useful context. Let other `GameAPIError` subclasses raised by the
   shared `HTTPClient` propagate as-is.

7. **Write tests** in `tests/test_your_game.py` using `respx` to mock HTTP
   responses — don't depend on the live API in the standard test suite.
   See `tests/test_chess_com.py` for the pattern. If you want, add a
   separate integration test (clearly marked) that hits the real API.

8. **Document it** — add a row to the "Supported games" table in
   `README.md`, including the data source, whether auth is required, and
   a link to the upstream API's documentation.

## Code style

- Type hints on all public functions/methods.
- Docstrings on all public classes and methods (Google style, as used
  throughout the codebase).
- Run `ruff check .` and `mypy src/` before submitting.

## Pull requests

- Keep PRs focused — one game integration or one fix per PR.
- Include tests for anything you add or change.
- Update `CHANGELOG.md` under an "Unreleased" heading.
