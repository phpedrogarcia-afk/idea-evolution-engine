"""
src/idea_evolution/artifacts/__init__.py
Módulo de Artefatos Canônicos de Produto do FioIdeias V1.
"""

from src.idea_evolution.artifacts.evolution_artifact import (
    EvolutionArtifact,
    CritiqueItem,
    CandidatePossibility,
    IntentImportance,
    IntentOriginType,
    IntentTreatmentStatus,
    IntentLedgerItem,
    UsefulInsight,
    OpenDecision,
    CoverageStatus,
    CoverageIssueType,
    CoverageIssue,
    TreatmentMode,
    SCHEMA_VERSION_1_0,
    SCHEMA_VERSION_1_1,
    FROZEN_LEAN_CORE_HASH,
)
from src.idea_evolution.artifacts.mapper import EvolutionArtifactMapper
from src.idea_evolution.artifacts.provenance import (
    ProvenanceReceipt,
    audit_artifact_provenance,
)

__all__ = [
    "EvolutionArtifact",
    "CritiqueItem",
    "CandidatePossibility",
    "IntentImportance",
    "IntentOriginType",
    "IntentTreatmentStatus",
    "IntentLedgerItem",
    "UsefulInsight",
    "OpenDecision",
    "CoverageStatus",
    "CoverageIssueType",
    "CoverageIssue",
    "TreatmentMode",
    "SCHEMA_VERSION_1_0",
    "SCHEMA_VERSION_1_1",
    "FROZEN_LEAN_CORE_HASH",
    "EvolutionArtifactMapper",
    "ProvenanceReceipt",
    "audit_artifact_provenance",
]
