import os
from typing import Any, Dict, Optional

import httpx

TRANSACTION_SERVICE_URL = os.getenv(
    "TRANSACTION_SERVICE_URL",
    "http://localhost:8001",
)


async def fetch_transaction(transaction_id: str) -> Optional[Dict[str, Any]]:
    url = f"{TRANSACTION_SERVICE_URL}/transactions/{transaction_id}"

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(url)

    if response.status_code == 404:
        return None

    response.raise_for_status()
    return response.json()