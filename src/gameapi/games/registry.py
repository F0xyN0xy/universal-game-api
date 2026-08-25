"""Registry mapping game slugs to their integration classes."""

from __future__ import annotations

from typing import Dict, Type

from .base import GameIntegration
from .chess_com.client import ChessComIntegration
from .lichess.client import LichessIntegration

GAME_REGISTRY: Dict[str, Type[GameIntegration]] = {
    ChessComIntegration.slug: ChessComIntegration,
    LichessIntegration.slug: LichessIntegration,
}


def supported_games() -> list[str]:
    """Return the list of currently registered game slugs."""
    return sorted(GAME_REGISTRY.keys())


def register_game(integration_cls: Type[GameIntegration]) -> Type[GameIntegration]:
    """Register a new game integration class."""
    GAME_REGISTRY[integration_cls.slug] = integration_cls
    return integration_cls