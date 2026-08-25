"""Simple CLI to look up players across games."""

from __future__ import annotations

import argparse
import sys

from gameapi import GameAPI, GameNotSupportedError, PlayerNotFoundError


def main() -> int:
    parser = argparse.ArgumentParser(description="Look up game players via gameapi")
    parser.add_argument("game", choices=["chess_com", "lichess"], help="Game slug")
    parser.add_argument("username", help="Player username")
    parser.add_argument("--matches", "-m", type=int, default=0, help="Show N recent matches")
    parser.add_argument("--leaderboard", "-l", action="store_true", help="Show leaderboard")

    args = parser.parse_args()

    api = GameAPI(cache=True, cache_ttl=120)

    try:
        print(f"\n🔍 Looking up {args.username} on {args.game}...\n")
        player = api.player(game=args.game, identifier=args.username)

        print(f"Name:     {player.name}")
        print(f"Title:    {player.rank.tier or 'N/A'}")
        print(f"Rating:   {player.rank.rating or 'N/A'}")
        print(f"Wins:     {player.stats.wins or 'N/A'}")
        print(f"Losses:   {player.stats.losses or 'N/A'}")
        print(f"Draws:    {player.stats.draws or 'N/A'}")
        if player.stats.win_rate is not None:
            print(f"Win Rate: {player.win_rate_pct()}%")

        if args.matches > 0:
            print(f"\n📅 Last {args.matches} matches:")
            for match in api.matches(game=args.game, identifier=args.username, limit=args.matches):
                result_emoji = "🟢" if match.is_win else "🔴" if match.is_loss else "🟡"
                print(f"  {result_emoji} vs {match.opponent or '?'} — {match.result}")

        if args.leaderboard:
            print("\n🏆 Leaderboard (top 5):")
            board = api.leaderboard(game=args.game)
            for entry in board.top(5):
                print(f"  {entry.position}. {entry.name} ({entry.rating or '?'})")

    except PlayerNotFoundError:
        print(f"❌ Player '{args.username}' not found on {args.game}.", file=sys.stderr)
        return 1
    except GameNotSupportedError as e:
        print(f"❌ {e}", file=sys.stderr)
        return 1
    finally:
        api.close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
