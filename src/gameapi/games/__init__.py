"""Game-specific integrations."""

from .base import GameIntegration
from .registry import GAME_REGISTRY, register_game, supported_games

__all__ = ["GAME_REGISTRY", "GameIntegration", "register_game", "supported_games"]
