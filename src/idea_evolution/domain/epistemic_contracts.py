"""
src/idea_evolution/domain/epistemic_contracts.py
Contratos de Ancoragem de Fonte, Representação, Insights Tipados, Conhecimento Negativo e Linhagem de Ideias.
Implementação offline/experimental para institucionalização da Fundação Epistêmica (FIOIDEIAS-EPISTEMIC-DONOR-FOUNDATION-01).
"""

from __future__ import annotations
import hashlib
from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from src.idea_evolution.domain.state import OntologyState, PromotionAuthorityBasis


class SourceAnchorKind(str, Enum):
    """Tipos admissíveis de artefatos de fonte primária (não gerados como meras representações)."""
    HUMAN_INPUT = "HUMAN_INPUT"
    HUMAN_DECISION = "HUMAN_DECISION"
    EXTERNAL_EVIDENCE = "EXTERNAL_EVIDENCE"
    DONOR_PRIMARY_SOURCE = "DONOR_PRIMARY_SOURCE"
    EXPERIMENT_ARTIFACT = "EXPERIMENT_ARTIFACT"


class RepresentationType(str, Enum):
    """Tipos admissíveis de representações geradas por modelos ou sínteses."""
    INTERPRETATION = "INTERPRETATION"
    SUMMARY = "SUMMARY"
    SEMANTIC_SIGNATURE = "SEMANTIC_SIGNATURE"
    CANDIDATE_DESCRIPTION = "CANDIDATE_DESCRIPTION"
    SYNTHESIS = "SYNTHESIS"
    INSIGHT = "INSIGHT"


class InsightType(str, Enum):
    """Tipos admissíveis de insights destilados."""
    OBSERVATION_SUMMARY = "OBSERVATION_SUMMARY"
    INFERENCE = "INFERENCE"
    CAUSAL_HYPOTHESIS = "CAUSAL_HYPOTHESIS"
    CONSTRAINT = "CONSTRAINT"
    HEURISTIC = "HEURISTIC"


class ClaimStatus(str, Enum):
    """Classificação epistêmica rigorosa de claims e insights."""
    CONFIRMED = "CONFIRMED"
    PLAUSIBLE = "PLAUSIBLE"
    BORROWED_MODEL = "BORROWED_MODEL"
    DESIGN_HYPOTHESIS = "DESIGN_HYPOTHESIS"
    SPECULATION = "SPECULATION"
    REJECTED = "REJECTED"
    REPORTED_BY_PAPER = "REPORTED_BY_PAPER"
    PROVEN_IN_DONOR = "PROVEN_IN_DONOR"
    PROVEN_IN_IEE = "PROVEN_IN_IEE"


class FailureClass(str, Enum):
    """Classes de falha para categorização de conhecimento negativo."""
    MECHANISM_REFUTED = "MECHANISM_REFUTED"
    IMPLEMENTATION_DEFECT = "IMPLEMENTATION_DEFECT"
    EVIDENCE_INCONCLUSIVE = "EVIDENCE_INCONCLUSIVE"
    MISSING_AUTHORITY = "MISSING_AUTHORITY"
    CONTEXT_MISMATCH = "CONTEXT_MISMATCH"
    DEPENDENCY_UNAVAILABLE = "DEPENDENCY_UNAVAILABLE"
    UNJUSTIFIED_COST = "UNJUSTIFIED_COST"
    NORMATIVE_REJECTION = "NORMATIVE_REJECTION"


class SourceAnchor(BaseModel):
    """
    Artefato fundamental de fonte primária imutável.
    MODEL OUTPUT MUST NEVER CREATE HUMAN SOURCE AUTHORITY.
    """
    source_id: str
    source_kind: SourceAnchorKind
    content_hash: str
    original_content: str
    provenance: str = ""
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    authority_class: str = "PRIMARY_AUTHORITY"

    @classmethod
    def create_human_input_anchor(cls, content: str, source_id: Optional[str] = None) -> SourceAnchor:
        norm = content.strip()
        c_hash = hashlib.sha256(norm.encode("utf-8")).hexdigest()
        sid = source_id or f"SRC-HUMAN-{c_hash[:8]}"
        return cls(
            source_id=sid,
            source_kind=SourceAnchorKind.HUMAN_INPUT,
            content_hash=c_hash,
            original_content=norm,
            provenance="Original human input prompt",
            authority_class="SOVEREIGN_HUMAN_INTENT",
        )


class RepresentationRecord(BaseModel):
    """
    Representação gerada a partir de uma fonte (mapa, resumo, síntese ou interpretação).
    Uma representação NUNCA herda silenciosamente a autoridade da fonte.
    """
    representation_id: str
    representation_type: RepresentationType
    source_refs: List[str] = Field(default_factory=list)
    generated_by: str  # Modelo / Provedor / Estágio que gerou
    transformation_type: str = "SEMANTIC_EXTRACTION"
    claim_status: ClaimStatus = ClaimStatus.DESIGN_HYPOTHESIS
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    content: str


class InsightRecord(BaseModel):
    """
    Registro estruturado de insight destilado a partir de observações ou experimentos.
    DISTILLED INSIGHT MAY GUIDE SEARCH. IT IS NOT AUTOMATICALLY EVIDENCE OR CAUSAL TRUTH.
    """
    insight_id: str
    statement: str
    source_node_ids: List[str] = Field(default_factory=list)
    evidence_refs: List[str] = Field(default_factory=list)
    insight_type: InsightType = InsightType.INFERENCE
    claim_status: ClaimStatus = ClaimStatus.DESIGN_HYPOTHESIS
    confidence: float = 0.5
    counter_explanations: List[str] = Field(default_factory=list)
    scope: str = "GENERAL"
    created_by: str = ""
    validation_needed: bool = True


class NegativeKnowledgeRecord(BaseModel):
    """
    Registro de conhecimento negativo (lições podadas com escopo e condições de reabertura).
    NEGATIVE KNOWLEDGE MUST HAVE SCOPE AND REOPEN CONDITIONS.
    """
    record_id: str
    mechanism_or_claim: str
    failure_class: FailureClass
    evidence_refs: List[str] = Field(default_factory=list)
    scope: str
    conditions_at_failure: Dict[str, Any] = Field(default_factory=dict)
    what_not_to_repeat: str
    what_remains_unknown: str
    reopen_condition: str
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())

    def can_reopen_under(self, current_conditions: Dict[str, Any]) -> bool:
        """Verifica se uma alteração documentada de condições permite reavaliar a direção."""
        # Se alguma condição restritiva anterior mudou ou nova evidência foi fornecida
        for k, v in self.conditions_at_failure.items():
            if k in current_conditions and current_conditions[k] != v:
                return True
        return False


class IdeaLineageNode(BaseModel):
    """
    Nó de linhagem evolutiva de ideias com suporte a multi-parentesco (recombinação de candidatos).
    """
    node_id: str
    parent_ids: List[str] = Field(default_factory=list)
    originating_operation: str = "SYNTHESIZE"  # SYNTHESIZE | MUTATION | RECOMBINATION | SPLIT
    proposal: str
    ontology_state: OntologyState = OntologyState.CANDIDATE
    authority_basis: PromotionAuthorityBasis = PromotionAuthorityBasis.MODEL_HYPOTHESIS
    authority_proof_ref: str = ""
    source_anchor_refs: List[str] = Field(default_factory=list)
    evidence_refs: List[str] = Field(default_factory=list)
    insight_refs: List[str] = Field(default_factory=list)
    decision_delta: str = ""
    status: str = "ACTIVE"
    reopen_condition: str = ""
    cost_record: Dict[str, Any] = Field(default_factory=dict)
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())
