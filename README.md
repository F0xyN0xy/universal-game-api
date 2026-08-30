# Universal Game API (`gameapi`)

[![PyPI version](https://badge.fury.io/py/universal-game-api.svg)](https://pypi.org/project/universal-game-api/)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> One interface. Every game. No API archaeology.

`gameapi` is a Python library that unifies public game APIs behind a single, consistent interface. Instead of learning a new client for every game, you write the same code for Chess.com, Lichess, and whatever comes next.

## PyPI

Go to [PyPI](https://pypi.org/project/universal-game-api/) and write an email to be invited as a collaborator.


## Installation

```bash
pip install gameapi
```

```python
from gameapi import GameAPI

with GameAPI() as api:
    player = api.player(game="chess_com", identifier="hikaru")
    print(player.name, player.rank.rating)   # hikaru 2800
```

---

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
api.player(game="lichess", identifier="...")
api.player(game="rocket_league", identifier="...")  # once implemented
```

Common fields (`name`, `stats`, `rank`) are normalized. Anything that doesn't generalize lives on `player.game_data`.

---

## Supported Games

| Game      | Slug        | Auth Required | Data Source                          |
|-----------|-------------|---------------|--------------------------------------|
| Chess.com | `chess_com` | No            | Chess.com Published-Data API         |
| Lichess   | `lichess`   | No            | Lichess Public API                   |
| osu!      | `osu`       | Yes (OAuth)   | osu! API v2                          |

```python
from gameapi import supported_games
print(supported_games())  # ['chess_com', 'lichess', 'osu']
```

### osu!

osu! is the first integration that requires credentials. Create a free
OAuth application at <https://osu.ppy.sh/home/account/edit> ("New OAuth
Application" — no redirect URI needed) and pass the Client ID/Secret as a
single `api_key` string in the form `"<client_id>:<client_secret>"`:

```python
from gameapi import GameAPI

with GameAPI(api_key="12345:your-client-secret") as api:
    player = api.player(game="osu", identifier="mrekk")
    print(player.name, player.rank.rating, player.rank.position)  # mrekk 18000.5 1
```

gameapi handles the OAuth client-credentials token exchange, caching, and
refresh for you — you only ever deal in the two credentials above.

osu! has no head-to-head "match" concept like chess does, so
`api.matches(game="osu", identifier=...)` returns the player's recent play
history instead, with `result` set to `"win"` for passed plays and
`"loss"` for failed ones. `leaderboard(game="osu", region="US")` accepts an
optional ISO country code to get a country's performance rankings instead
of the global one.

---

## Installation

```bash
pip install gameapi
```

Requires Python 3.9+.

### Development

```bash
git clone https://github.com/F0xyN0xy/universal-game-api.git
cd universal-game-api
pip install -e ".[dev]"
pytest
```

---

## Quick Start

### Player Profile

```python
from gameapi import GameAPI

with GameAPI() as api:
    player = api.player(game="chess_com", identifier="hikaru")
    print(player.name)           # hikaru
    print(player.rank.tier)      # GM
    print(player.rank.rating)    # 2800
    print(player.stats)          # PlayerStats(games_played=..., wins=...)
```

### Recent Matches

```python
for match in api.matches(game="chess_com", identifier="hikaru", limit=10):
    print(match.result, match.opponent, match.played_at)
```

### Leaderboard

```python
board = api.leaderboard(game="chess_com")
for entry in board.top(5):
    print(entry.position, entry.name, entry.rating)
```

### Batch Lookups

```python
players = api.compare_players("chess_com", ["hikaru", "magnuscarlsen", "nihalsarin"])
for p in players:
    print(p.name, p.rank.rating)
```

### Async

```python
import asyncio
from gameapi import AsyncGameAPI

async def main():
    async with AsyncGameAPI() as api:
        player = await api.player(game="lichess", identifier="drnykterstein")
        print(player.name)

asyncio.run(main())
```

---

## Caching

Optional in-process caching reduces redundant requests:

```python
api = GameAPI(cache=True, cache_ttl=60)  # seconds
```

Nothing sensitive is ever cached — only parsed response data.

---

## Rate Limits & Retries

`gameapi` retries transient failures (HTTP 429/500/502/503/504) with exponential backoff, then raises typed exceptions:

```python
from gameapi import RateLimitError

try:
    player = api.player(game="chess_com", identifier="hikaru")
except RateLimitError as e:
    print(f"Rate limited, retry after {e.retry_after}s")
```

429 responses respect the upstream `Retry-After` header when provided.

---

## Error Handling

All exceptions inherit from `GameAPIError`:

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
```

---

## Type Safety

`gameapi` is fully typed and passes `mypy --strict` with zero errors. All public APIs have complete type annotations using modern Python 3.9+ syntax:

```python
from gameapi import GameAPI, Player

api: GameAPI = GameAPI()
player: Player = api.player(game="chess_com", identifier="hikaru")

# IDE autocomplete works perfectly
rating: float | None = player.rank.rating
games: int | None = player.stats.games_played
```

Type stubs are included in the package for optimal IDE support.

---

## API Reference

### `GameAPI(api_key=None, cache=False, cache_ttl=60.0, timeout=10.0, max_retries=2)`

| Method | Returns |
|--------|---------|
| `player(game, identifier)` | `Player` |
| `matches(game, identifier, limit=20)` | `list[Match]` |
| `leaderboard(game, region=None)` | `Leaderboard` |
| `compare_players(game, identifiers)` | `list[Player]` |
| `game_info(game)` | `dict` |
| `close()` | — |

Context-manager compatible: `with GameAPI() as api:`

`AsyncGameAPI` has identical signatures, `await`-ed.

### Models

- `Player` — `name`, `game`, `identifier`, `stats`, `rank`, `game_data`, `avatar_url`
- `PlayerStats` — `games_played`, `wins`, `losses`, `draws`, `win_rate`
- `Rank` — `tier`, `rating`, `position`, `raw`
- `Match` — `id`, `game`, `played_at`, `result`, `opponent`, `game_data`
- `Leaderboard` / `LeaderboardEntry` — `position`, `name`, `rating`

Every model is a `@dataclass`, so `dataclasses.asdict(player)` works out of the box.

---

## Demo Project

A small CLI and dashboard built on `gameapi` lives in `demo-project/`:

```bash
cd demo-project
pip install -e "."

# Look up a player
python -m demo_project chess_com hikaru -m 5 -l

# Compare two players side-by-side
python src/demo_project/dashboard.py chess_com hikaru magnuscarlsen
```

---

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for how to add a new game integration. The pattern is:

1. Create `src/gameapi/games/<game>/`
2. Subclass `GameIntegration`
3. Register it in `games/registry.py`

No changes to `client.py` or `async_client.py` are needed.

---

## License

[MIT](LICENSE)

## Legal

`gameapi` only integrates with public APIs that permit this kind of access under their terms of service. It does not scrape websites in ways that violate their terms, and does not attempt to bypass authentication, rate limits, or anti-bot protections.
