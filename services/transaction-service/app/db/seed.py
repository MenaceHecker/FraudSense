from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.transaction import Transaction


def seed_transactions(db: Session) -> None:
    existing = db.execute(select(Transaction)).scalars().first()
    if existing:
        return

    rows = [
        Transaction(
            txn_external_id="txn_seed_001",
            user_id="user_101",
            amount=8450.75,
            merchant="CryptoHub",
            category="crypto",
            location="Atlanta, US",
            country_code="US",
            timestamp=datetime(2026, 3, 25, 15, 12, tzinfo=timezone.utc),
            device_id="device_a91",
            rapid_repeat=False,
            is_flagged=True,
            flags=["HIGH_AMOUNT", "RISKY_CATEGORY"],
            created_at=datetime.now(timezone.utc),
        ),
        Transaction(
            txn_external_id="txn_seed_002",
            user_id="user_102",
            amount=48.20,
            merchant="Star Coffee",
            category="food",
            location="Atlanta, US",
            country_code="US",
            timestamp=datetime(2026, 3, 25, 13, 5, tzinfo=timezone.utc),
            device_id="device_b55",
            rapid_repeat=False,
            is_flagged=False,
            flags=[],
            created_at=datetime.now(timezone.utc),
        ),
    ]

    db.add_all(rows)
    db.commit()