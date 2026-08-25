"""Compare multiple players at once."""

from gameapi import GameAPI

with GameAPI() as api:
    players = api.compare_players("chess_com", ["hikaru", "magnuscarlsen", "nihalsarin"])
    for p in players:
        print(f"{p.name:20} | {p.rank.tier or 'N/A':4} | {p.rank.rating or 'N/A':6} | {p.win_rate_pct() or 'N/A'}%")
