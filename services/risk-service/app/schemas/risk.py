from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class RiskAssessmentResponse(BaseModel):
    id: str
    transaction_id: str
    risk_score: int
    is_suspicious: bool
    severity: str
    reason: str
    recommended_action: str
    key_signals: List[str]
    model_version: Optional[str] = None
    created_at: datetime