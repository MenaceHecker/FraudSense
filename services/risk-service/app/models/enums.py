import enum


class Severity(str, enum.Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class RecommendedAction(str, enum.Enum):
    BLOCK = "block"
    REVIEW = "review"
    ALLOW = "allow"