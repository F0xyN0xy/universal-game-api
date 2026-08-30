"""Registry mapping game slugs to their integration classes."""

from __future__ import annotations

from .base import GameIntegration
from .chess_com.client import ChessComIntegration
from .lichess.client import LichessIntegration
from .osu.client import OsuIntegration

GAME_REGISTRY: dict[str, type[GameIntegration]] = {
    ChessComIntegration.slug: ChessComIntegration,
    LichessIntegration.slug: LichessIntegration,
    OsuIntegration.slug: OsuIntegration,
}


def supported_games() -> list[str]:
    """Return the list of currently registered game slugs."""
    return sorted(GAME_REGISTRY.keys())


def register_game(integration_cls: type[GameIntegration]) -> type[GameIntegration]:
    """Register a new game integration class."""
    GAME_REGISTRY[integration_cls.slug] = integration_cls
    return integration_cls