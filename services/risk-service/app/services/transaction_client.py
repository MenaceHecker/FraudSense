import os
from typing import Any, Dict, Optional

import httpx

TRANSACTION_SERVICE_URL = os.getenv(
    "TRANSACTION_SERVICE_URL",
    "http://localhost:8001",
)

# A single client is shared across requests so the connection pool is reused
# instead of paying for a new pool and TCP/TLS handshake on every call.
_client: Optional[httpx.AsyncClient] = None


def get_client() -> httpx.AsyncClient:
    global _client
    if _client is None:
        _client = httpx.AsyncClient(
            base_url=TRANSACTION_SERVICE_URL,
            timeout=10.0,
        )
    return _client


async def close_client() -> None:
    global _client
    if _client is not None:
        await _client.aclose()
        _client = None


async def fetch_transaction(transaction_id: str) -> Optional[Dict[str, Any]]:
    response = await get_client().get(f"/transactions/{transaction_id}")

    if response.status_code == 404:
        return None

    response.raise_for_status()
    return response.json()