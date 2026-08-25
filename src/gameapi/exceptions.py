"""Custom exception hierarchy for Universal Game API.

All exceptions raised by the public API inherit from :class:`GameAPIError`,
so callers can either catch broad failures or narrow in on a specific
failure mode.

Example
-------
>>> try:
...     player = api.player("chess_com", "does-not-exist-hopefully")
... except PlayerNotFoundError:
...     print("Player doesn't exist.")
... except GameAPIError as exc:
...     print(f"Something else went wrong: {exc}")
"""

from __future__ import annotations

from typing import Optional


class GameAPIError(Exception):
    """Base class for all errors raised by gameapi.

    Attributes:
        message: Human-readable description of the failure.
    """

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class GameNotSupportedError(GameAPIError):
    """Raised when a requested game has no registered integration."""

    def __init__(self, game: str, supported: Optional[list] = None) -> None:
        self.game = game
        self.supported = supported or []
        supported_str = ", ".join(sorted(self.supported)) if self.supported else "none registered"
        super().__init__(
            f"Game '{game}' is not supported. Currently supported games: {supported_str}."
        )


class PlayerNotFoundError(GameAPIError):
    """Raised when a game's API reports that a player/identifier does not exist."""

    def __init__(self, game: str, identifier: str) -> None:
        self.game = game
        self.identifier = identifier
        super().__init__(f"Player '{identifier}' was not found for game '{game}'.")


class AuthenticationError(GameAPIError):
    """Raised when a request fails due to missing or invalid credentials."""

    def __init__(self, message: str = "Authentication failed. Check your API key.") -> None:
        super().__init__(message)


class RateLimitError(GameAPIError):
    """Raised when the upstream API reports that a rate limit was exceeded.

    Attributes:
        retry_after: Seconds to wait before retrying, if the upstream API
            provided this information (via a ``Retry-After`` header). May be
            ``None`` if the upstream response did not include it.
    """

    def __init__(
        self, message: str = "Rate limit exceeded.", retry_after: Optional[float] = None
    ) -> None:
        self.retry_after = retry_after
        super().__init__(message)

    def __repr__(self) -> str:
        return f"RateLimitError(retry_after={self.retry_after!r}, message={self.message!r})"


class APIUnavailableError(GameAPIError):
    """Raised when the upstream API is unreachable or returns a server error
    after retries have been exhausted."""

    def __init__(self, message: str = "The upstream API is currently unavailable.") -> None:
        super().__init__(message)


class InvalidResponseError(GameAPIError):
    """Raised when the upstream API returns a response gameapi cannot parse."""

    def __init__(
        self, message: str = "Received an invalid or unparsable response from the API."
    ) -> None:
        super().__init__(message)
