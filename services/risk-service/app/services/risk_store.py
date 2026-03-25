from datetime import datetime, timezone
from typing import Dict, Optional
from uuid import uuid4


class RiskStore:
    def __init__(self) -> None:
        self._assessments: Dict[str, Dict] = {}

    def get(self, transaction_id: str) -> Optional[Dict]:
        return self._assessments.get(transaction_id)

    def save(self, transaction_id: str, assessment: Dict) -> Dict:
        self._assessments[transaction_id] = assessment
        return assessment