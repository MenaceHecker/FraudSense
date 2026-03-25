from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class TransactionCreate(BaseModel):
    txn_external_id: str = Field(..., min_length=1)
    user_id: str = Field(..., min_length=1)
    amount: float
    merchant: str = Field(..., min_length=1)
    category: str = Field(..., min_length=1)
    location: str = Field(..., min_length=1)
    country_code: str = Field(..., min_length=2, max_length=2)
    timestamp: datetime
    device_id: Optional[str] = None
    rapid_repeat: bool = False


class TransactionResponse(BaseModel):
    id: str
    txn_external_id: str
    user_id: str
    amount: float
    merchant: str
    category: str
    location: str
    country_code: str
    timestamp: datetime
    device_id: Optional[str] = None
    rapid_repeat: bool
    is_flagged: bool
    flags: List[str]
    created_at: datetime


class TransactionListResponse(BaseModel):
    transactions: List[TransactionResponse]
    total: int