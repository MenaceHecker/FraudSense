import uuid
from decimal import Decimal

from sqlalchemy import DateTime, Enum, Integer, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base
from app.models.enums import AlertSeverity, AlertStatus, RecommendedAction

"""
Alert model representing a fraud alert in the system.

Each alert is generated in response to a transaction that is deemed suspicious
by the risk assessment service. It contains details about the transaction, the
risk analysis, and the current status of the investigation.
"""

class Alert(Base):
    __tablename__ = "alerts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    transaction_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    user_id: Mapped[str] = mapped_column(String(64), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    risk_score: Mapped[int] = mapped_column(Integer, nullable=False)
    severity: Mapped[AlertSeverity] = mapped_column(Enum(AlertSeverity), nullable=False)
    ai_reason: Mapped[str] = mapped_column(Text, nullable=False)
    recommended_action: Mapped[RecommendedAction] = mapped_column(Enum(RecommendedAction), nullable=False)
    status: Mapped[AlertStatus] = mapped_column(Enum(AlertStatus), nullable=False, default=AlertStatus.OPEN)
    analyst_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    resolved_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)