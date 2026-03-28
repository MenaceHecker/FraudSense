from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class AlertCreate(BaseModel):
    transaction_id: str = Field(..., min_length=1)
    user_id: str = Field(..., min_length=1)
    amount: float
    risk_score: int
    severity: str = Field(..., min_length=1)
    ai_reason: str = Field(..., min_length=1)
    recommended_action: str = Field(..., min_length=1)


class AlertStatusUpdate(BaseModel):
    status: str = Field(..., min_length=1)
    analyst_notes: Optional[str] = None


class AlertResponse(BaseModel):
    id: str
    transaction_id: str
    user_id: str
    amount: float
    risk_score: int
    severity: str
    ai_reason: str
    recommended_action: str
    status: str
    analyst_notes: Optional[str] = None
    created_at: datetime
    resolved_at: Optional[datetime] = None


class AlertListResponse(BaseModel):
    alerts: List[AlertResponse]
    total: int


class DashboardStatsResponse(BaseModel):
    total_transactions: int
    flagged_transactions: int
    high_severity_alerts: int
    medium_severity_alerts: int
    resolved_alerts: int