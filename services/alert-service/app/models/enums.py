import enum


class AlertSeverity(str, enum.Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class AlertStatus(str, enum.Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"


class RecommendedAction(str, enum.Enum):
    BLOCK = "block"
    REVIEW = "review"
    ALLOW = "allow"