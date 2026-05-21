"""Date utilities."""

from datetime import datetime


def now_iso() -> str:
    return datetime.utcnow().isoformat() + "Z"
