"""
PRYSM Enterprise Logging
===========================
Structured JSON logging with request ID traceability.
Consolidates core/logging.py and logging/logger.py into one system.
"""

import json
import logging
import uuid
from contextvars import ContextVar
from datetime import datetime, timezone

from app.core.config import settings

# ── Request ID context (set by middleware, read by formatter) ────────────
request_id_ctx: ContextVar[str] = ContextVar("request_id", default="")


class JsonFormatter(logging.Formatter):
    """Structured JSON log formatter with request ID and event metadata."""

    def format(self, record: logging.LogRecord) -> str:
        payload: dict = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        # Attach request ID if available
        rid = request_id_ctx.get("")
        if rid:
            payload["request_id"] = rid
        # Attach structured extra fields
        for key in ("doc_id", "event", "status", "event_type", "event_data",
                     "handler_count", "finding_id", "from_status", "to_status",
                     "node_id", "edge_id", "task_id", "rule_id", "severity"):
            if hasattr(record, key):
                payload[key] = getattr(record, key)
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=True, default=str)


def setup_logging() -> None:
    """Configure application-wide structured logging."""
    root = logging.getLogger()
    if root.handlers:
        return
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    root.setLevel(settings.log_level.upper())
    root.addHandler(handler)


def get_logger(name: str) -> logging.Logger:
    """Get a named logger instance with prysm prefix."""
    return logging.getLogger(f"prysm.{name}")


def generate_request_id() -> str:
    """Generate a unique request ID for traceability."""
    return str(uuid.uuid4())[:8]
