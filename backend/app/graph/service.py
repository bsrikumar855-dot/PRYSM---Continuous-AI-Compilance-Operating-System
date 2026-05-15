"""
PRYSM Evidence Graph — Service Layer
=======================================
Business logic for creating, querying, and managing evidence relationships.
"""

from __future__ import annotations

import json
import logging
import uuid
from typing import Any

from sqlalchemy.orm import Session

from app.core.enums import EvidenceEntityType, RelationshipType
from app.graph.models import EvidenceEdge, EvidenceNode

logger = logging.getLogger(__name__)


class EvidenceGraphService:
    """Service for building and querying the evidence relationship graph."""

    # ── Node Operations ─────────────────────────────────────────────────

    def create_node(
        self,
        db: Session,
        entity_type: EvidenceEntityType | str,
        label: str,
        doc_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> EvidenceNode:
        """Create a new evidence node."""
        node = EvidenceNode(
            node_id=str(uuid.uuid4()),
            entity_type=str(entity_type),
            doc_id=doc_id,
            label=label,
            metadata_json=json.dumps(metadata) if metadata else None,
        )
        db.add(node)
        db.flush()
        logger.info("evidence_node_created", extra={
            "node_id": node.node_id, "entity_type": node.entity_type,
        })
        return node

    def get_node(self, db: Session, node_id: str) -> EvidenceNode | None:
        return db.query(EvidenceNode).filter(EvidenceNode.node_id == node_id).first()

    def get_nodes_by_doc(self, db: Session, doc_id: str) -> list[EvidenceNode]:
        return db.query(EvidenceNode).filter(EvidenceNode.doc_id == doc_id).all()

    # ── Edge Operations ─────────────────────────────────────────────────

    def link(
        self,
        db: Session,
        source_node_id: str,
        target_node_id: str,
        relationship_type: RelationshipType | str,
        confidence: float = 1.0,
        evidence_text: str | None = None,
        metadata: dict[str, Any] | None = None,
        created_by: str = "system",
    ) -> EvidenceEdge:
        """Create a relationship edge between two evidence nodes."""
        edge = EvidenceEdge(
            edge_id=str(uuid.uuid4()),
            source_node_id=source_node_id,
            target_node_id=target_node_id,
            relationship_type=str(relationship_type),
            confidence=confidence,
            evidence_text=evidence_text,
            metadata_json=json.dumps(metadata) if metadata else None,
            created_by=created_by,
        )
        db.add(edge)
        db.flush()
        logger.info("evidence_edge_created", extra={
            "edge_id": edge.edge_id,
            "source": source_node_id,
            "target": target_node_id,
            "type": str(relationship_type),
        })
        return edge

    # ── Query Helpers ────────────────────────────────────────────────────

    def get_relationships(
        self, db: Session, node_id: str
    ) -> list[dict[str, Any]]:
        """Get all relationships (inbound + outbound) for a node."""
        outbound = db.query(EvidenceEdge).filter(
            EvidenceEdge.source_node_id == node_id
        ).all()
        inbound = db.query(EvidenceEdge).filter(
            EvidenceEdge.target_node_id == node_id
        ).all()

        results = []
        for edge in outbound:
            results.append({
                "edge_id": edge.edge_id,
                "direction": "outbound",
                "related_node_id": edge.target_node_id,
                "relationship_type": edge.relationship_type,
                "confidence": edge.confidence,
                "evidence_text": edge.evidence_text,
            })
        for edge in inbound:
            results.append({
                "edge_id": edge.edge_id,
                "direction": "inbound",
                "related_node_id": edge.source_node_id,
                "relationship_type": edge.relationship_type,
                "confidence": edge.confidence,
                "evidence_text": edge.evidence_text,
            })
        return results

    def find_discrepancies(self, db: Session, doc_id: str) -> list[EvidenceEdge]:
        """Find all DISCREPANT relationships involving a document."""
        nodes = self.get_nodes_by_doc(db, doc_id)
        node_ids = {n.node_id for n in nodes}
        if not node_ids:
            return []
        return db.query(EvidenceEdge).filter(
            EvidenceEdge.relationship_type == RelationshipType.DISCREPANT,
            (
                EvidenceEdge.source_node_id.in_(node_ids)
                | EvidenceEdge.target_node_id.in_(node_ids)
            ),
        ).all()

    def get_document_graph(
        self, db: Session, doc_id: str
    ) -> dict[str, Any]:
        """Build the full evidence graph for a document (for visualization)."""
        nodes = self.get_nodes_by_doc(db, doc_id)
        node_ids = {n.node_id for n in nodes}
        if not node_ids:
            return {"nodes": [], "edges": []}

        edges = db.query(EvidenceEdge).filter(
            EvidenceEdge.source_node_id.in_(node_ids)
            | EvidenceEdge.target_node_id.in_(node_ids)
        ).all()

        return {
            "nodes": [
                {
                    "node_id": n.node_id,
                    "entity_type": n.entity_type,
                    "label": n.label,
                    "doc_id": n.doc_id,
                }
                for n in nodes
            ],
            "edges": [
                {
                    "edge_id": e.edge_id,
                    "source": e.source_node_id,
                    "target": e.target_node_id,
                    "type": e.relationship_type,
                    "confidence": e.confidence,
                }
                for e in edges
            ],
        }
