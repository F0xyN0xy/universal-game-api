# Universal Game API (`gameapi`)

A simple, consistent, developer-friendly Python interface for public game
data and statistics. `gameapi` hides the quirks of individual game APIs
behind one unified interface, so you don't have to learn a new client
library for every game.

```bash
pip install gameapi
```

```python
from gameapi import GameAPI

api = GameAPI()

player = api.player(game="chess_com", identifier="hikaru")

print(player.name)        # "hikaru"
print(player.rank.tier)   # "GM"
print(player.rank.rating) # 2800
print(player.stats)       # PlayerStats(games_played=..., wins=..., ...)
```

## Why

Every game API looks different:

```python
# Without gameapi
chess_client.get_profile(...)
rl_client.fetch_stats(...)
mc_client.player_lookup(...)
```

`gameapi` gives you one shape instead:

```python
# With gameapi
api.player(game="chess_com", identifier="...")
api.player(game="rocket_league", identifier="...")   # once implemented
api.player(game="minecraft", identifier="...")        # once implemented
```

Common fields (`name`, `stats`, `rank`) are normalized across every game.
Anything that doesn't generalize (Chess.com's per-time-control ratings,
Rocket League's MMR playlists, etc.) is still available on
`player.game_data`, un-flattened.

## Installation

```bash
pip install gameapi
```

Requires Python 3.9+.

## Quick start

```python
from gameapi import GameAPI

api = GameAPI()

# Player profile
player = api.player(game="chess_com", identifier="hikaru")
print(player.name, player.rank.rating)

# Recent matches
for match in api.matches(game="chess_com", identifier="hikaru", limit=10):
    print(match.result, match.opponent, match.played_at)

# Leaderboard
for entry in api.leaderboard(game="chess_com"):
    print(entry.position, entry.name, entry.rating)

api.close()  # or use `with GameAPI() as api: ...`
```

### Async

Every method has an async equivalent, with the exact same signatures:

```python
import asyncio
from gameapi import AsyncGameAPI

async def main():
    async with AsyncGameAPI() as api:
        player = await api.player(game="chess_com", identifier="hikaru")
        print(player.name)

asyncio.run(main())
```

## Supported games

| Game | Slug | Auth required | Data source |
|---|---|---|---|
| Chess.com | `chess_com` | No | [Chess.com Published-Data API](https://www.chess.com/news/view/published-data-api) |

More games are added as reliable, legally usable public data sources are
identified for them — see [CONTRIBUTING.md](CONTRIBUTING.md) for how to add
one. `gameapi` intentionally does not fake support for a game that has no
suitable public API.

```python
from gameapi import supported_games
print(supported_games())  # ['chess_com']
```

## Authentication

Games that require an API key accept one directly:

```python
api = GameAPI(api_key="YOUR_API_KEY")
```

or via the `GAMEAPI_API_KEY` environment variable. Keys are never logged
and never hard-coded into the library. (Chess.com's public API needs no key
at all.)

## Caching

Optional in-process caching reduces redundant requests and helps you stay
within upstream rate limits:

```python
api = GameAPI(cache=True, cache_ttl=60)  # cache_ttl is in seconds
```

Caching is off by default. Nothing sensitive (credentials, headers) is ever
cached — only parsed response data.

## Rate limits & retries

`gameapi` never attempts to bypass a third-party API's rate limits. When an
upstream API returns HTTP 429, `gameapi` retries a small, conservative
number of times with exponential backoff, then raises `RateLimitError`,
which exposes `error.retry_after` (seconds) when the upstream API provided
it:

```python
from gameapi import RateLimitError

try:
    player = api.player(game="chess_com", identifier="hikaru")
except RateLimitError as e:
    print(f"Rate limited, retry after {e.retry_after}s")
```

Transient server errors (HTTP 500/502/503/504) and network timeouts are
retried the same way before surfacing as `APIUnavailableError`.

## Error handling

All exceptions inherit from `GameAPIError`, so you can catch broadly or
narrowly:

```python
from gameapi import (
    GameAPIError,
    GameNotSupportedError,
    PlayerNotFoundError,
    AuthenticationError,
    RateLimitError,
    APIUnavailableError,
    InvalidResponseError,
)

try:
    player = api.player(game="chess_com", identifier="does-not-exist")
except PlayerNotFoundError:
    print("No such player.")
except GameAPIError as e:
    print(f"Something else went wrong: {e}")
```

## API reference

### `GameAPI(api_key=None, cache=False, cache_ttl=60.0, timeout=10.0, max_retries=2)`

- `player(game: str, identifier: str) -> Player`
- `matches(game: str, identifier: str, limit: int = 20) -> list[Match]`
- `leaderboard(game: str, region: str | None = None) -> Leaderboard`
- `close() -> None` (also available as a context manager: `with GameAPI() as api:`)

`AsyncGameAPI` has the identical constructor and method signatures, `await`-ed,
plus `await api.aclose()` (also available as `async with AsyncGameAPI() as api:`).

### Models (`gameapi.models`)

- `Player` — `name`, `game`, `identifier`, `stats`, `rank`, `game_data`, `avatar_url`
- `PlayerStats` — `games_played`, `wins`, `losses`, `draws`, `win_rate`
- `Rank` — `tier`, `rating`, `position`, `raw`
- `Match` — `id`, `game`, `played_at`, `result`, `opponent`, `game_data`
- `Leaderboard` / `LeaderboardEntry` — `position`, `name`, `rating`

Every model is a plain `@dataclass`, so `dataclasses.asdict(player)` works
out of the box if you need to serialize one.

## Development

```bash
git clone https://github.com/F0xyN0xy/gameapi
cd gameapi
pip install -e ".[dev]"
pytest
```

Tests use mocked HTTP responses (via `respx`) — no live network calls or
API keys are needed to run the suite.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to add a new game
integration or improve an existing one.

## License

[MIT](LICENSE)

## Legal

`gameapi` only integrates with public APIs that permit this kind of access
under their terms of service, and documents the original data source for
every integration. It does not imply affiliation with, or endorsement by,
any game publisher unless explicitly stated. `gameapi` does not scrape
websites in ways that violate their terms, and does not attempt to bypass
authentication, rate limits, or anti-bot protections.
