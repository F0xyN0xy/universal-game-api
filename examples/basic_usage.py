"""Basic synchronous usage example."""

from gameapi import GameAPI

with GameAPI(cache=True, cache_ttl=120) as api:
    # Player lookup
    player = api.player(game="chess_com", identifier="hikaru")
    print(f"{player.name} — {player.rank.tier} — Rating: {player.rank.rating}")
    print(f"Stats: {player.stats}")

    # Recent matches
    for match in api.matches(game="chess_com", identifier="hikaru", limit=5):
        print(f"  {match.result} vs {match.opponent} on {match.played_at}")

    # Leaderboard
    board = api.leaderboard(game="chess_com")
    for entry in board.top(5):
        print(f"  {entry.position}. {entry.name} ({entry.rating})")
