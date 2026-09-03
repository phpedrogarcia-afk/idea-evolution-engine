"""
src/idea_evolution/artifacts/evolution_artifact.py
Artefato Canônico de Produto do FioIdeias V1 (M06 P2).

Representação estruturada e auditável do desfecho de maturação de uma ideia,
preservando a distinção estrita entre:
- O que o humano expressou (original_idea)
- O que o sistema inferiu (human_intent, com proveniência explícita)
- O que o sistema propôs (refined_idea, candidate_possibilities)
- O que permanece incerto (critique, assumptions, uncertainties, human_decision_required)
"""

from __future__ import annotations
from enum import Enum
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, field_validator, model_validator

from src.idea_evolution.domain.state import PromotionAuthorityBasis
from src.idea_evolution.domain.epistemic_contracts import SourceAnchor

SCHEMA_VERSION_1_0 = "1.0"
FROZEN_LEAN_CORE_HASH = "e6785bcaf5af291f438ab467386db640d4c0790e0f7012c40773dd25782e5600"


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


class CandidatePossibility(BaseModel):
    """Possibilidade ou alternativa gerada pelo sistema (estritamente não-autoritativa)."""
    mechanism: str
    authority_basis: PromotionAuthorityBasis = PromotionAuthorityBasis.MODEL_HYPOTHESIS
    justification: str = ""
    tradeoffs: List[str] = Field(default_factory=list)

    @field_validator("authority_basis")
    @classmethod
    def prevent_user_explicit_spoofing(cls, v: PromotionAuthorityBasis) -> PromotionAuthorityBasis:
        """Invariante: Candidatos propostos pelo sistema não podem alegar autoridade do usuário."""
        if v in (PromotionAuthorityBasis.USER_EXPLICIT, PromotionAuthorityBasis.VALID_USER_DERIVATION):
            raise ValueError(
                f"CandidatePossibility não pode assumir base de autoridade {v}. "
                "Candidatos do sistema devem ser MODEL_HYPOTHESIS ou BORROWED_MODEL."
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
    human_intent: str
    intent_provenance: PromotionAuthorityBasis = PromotionAuthorityBasis.VALID_USER_DERIVATION

    # 3. Ideia Refinada e Mudanças Substanciais
    refined_idea: str
    what_changed: List[str] = Field(default_factory=list)

    # 4. Crítica, Premissas e Incertezas
    critique: List[CritiqueItem] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)
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

    @model_validator(mode="after")
    def validate_terminal_invariants(self) -> EvolutionArtifact:
        """Validações estruturais pós-construção dependentes do estado do artefato."""
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

        return self
