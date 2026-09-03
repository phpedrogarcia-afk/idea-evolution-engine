"""
src/idea_evolution/artifacts/__init__.py
Módulo de Artefatos Canônicos de Produto do FioIdeias V1.
"""

from src.idea_evolution.artifacts.evolution_artifact import (
    EvolutionArtifact,
    CritiqueItem,
    CandidatePossibility,
    TreatmentMode,
    SCHEMA_VERSION_1_0,
    FROZEN_LEAN_CORE_HASH,
)
from src.idea_evolution.artifacts.mapper import EvolutionArtifactMapper

__all__ = [
    "EvolutionArtifact",
    "CritiqueItem",
    "CandidatePossibility",
    "TreatmentMode",
    "SCHEMA_VERSION_1_0",
    "FROZEN_LEAN_CORE_HASH",
    "EvolutionArtifactMapper",
]
