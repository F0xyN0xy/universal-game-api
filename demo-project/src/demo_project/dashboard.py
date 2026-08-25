"""Rich text dashboard comparing two players."""

from __future__ import annotations

import argparse

from rich.console import Console
from rich.table import Table

from gameapi import GameAPI


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare two players side-by-side")
    parser.add_argument("game", choices=["chess_com", "lichess"])
    parser.add_argument("player1")
    parser.add_argument("player2")
    args = parser.parse_args()

    console = Console()
    api = GameAPI(cache=True, cache_ttl=120)

    try:
        p1, p2 = api.compare_players(args.game, [args.player1, args.player2])

        table = Table(title=f"{args.game} — Player Comparison", show_header=True, header_style="bold magenta")
        table.add_column("Metric", style="cyan")
        table.add_column(p1.name, justify="right")
        table.add_column(p2.name, justify="right")

        table.add_row("Title", p1.rank.tier or "N/A", p2.rank.tier or "N/A")
        table.add_row("Rating", str(p1.rank.rating or "N/A"), str(p2.rank.rating or "N/A"))
        table.add_row("Wins", str(p1.stats.wins or "N/A"), str(p2.stats.wins or "N/A"))
        table.add_row("Losses", str(p1.stats.losses or "N/A"), str(p2.stats.losses or "N/A"))
        table.add_row("Draws", str(p1.stats.draws or "N/A"), str(p2.stats.draws or "N/A"))
        table.add_row("Win Rate", f"{p1.win_rate_pct() or 'N/A'}%", f"{p2.win_rate_pct() or 'N/A'}%")

        console.print(table)
    finally:
        api.close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
