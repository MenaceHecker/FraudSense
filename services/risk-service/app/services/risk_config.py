from typing import Dict, List, TypedDict


class ScoreComponent(TypedDict):
    score: int
    key_signal: str


class AmountThreshold(TypedDict):
    threshold: float
    component: ScoreComponent


class RiskConfig(TypedDict):
    initial_score: int
    amount_thresholds: List[AmountThreshold]
    risky_categories: Dict[str, ScoreComponent]
    rapid_repeat: ScoreComponent
    odd_hour: ScoreComponent


# Default configuration for the rules-v1 model
DEFAULT_RISK_CONFIG: RiskConfig = {
    "initial_score": 5,
    "amount_thresholds": [
        {"threshold": 5000, "component": {"score": 35, "key_signal": "HIGH_AMOUNT"}},
        {"threshold": 1000, "component": {"score": 15, "key_signal": "LARGE_PURCHASE"}},
    ],
    "risky_categories": {
        "crypto": {"score": 25, "key_signal": "RISKY_CATEGORY"},
        "gift_cards": {"score": 25, "key_signal": "RISKY_CATEGORY"},
        "wire_transfer": {"score": 25, "key_signal": "RISKY_CATEGORY"},
    },
    "rapid_repeat": {"score": 20, "key_signal": "RAPID_REPEAT"},
    "odd_hour": {"score": 10, "key_signal": "ODD_HOUR"},
}