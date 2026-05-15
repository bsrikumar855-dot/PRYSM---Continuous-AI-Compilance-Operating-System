"""SQLAlchemy declarative base."""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


def import_models() -> None:
    """Import all ORM models so they are registered with the metadata."""
    from app.models import document, entity, report, risk  # noqa: F401
    from app.models import audit_log, compliance_result, review_task, risk_flag, user  # noqa: F401
    from app.graph import models as graph_models  # noqa: F401
