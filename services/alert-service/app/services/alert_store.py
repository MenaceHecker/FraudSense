from datetime import datetime, timezone
from typing import Dict, List, Optional
from uuid import uuid4

from app.schemas.alert import AlertCreate, AlertStatusUpdate


class AlertStore:
    def __init__(self) -> None:
        self._alerts: List[Dict] = [
            {
                "id": str(uuid4()),
                "transaction_id": "seed-transaction-001",
                "user_id": "user_101",
                "amount": 8450.75,
                "risk_score": 82,
                "severity": "high",
                "ai_reason": "Large crypto transaction with elevated fraud signals.",
                "recommended_action": "block",
                "status": "open",
                "analyst_notes": None,
                "created_at": datetime.now(timezone.utc),
                "resolved_at": None,
            },
            {
                "id": str(uuid4()),
                "transaction_id": "seed-transaction-002",
                "user_id": "user_102",
                "amount": 1200.00,
                "risk_score": 58,
                "severity": "medium",
                "ai_reason": "Moderate anomaly detected based on category and timing.",
                "recommended_action": "review",
                "status": "reviewing",
                "analyst_notes": "Checking prior customer history.",
                "created_at": datetime.now(timezone.utc),
                "resolved_at": None,
            },
        ]