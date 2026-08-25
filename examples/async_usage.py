"""Basic asynchronous usage example."""

import asyncio
from gameapi import AsyncGameAPI


async def main():
    async with AsyncGameAPI(cache=True, cache_ttl=120) as api:
        player = await api.player(game="lichess", identifier="drnykterstein")
        print(f"{player.name} — {player.rank.tier} — Rating: {player.rank.rating}")

        board = await api.leaderboard(game="lichess")
        for entry in board.top(5):
            print(f"  {entry.position}. {entry.name} ({entry.rating})")


if __name__ == "__main__":
    asyncio.run(main())
