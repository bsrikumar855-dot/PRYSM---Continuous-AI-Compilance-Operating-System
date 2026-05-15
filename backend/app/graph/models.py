"""
PRYSM Evidence Graph — ORM Models
====================================
Relational-first models for evidence linking and cross-document traceability.
Supports: Invoice ↔ GST Filing ↔ Bank Transaction ↔ Vendor ↔ ROC Record
"""

from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class EvidenceNode(Base):
    """A node in the evidence graph — represents a traceable compliance entity."""
    __tablename__ = "evidence_nodes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    node_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    entity_type: Mapped[str] = mapped_column(String(50), index=True)
    doc_id: Mapped[str | None] = mapped_column(String(64), index=True, nullable=True)
    label: Mapped[str] = mapped_column(String(255))
    metadata_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )


class EvidenceEdge(Base):
    """An edge — represents a relationship between two evidence nodes."""
    __tablename__ = "evidence_edges"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    edge_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    source_node_id: Mapped[str] = mapped_column(String(64), index=True)
    target_node_id: Mapped[str] = mapped_column(String(64), index=True)
    relationship_type: Mapped[str] = mapped_column(String(50), index=True)
    confidence: Mapped[float] = mapped_column(Float, default=1.0)
    evidence_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    metadata_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_by: Mapped[str] = mapped_column(String(50), default="system")
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
