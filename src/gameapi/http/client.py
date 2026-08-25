"""Shared HTTP layer used by every game integration."""

from __future__ import annotations

import asyncio
import random
import time
from typing import Any, Dict, Optional

import httpx

from ..exceptions import (
    APIUnavailableError,
    AuthenticationError,
    InvalidResponseError,
    RateLimitError,
)

_RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}

DEFAULT_TIMEOUT = 10.0
DEFAULT_MAX_RETRIES = 2
DEFAULT_BACKOFF_BASE = 0.5


class HTTPClient:
    """A thin, shared wrapper around httpx providing retries and error mapping."""

    def __init__(
        self,
        base_headers: Optional[Dict[str, str]] = None,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
    ) -> None:
        self.base_headers = base_headers or {}
        self.timeout = timeout
        self.max_retries = max_retries
        self._sync_client: Optional[httpx.Client] = None
        self._async_client: Optional[httpx.AsyncClient] = None

    @property
    def _sync(self) -> httpx.Client:
        if self._sync_client is None:
            self._sync_client = httpx.Client(
                timeout=self.timeout, headers=dict(self.base_headers)
            )
        return self._sync_client

    @property
    def _async(self) -> httpx.AsyncClient:
        if self._async_client is None:
            self._async_client = httpx.AsyncClient(
                timeout=self.timeout, headers=dict(self.base_headers)
            )
        return self._async_client

    def close(self) -> None:
        if self._sync_client is not None:
            self._sync_client.close()
            self._sync_client = None

    async def aclose(self) -> None:
        if self._async_client is not None:
            await self._async_client.aclose()
            self._async_client = None

    def _merged_headers(self, extra: Optional[Dict[str, str]]) -> Dict[str, str]:
        headers = dict(self.base_headers)
        if extra:
            headers.update(extra)
        return headers

    @staticmethod
    def _backoff_delay(attempt: int) -> float:
        return DEFAULT_BACKOFF_BASE * (2 ** attempt) + random.uniform(0, 0.1)

    @staticmethod
    def _retry_after_seconds(response: httpx.Response) -> Optional[float]:
        header = response.headers.get("Retry-After")
        if header is None:
            return None
        try:
            return float(header)
        except ValueError:
            return None

    def _handle_response(self, response: httpx.Response) -> Dict[str, Any]:
        if response.status_code in (401, 403):
            raise AuthenticationError(
                f"Authentication failed with status {response.status_code}."
            )
        if response.status_code == 429:
            raise RateLimitError(
                "Rate limit exceeded.", retry_after=self._retry_after_seconds(response)
            )
        if response.status_code == 404:
            raise InvalidResponseError("Resource not found (HTTP 404).")
        if response.status_code >= 500:
            raise APIUnavailableError(
                f"The upstream API returned a server error (HTTP {response.status_code})."
            )
        if response.status_code >= 400:
            raise InvalidResponseError(
                f"The upstream API returned an unexpected status: {response.status_code}."
            )
        try:
            return response.json()
        except ValueError as exc:
            raise InvalidResponseError("Response body was not valid JSON.") from exc

    def _sleep_for_retry(self, attempt: int, response: Optional[httpx.Response]) -> None:
        retry_after = None
        if response is not None:
            retry_after = self._retry_after_seconds(response)
        delay = retry_after if retry_after is not None else self._backoff_delay(attempt)
        time.sleep(delay)

    async def _async_sleep_for_retry(
        self, attempt: int, response: Optional[httpx.Response]
    ) -> None:
        retry_after = None
        if response is not None:
            retry_after = self._retry_after_seconds(response)
        delay = retry_after if retry_after is not None else self._backoff_delay(attempt)
        await asyncio.sleep(delay)

    def request(
        self,
        method: str,
        url: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        merged_headers = self._merged_headers(headers)
        last_exc: Optional[Exception] = None

        for attempt in range(self.max_retries + 1):
            response: Optional[httpx.Response] = None
            try:
                response = self._sync.request(
                    method, url, params=params, headers=merged_headers
                )
            except httpx.TimeoutException as exc:
                last_exc = APIUnavailableError("Request timed out.")
                if attempt < self.max_retries:
                    time.sleep(self._backoff_delay(attempt))
                    continue
                raise last_exc from exc
            except httpx.HTTPError as exc:
                last_exc = APIUnavailableError(f"Network error contacting API: {exc}")
                if attempt < self.max_retries:
                    time.sleep(self._backoff_delay(attempt))
                    continue
                raise last_exc from exc

            if response.status_code in _RETRYABLE_STATUS_CODES and attempt < self.max_retries:
                self._sleep_for_retry(attempt, response)
                continue

            return self._handle_response(response)

        assert last_exc is not None
        raise last_exc

    async def request_async(
        self,
        method: str,
        url: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        merged_headers = self._merged_headers(headers)
        last_exc: Optional[Exception] = None

        for attempt in range(self.max_retries + 1):
            response: Optional[httpx.Response] = None
            try:
                response = await self._async.request(
                    method, url, params=params, headers=merged_headers
                )
            except httpx.TimeoutException as exc:
                last_exc = APIUnavailableError("Request timed out.")
                if attempt < self.max_retries:
                    await asyncio.sleep(self._backoff_delay(attempt))
                    continue
                raise last_exc from exc
            except httpx.HTTPError as exc:
                last_exc = APIUnavailableError(f"Network error contacting API: {exc}")
                if attempt < self.max_retries:
                    await asyncio.sleep(self._backoff_delay(attempt))
                    continue
                raise last_exc from exc

            if response.status_code in _RETRYABLE_STATUS_CODES and attempt < self.max_retries:
                await self._async_sleep_for_retry(attempt, response)
                continue

            return self._handle_response(response)

        assert last_exc is not None
        raise last_exc
