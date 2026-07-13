from enum import StrEnum
import random


class Status(StrEnum):
    NORMAL = "normal"
    WARNING = "warning"
    CRITICAL = "critical"


def get_style(status: Status) -> str:
    styles = {
        Status.NORMAL: "badge-success",
        Status.WARNING: "badge-warning",
        Status.CRITICAL: "badge-error",
    }
    return styles[status]


def get_status() -> Status:
    return random.choice([s for s in Status])
