from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate


class TransactionStore:
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

    def serialize(self, txn: Transaction) -> dict:
        return {
            "id": str(txn.id),
            "txn_external_id": txn.txn_external_id,
            "user_id": txn.user_id,
            "amount": float(txn.amount),
            "merchant": txn.merchant,
            "category": txn.category,
            "location": txn.location,
            "country_code": txn.country_code,
            "timestamp": txn.timestamp,
            "device_id": txn.device_id,
            "rapid_repeat": txn.rapid_repeat,
            "is_flagged": txn.is_flagged,
            "flags": txn.flags or [],
            "created_at": txn.created_at,
        }

    def list_transactions(self, db: Session, flagged_only: bool = False) -> List[dict]:
        stmt = select(Transaction)
        if flagged_only:
            stmt = stmt.where(Transaction.is_flagged.is_(True))

        rows = db.execute(stmt.order_by(Transaction.created_at.desc())).scalars().all()
        return [self.serialize(row) for row in rows]

    def get_transaction(self, db: Session, transaction_id: str) -> Optional[dict]:
        row = db.get(Transaction, UUID(transaction_id))
        if not row:
            return None
        return self.serialize(row)

    def get_transactions_by_user(self, db: Session, user_id: str) -> List[dict]:
        rows = (
            db.execute(
                select(Transaction)
                .where(Transaction.user_id == user_id)
                .order_by(Transaction.created_at.desc())
            )
            .scalars()
            .all()
        )
        return [self.serialize(row) for row in rows]

    def create_transaction(self, db: Session, payload: TransactionCreate) -> dict:
        flags = self._derive_flags(payload)

        txn = Transaction(
            txn_external_id=payload.txn_external_id,
            user_id=payload.user_id,
            amount=payload.amount,
            merchant=payload.merchant,
            category=payload.category,
            location=payload.location,
            country_code=payload.country_code.upper(),
            timestamp=payload.timestamp,
            device_id=payload.device_id,
            rapid_repeat=payload.rapid_repeat,
            is_flagged=len(flags) > 0,
            flags=flags,
            created_at=datetime.now(timezone.utc),
        )

        db.add(txn)
        db.commit()
        db.refresh(txn)

        return self.serialize(txn)


transaction_store = TransactionStore()