from __future__ import annotations

import httpx
import respx

from gameapi.games.chess_com import endpoints as chess_endpoints
from src.demo_project.main import main


@respx.mock
def test_main_cli(capsys, chess_profile, chess_stats):
    respx.get(chess_endpoints.player_profile_url("hikaru")).mock(
        return_value=httpx.Response(200, json=chess_profile)
    )
    respx.get(chess_endpoints.player_stats_url("hikaru")).mock(
        return_value=httpx.Response(200, json=chess_stats)
    )

    import sys
    old_argv = sys.argv
    sys.argv = ["demo", "chess_com", "hikaru"]
    try:
        ret = main()
        assert ret == 0
    finally:
        sys.argv = old_argv

    captured = capsys.readouterr()
    assert "hikaru" in captured.out
