"""Game-specific integrations. See games/base.py for the interface every
integration implements, and games/registry.py for how integrations are
registered and looked up by slug."""

from .base import GameIntegration
from .registry import GAME_REGISTRY, register_game, supported_games

__all__ = ["GameIntegration", "GAME_REGISTRY", "register_game", "supported_games"]
