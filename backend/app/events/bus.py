"""
PRYSM Domain Event Bus
========================
Lightweight, in-process event system for internal orchestration,
logging, and future async workflow support.

Usage:
    from app.events.bus import event_bus
    from app.events.types import DocumentUploaded

    # Subscribe
    @event_bus.on(DocumentUploaded)
    def handle_upload(event: DocumentUploaded):
        logger.info(f"Document {event.doc_id} uploaded")

    # Publish
    event_bus.emit(DocumentUploaded(doc_id="abc-123", filename="invoice.pdf"))

Design:
    - Synchronous, in-process only (no Kafka/RabbitMQ)
    - Type-safe event dispatch
    - Supports multiple handlers per event
    - Audit-safe: all events are logged
    - Future-ready for async handlers
"""

from __future__ import annotations

import logging
from collections import defaultdict
from typing import Callable, Type

from app.events.types import DomainEvent

logger = logging.getLogger(__name__)

HandlerFunc = Callable[[DomainEvent], None]


class EventBus:
    """Simple synchronous event bus for domain event dispatch."""

    def __init__(self) -> None:
        self._handlers: dict[Type[DomainEvent], list[HandlerFunc]] = defaultdict(list)

    def subscribe(self, event_type: Type[DomainEvent], handler: HandlerFunc) -> None:
        """Register a handler for a specific event type."""
        self._handlers[event_type].append(handler)
        logger.debug(
            "event_handler_registered",
            extra={"event_type": event_type.__name__, "handler": handler.__qualname__},
        )

    def on(self, event_type: Type[DomainEvent]) -> Callable:
        """Decorator to subscribe a handler to an event type.

        Example:
            @event_bus.on(DocumentUploaded)
            def handle(event): ...
        """
        def decorator(func: HandlerFunc) -> HandlerFunc:
            self.subscribe(event_type, func)
            return func
        return decorator

    def emit(self, event: DomainEvent) -> None:
        """Dispatch an event to all registered handlers.

        Handlers are executed synchronously. Failures in one handler
        do not prevent other handlers from executing.
        """
        event_type = type(event)
        handlers = self._handlers.get(event_type, [])

        logger.info(
            "domain_event_emitted",
            extra={
                "event_type": event_type.__name__,
                "event_data": event.to_dict(),
                "handler_count": len(handlers),
            },
        )

        for handler in handlers:
            try:
                handler(event)
            except Exception:
                logger.exception(
                    "event_handler_failed",
                    extra={
                        "event_type": event_type.__name__,
                        "handler": handler.__qualname__,
                    },
                )

    def clear(self) -> None:
        """Remove all handlers. Useful for testing."""
        self._handlers.clear()

    def handler_count(self, event_type: Type[DomainEvent] | None = None) -> int:
        """Return the number of registered handlers."""
        if event_type:
            return len(self._handlers.get(event_type, []))
        return sum(len(h) for h in self._handlers.values())


# =============================================================================
# Module-level singleton
# =============================================================================

event_bus = EventBus()
