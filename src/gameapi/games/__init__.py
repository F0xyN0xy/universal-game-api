"""Game-specific integrations."""

from .base import GameIntegration
from .registry import GAME_REGISTRY, register_game, supported_games

__all__ = ["GameIntegration", "GAME_REGISTRY", "register_game", "supported_games"]
