from __future__ import annotations

import httpx
import pytest
import respx

from gameapi.exceptions import (
    APIUnavailableError,
    AuthenticationError,
    InvalidResponseError,
    RateLimitError,
)
from gameapi.http import HTTPClient

URL = "https://example.test/resource"


@respx.mock
def test_successful_request_returns_json():
    respx.get(URL).mock(return_value=httpx.Response(200, json={"ok": True}))
    client = HTTPClient(max_retries=0)
    result = client.request("GET", URL)
    assert result == {"ok": True}


@respx.mock
def test_401_raises_authentication_error():
    respx.get(URL).mock(return_value=httpx.Response(401))
    client = HTTPClient(max_retries=0)
    with pytest.raises(AuthenticationError):
        client.request("GET", URL)


@respx.mock
def test_404_raises_invalid_response_error():
    respx.get(URL).mock(return_value=httpx.Response(404))
    client = HTTPClient(max_retries=0)
    with pytest.raises(InvalidResponseError):
        client.request("GET", URL)


@respx.mock
def test_429_retries_then_raises_rate_limit_error_with_retry_after():
    route = respx.get(URL).mock(
        return_value=httpx.Response(429, headers={"Retry-After": "5"})
    )
    client = HTTPClient(max_retries=2)
    with pytest.raises(RateLimitError) as exc_info:
        client.request("GET", URL)
    assert exc_info.value.retry_after == 5.0
    assert route.call_count == 3


@respx.mock
def test_429_uses_retry_after_header_when_present():
    route = respx.get(URL).mock(
        side_effect=[
            httpx.Response(429, headers={"Retry-After": "0.01"}),
            httpx.Response(200, json={"ok": True}),
        ]
    )
    client = HTTPClient(max_retries=2)
    result = client.request("GET", URL)
    assert result == {"ok": True}
    assert route.call_count == 2


@respx.mock
def test_500_retries_then_succeeds():
    route = respx.get(URL).mock(
        side_effect=[
            httpx.Response(500),
            httpx.Response(200, json={"ok": True}),
        ]
    )
    client = HTTPClient(max_retries=2)
    result = client.request("GET", URL)
    assert result == {"ok": True}
    assert route.call_count == 2


@respx.mock
def test_persistent_500_raises_api_unavailable_error():
    respx.get(URL).mock(return_value=httpx.Response(503))
    client = HTTPClient(max_retries=1)
    with pytest.raises(APIUnavailableError):
        client.request("GET", URL)


@respx.mock
def test_invalid_json_raises_invalid_response_error():
    respx.get(URL).mock(return_value=httpx.Response(200, content=b"not json"))
    client = HTTPClient(max_retries=0)
    with pytest.raises(InvalidResponseError):
        client.request("GET", URL)


@pytest.mark.asyncio
@respx.mock
async def test_async_request_returns_json():
    respx.get(URL).mock(return_value=httpx.Response(200, json={"ok": True}))
    client = HTTPClient(max_retries=0)
    result = await client.request_async("GET", URL)
    assert result == {"ok": True}
    await client.aclose()


@respx.mock
def test_headers_are_merged():
    client = HTTPClient(base_headers={"X-Base": "1"})
    merged = client._merged_headers({"X-Extra": "2"})
    assert merged == {"X-Base": "1", "X-Extra": "2"}


def test_client_passes_base_headers_to_httpx():
    client = HTTPClient(base_headers={"X-Test": "hello"})
    assert client._sync.headers["X-Test"] == "hello"
    client.close()
