"""Registry mapping game slugs to their integration classes.

Adding a new game integration requires creating a ``games/<new_game>/``
module (see ``games/chess_com/`` for the reference implementation) and
registering its integration class here. Nothing in :mod:`gameapi.client`
or :mod:`gameapi.async_client` needs to change.
"""

from __future__ import annotations

from typing import Dict, Type

from .base import GameIntegration
from .chess_com.client import ChessComIntegration

GAME_REGISTRY: Dict[str, Type[GameIntegration]] = {
    ChessComIntegration.slug: ChessComIntegration,
}


def supported_games() -> list:
    """Return the list of currently registered game slugs."""
    return sorted(GAME_REGISTRY.keys())


def register_game(integration_cls: Type[GameIntegration]) -> Type[GameIntegration]:
    """Register a new game integration class.

    Can be used as a decorator by third-party integrations:

    >>> @register_game
    ... class MyGameIntegration(GameIntegration):
    ...     slug = "my_game"
    ...     ...
    """
    GAME_REGISTRY[integration_cls.slug] = integration_cls
    return integration_cls
