from datetime import datetime, timezone
from typing import Dict, List, Optional
from uuid import uuid4

from app.schemas.transaction import TransactionCreate


class TransactionStore:
    def __init__(self) -> None:
        self._transactions: List[Dict] = [
            {
                "id": str(uuid4()),
                "txn_external_id": "txn_seed_001",
                "user_id": "user_101",
                "amount": 8450.75,
                "merchant": "CryptoHub",
                "category": "crypto",
                "location": "Atlanta, US",
                "country_code": "US",
                "timestamp": datetime(2026, 3, 25, 15, 12, tzinfo=timezone.utc),
                "device_id": "device_a91",
                "rapid_repeat": False,
                "is_flagged": True,
                "flags": ["HIGH_AMOUNT", "RISKY_CATEGORY"],
                "created_at": datetime.now(timezone.utc),
            },
            {
                "id": str(uuid4()),
                "txn_external_id": "txn_seed_002",
                "user_id": "user_102",
                "amount": 48.20,
                "merchant": "Star Coffee",
                "category": "food",
                "location": "Atlanta, US",
                "country_code": "US",
                "timestamp": datetime(2026, 3, 25, 13, 5, tzinfo=timezone.utc),
                "device_id": "device_b55",
                "rapid_repeat": False,
                "is_flagged": False,
                "flags": [],
                "created_at": datetime.now(timezone.utc),
            },
        ]

    def _derive_flags(self, payload: TransactionCreate) -> List[str]:
        flags: List[str] = []

        if payload.amount >= 5000:
            flags.append("HIGH_AMOUNT")

        risky_categories = {"crypto", "gift_cards", "wire_transfer"}
        if payload.category.lower() in risky_categories:
            flags.append("RISKY_CATEGORY")

        if payload.rapid_repeat:
            flags.append("RAPID_REPEAT")

        hour = payload.timestamp.hour
        if hour < 6 or hour > 23:
            flags.append("ODD_HOUR")

        return flags

    def list_transactions(self, flagged_only: bool = False) -> List[Dict]:
        if flagged_only:
            return [txn for txn in self._transactions if txn["is_flagged"]]
        return self._transactions

    def get_transaction(self, transaction_id: str) -> Optional[Dict]:
        return next(
            (txn for txn in self._transactions if txn["id"] == transaction_id),
            None,
        )

    def get_transactions_by_user(self, user_id: str) -> List[Dict]:
        return [txn for txn in self._transactions if txn["user_id"] == user_id]

    def create_transaction(self, payload: TransactionCreate) -> Dict:
        flags = self._derive_flags(payload)

        txn = {
            "id": str(uuid4()),
            "txn_external_id": payload.txn_external_id,
            "user_id": payload.user_id,
            "amount": payload.amount,
            "merchant": payload.merchant,
            "category": payload.category,
            "location": payload.location,
            "country_code": payload.country_code.upper(),
            "timestamp": payload.timestamp,
            "device_id": payload.device_id,
            "rapid_repeat": payload.rapid_repeat,
            "is_flagged": len(flags) > 0,
            "flags": flags,
            "created_at": datetime.now(timezone.utc),
        }

        self._transactions.append(txn)
        return txn


transaction_store = TransactionStore()