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

    def list_alerts(
        self,
        status: Optional[str] = None,
        severity: Optional[str] = None,
    ) -> List[Dict]:
        alerts = self._alerts

        if status:
            alerts = [alert for alert in alerts if alert["status"] == status]

        if severity:
            alerts = [alert for alert in alerts if alert["severity"] == severity]

        return alerts

    def get_alert(self, alert_id: str) -> Optional[Dict]:
        return next((alert for alert in self._alerts if alert["id"] == alert_id), None)

    def get_alerts_by_transaction(self, transaction_id: str) -> List[Dict]:
        return [
            alert for alert in self._alerts if alert["transaction_id"] == transaction_id
        ]

    def create_alert(self, payload: AlertCreate) -> Dict:
        alert = {
            "id": str(uuid4()),
            "transaction_id": payload.transaction_id,
            "user_id": payload.user_id,
            "amount": payload.amount,
            "risk_score": payload.risk_score,
            "severity": payload.severity.lower(),
            "ai_reason": payload.ai_reason,
            "recommended_action": payload.recommended_action.lower(),
            "status": "open",
            "analyst_notes": None,
            "created_at": datetime.now(timezone.utc),
            "resolved_at": None,
        }

        self._alerts.append(alert)
        return alert

    def update_status(self, alert_id: str, payload: AlertStatusUpdate) -> Optional[Dict]:
        alert = self.get_alert(alert_id)
        if not alert:
            return None

        new_status = payload.status.lower()
        alert["status"] = new_status
        alert["analyst_notes"] = payload.analyst_notes

        if new_status == "resolved":
            alert["resolved_at"] = datetime.now(timezone.utc)
        else:
            alert["resolved_at"] = None

        return alert

    def get_dashboard_stats(self) -> Dict:
        high_alerts = sum(1 for alert in self._alerts if alert["severity"] == "high")
        medium_alerts = sum(1 for alert in self._alerts if alert["severity"] == "medium")
        resolved_alerts = sum(1 for alert in self._alerts if alert["status"] == "resolved")

        flagged_transactions = len({alert["transaction_id"] for alert in self._alerts})

        return {
            "total_transactions": flagged_transactions + 3,
            "flagged_transactions": flagged_transactions,
            "high_severity_alerts": high_alerts,
            "medium_severity_alerts": medium_alerts,
            "resolved_alerts": resolved_alerts,
        }


alert_store = AlertStore()