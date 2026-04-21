from datetime import datetime, timezone
from typing import Dict, List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.alert import Alert
from app.schemas.alert import AlertCreate, AlertStatusUpdate


class AlertStore:
    def serialize(self, alert: Alert) -> Dict:
        return {
            "id": str(alert.id),
            "transaction_id": str(alert.transaction_id),
            "user_id": alert.user_id,
            "amount": float(alert.amount),
            "risk_score": alert.risk_score,
            "severity": alert.severity,
            "ai_reason": alert.ai_reason,
            "recommended_action": alert.recommended_action,
            "status": alert.status,
            "analyst_notes": alert.analyst_notes,
            "created_at": alert.created_at,
            "resolved_at": alert.resolved_at,
        }

    def list_alerts(
        self,
        db: Session,
        status: Optional[str] = None,
        severity: Optional[str] = None,
    ) -> List[Dict]:
        stmt = select(Alert)

        if status:
            stmt = stmt.where(Alert.status == status)

        if severity:
            stmt = stmt.where(Alert.severity == severity)

        rows = db.execute(stmt.order_by(Alert.created_at.desc())).scalars().all()
        return [self.serialize(row) for row in rows]

    def get_alert(self, db: Session, alert_id: str) -> Optional[Dict]:
        row = db.get(Alert, UUID(alert_id))
        if not row:
            return None
        return self.serialize(row)

    def get_alerts_by_transaction(self, db: Session, transaction_id: str) -> List[Dict]:
        rows = (
            db.execute(
                select(Alert)
                .where(Alert.transaction_id == UUID(transaction_id))
                .order_by(Alert.created_at.desc())
            )
            .scalars()
            .all()
        )
        return [self.serialize(row) for row in rows]

    def create_alert(self, db: Session, payload: AlertCreate) -> Dict:
        alert = Alert(
            transaction_id=UUID(payload.transaction_id),
            user_id=payload.user_id,
            amount=payload.amount,
            risk_score=payload.risk_score,
            severity=payload.severity.lower(),
            ai_reason=payload.ai_reason,
            recommended_action=payload.recommended_action.lower(),
            status="open",
            analyst_notes=None,
            created_at=datetime.now(timezone.utc),
            resolved_at=None,
        )

        db.add(alert)
        db.commit()
        db.refresh(alert)
        return self.serialize(alert)

    def update_status(
        self,
        db: Session,
        alert_id: str,
        payload: AlertStatusUpdate,
    ) -> Optional[Dict]:
        alert = db.get(Alert, UUID(alert_id))
        if not alert:
            return None

        new_status = payload.status.lower()
        alert.status = new_status
        alert.analyst_notes = payload.analyst_notes

        if new_status == "resolved":
            alert.resolved_at = datetime.now(timezone.utc)
        else:
            alert.resolved_at = None

        db.commit()
        db.refresh(alert)
        return self.serialize(alert)

    def get_dashboard_stats(self, db: Session) -> Dict:
        alerts = db.execute(select(Alert)).scalars().all()

        high_alerts = sum(1 for alert in alerts if alert.severity == "high")
        medium_alerts = sum(1 for alert in alerts if alert.severity == "medium")
        resolved_alerts = sum(1 for alert in alerts if alert.status == "resolved")
        flagged_transactions = len({str(alert.transaction_id) for alert in alerts})

        return {
            "total_transactions": flagged_transactions + 3,
            "flagged_transactions": flagged_transactions,
            "high_severity_alerts": high_alerts,
            "medium_severity_alerts": medium_alerts,
            "resolved_alerts": resolved_alerts,
        }


alert_store = AlertStore()