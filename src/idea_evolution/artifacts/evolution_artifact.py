"""
src/idea_evolution/artifacts/evolution_artifact.py
Artefato Canônico de Produto do FioIdeias V1 (M06 P2/P3).

Representação estruturada, auditável e imutável do desfecho de maturação de uma ideia,
preservando a distinção estrita e determinística entre:
- O que o humano expressou (original_idea -> USER_EXPLICIT)
- O que o sistema inferiu (human_intent -> VALID_USER_DERIVATION)
- O que o sistema propôs (refined_idea -> MODEL_HYPOTHESIS, candidate_possibilities)
- O que permanece incerto (critique, assumptions, uncertainties, human_decision_required)

Invariante inegociável:
USER_EXPLICIT != VALID_USER_DERIVATION != MODEL_CANDIDATE != UNKNOWN
"""

from __future__ import annotations
import hashlib
from enum import Enum
from typing import Optional, List, Dict, Any, TYPE_CHECKING
from datetime import datetime
from pydantic import BaseModel, Field, field_validator, model_validator

from src.idea_evolution.domain.state import PromotionAuthorityBasis, OntologyState
from src.idea_evolution.domain.epistemic_contracts import SourceAnchor
from src.idea_evolution.domain.grounding import AuthorityProofValidator

if TYPE_CHECKING:
    from src.idea_evolution.artifacts.provenance import ProvenanceReceipt

SCHEMA_VERSION_1_0 = "1.0"
SCHEMA_VERSION_1_1 = "1.1"
FROZEN_LEAN_CORE_HASH_V1_0 = "e6785bcaf5af291f438ab467386db640d4c0790e0f7012c40773dd25782e5600"
FROZEN_LEAN_CORE_HASH_V1_1 = "9a8ff063138f2f1fb8624a75feb968ac5a48f358f858c6c5e4ab61513dfb6423"
FROZEN_LEAN_CORE_HASH = FROZEN_LEAN_CORE_HASH_V1_1


class TreatmentMode(str, Enum):
    """
    Modos de tratamento suportados pelo FioIdeias V1.
    O padrão inegociável de produto é LEAN_L1 (Condição C).
    """
    LEAN_L1 = "LEAN_L1"                          # Padrão de produto: Lean L1 + Early Epistemic Gate
    FAST_FALLBACK = "FAST_FALLBACK"              # Fallback de contingência / Sanity Baseline (Condição A)
    SUSPENDED_DEEP_LOOP = "SUSPENDED_DEEP_LOOP"  # Suspenso do caminho padrão; pesquisa interna isolada (Condição B)


class CritiqueItem(BaseModel):
    """Item individual de crítica ou vulnerabilidade identificado pelo sistema."""
    vulnerability: str
    severity: str = "MEDIUM"  # HIGH, MEDIUM, LOW
    why_it_matters: str = ""
    affected_aspect: str = ""
    authority_basis: PromotionAuthorityBasis = PromotionAuthorityBasis.MODEL_HYPOTHESIS


class CandidatePossibility(BaseModel):
    """Possibilidade ou alternativa gerada pelo sistema (estritamente não-autoritativa)."""
    mechanism: str
    authority_basis: PromotionAuthorityBasis = PromotionAuthorityBasis.MODEL_HYPOTHESIS
    ontology_state: OntologyState = OntologyState.CANDIDATE
    justification: str = ""
    tradeoffs: List[str] = Field(default_factory=list)

    @field_validator("authority_basis")
    @classmethod
    def prevent_user_explicit_spoofing(cls, v: PromotionAuthorityBasis) -> PromotionAuthorityBasis:
        """Invariante: Candidatos propostos pelo sistema não podem alegar autoridade do usuário."""
        if v in (PromotionAuthorityBasis.USER_EXPLICIT, PromotionAuthorityBasis.VALID_USER_DERIVATION):
            raise ValueError(
                f"CandidatePossibility não pode assumir base de autoridade {v}. "
                "Candidatos do sistema pertencem a MODEL_HYPOTHESIS ou BORROWED_MODEL."
            )
        return v

    @field_validator("ontology_state")
    @classmethod
    def prevent_core_spoofing(cls, v: OntologyState) -> OntologyState:
        """Invariante: Candidatos do sistema não podem alegar estado CORE."""
        if v == OntologyState.CORE:
            raise ValueError(
                "CandidatePossibility não pode assumir estado ontológico CORE. "
                "Candidatos do sistema pertencem a CANDIDATE, DEFERRED ou REJECTED."
            )
        return v


class EvolutionArtifact(BaseModel):
    """
    Artefato Canônico de Evolução de Ideia (FioIdeias V1).
    Contrato unificado consumido por CLI, APIs, Renderizador e futura integração FioOS.
    """
    # 1. Metadados e Versionamento do Schema
    schema_version: str = SCHEMA_VERSION_1_0
    artifact_id: str
    run_id: str
    treatment_mode: TreatmentMode
    terminal_status: str
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())

    # 2. Entrada Imutável e Intenção Preservada
    original_idea: str
    original_idea_authority: PromotionAuthorityBasis = PromotionAuthorityBasis.USER_EXPLICIT
    human_intent: str
    intent_provenance: PromotionAuthorityBasis = PromotionAuthorityBasis.VALID_USER_DERIVATION

    # 3. Ideia Refinada e Mudanças Substanciais
    refined_idea: str
    refined_idea_authority: PromotionAuthorityBasis = PromotionAuthorityBasis.MODEL_HYPOTHESIS
    what_changed: List[str] = Field(default_factory=list)

    # 4. Crítica, Premissas e Incertezas
    critique: List[CritiqueItem] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)
    assumptions_authority: PromotionAuthorityBasis = PromotionAuthorityBasis.MODEL_HYPOTHESIS
    uncertainties: List[str] = Field(default_factory=list)

    # 5. Possibilidades e Próximos Passos
    candidate_possibilities: List[CandidatePossibility] = Field(default_factory=list)
    recommended_next_action: str = ""
    human_decision_required: bool = False
    human_decision_description: Optional[str] = None

    # 6. Proveniência e Auditoria Mínima
    source_anchor: Optional[SourceAnchor] = None
    scientific_core_hash: Optional[str] = None
    model_name: Optional[str] = None
    provider: Optional[str] = None
    total_model_calls: int = 0

    # ---------------------------------------------------------------------------
    # Validações de Invariantes de Produto
    # ---------------------------------------------------------------------------

    @field_validator("original_idea")
    @classmethod
    def validate_original_idea_non_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("EvolutionArtifact: original_idea não pode ser vazia.")
        return v

    @field_validator("original_idea_authority")
    @classmethod
    def validate_original_idea_authority(cls, v: PromotionAuthorityBasis) -> PromotionAuthorityBasis:
        if v != PromotionAuthorityBasis.USER_EXPLICIT:
            raise ValueError("EvolutionArtifact: original_idea deve ter autoridade USER_EXPLICIT.")
        return v

    @model_validator(mode="after")
    def validate_terminal_invariants(self) -> EvolutionArtifact:
        """Validações estruturais e epistêmicas pós-construção dependentes do estado do artefato."""
        completed_statuses = {
            "COMPLETED_DIRECT_ONE_PASS",
            "COMPLETED_WITH_FOCUSED_ESCALATION",
            "COMPLETED",
        }
        if self.terminal_status in completed_statuses and not self.refined_idea.strip():
            raise ValueError(
                f"EvolutionArtifact: refined_idea não pode ser vazia quando terminal_status é {self.terminal_status}."
            )

        # Se for Lean L1, o hash do núcleo científico deve ser declarado
        if self.treatment_mode == TreatmentMode.LEAN_L1 and not self.scientific_core_hash:
            self.scientific_core_hash = FROZEN_LEAN_CORE_HASH

        # 1. Validação estrita de autoridade em refined_idea
        if self.refined_idea_authority == PromotionAuthorityBasis.USER_EXPLICIT:
            is_valid, _, reason = AuthorityProofValidator.validate_user_explicit(self.original_idea, self.refined_idea)
            if not is_valid:
                raise ValueError(
                    f"Authority Spoofing: refined_idea alega autoridade USER_EXPLICIT mas falhou na validação de ancoragem: {reason}"
                )

        # 2. Validação estrita de autoridade em human_intent
        if self.intent_provenance == PromotionAuthorityBasis.USER_EXPLICIT:
            is_valid, _, reason = AuthorityProofValidator.validate_user_explicit(self.original_idea, self.human_intent)
            if not is_valid:
                raise ValueError(
                    f"Authority Spoofing: human_intent alega autoridade USER_EXPLICIT mas falhou na validação de ancoragem: {reason}"
                )

        # 3. Validação de premissas (assumptions nunca podem ser declaradas como fatos explícitos do usuário)
        if self.assumptions_authority == PromotionAuthorityBasis.USER_EXPLICIT:
            raise ValueError("EvolutionArtifact: premissas (assumptions) não podem ter autoridade USER_EXPLICIT.")

        # 4. Verificação de integridade de SourceAnchor e detecção de tampering
        if self.source_anchor is not None:
            # Checagem de hash do conteúdo
            expected_hash = hashlib.sha256(self.source_anchor.original_content.encode()).hexdigest()
            if self.source_anchor.content_hash and self.source_anchor.content_hash != expected_hash:
                raise ValueError(
                    f"Tamper detected no SourceAnchor: content_hash ({self.source_anchor.content_hash}) "
                    f"não corresponde ao SHA-256 do conteúdo ({expected_hash})."
                )
            # Checagem de concordância com original_idea
            if self.original_idea.strip() != self.source_anchor.original_content.strip():
                raise ValueError(
                    "Tamper detected: original_idea difere de source_anchor.original_content."
                )

        return self

    def audit_provenance(self) -> ProvenanceReceipt:
        """Gera o recibo determinístico de proveniência dos itens semânticos do artefato."""
        from src.idea_evolution.artifacts.provenance import audit_artifact_provenance
        return audit_artifact_provenance(self)
