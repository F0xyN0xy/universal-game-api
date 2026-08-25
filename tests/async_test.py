import asyncio
from gameapi import AsyncGameAPI

async def main():
    async with AsyncGameAPI() as api:
        player = await api.player(game='chess_com', identifier='hikaru')
        print(player.name)

asyncio.run(main())
