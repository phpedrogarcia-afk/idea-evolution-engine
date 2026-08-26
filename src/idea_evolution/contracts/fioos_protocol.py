"""
src/idea_evolution/contracts/fioos_protocol.py
Contratos tipados Pydantic e invariantes determinísticas do protocolo IEE/FioOS Protocol V1.
ESTE MÓDULO É PURAMENTE UMA ESPECIFICAÇÃO DE SCHEMA E CONTRATO.
NÃO CONTÉM RUNTIME, BRIDGE OU CÓDIGO DE EXECUÇÃO DO FioOS.
"""

from __future__ import annotations
from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, field_validator, model_validator


# ==============================================================================
# ENUMS DO PROTOCOLO
# ==============================================================================

class CognitiveRequirement(str, Enum):
    """Requisitos cognitivos abstratos para investigação epistêmica (não amarrados a modelos)."""
    ADVERSARIAL_REASONING_HIGH = "ADVERSARIAL_REASONING_HIGH"
    ADVERSARIAL_REASONING_MEDIUM = "ADVERSARIAL_REASONING_MEDIUM"
    SEMANTIC_SYNTHESIS_HIGH = "SEMANTIC_SYNTHESIS_HIGH"
    SEMANTIC_SYNTHESIS_MEDIUM = "SEMANTIC_SYNTHESIS_MEDIUM"
    RESEARCH_FAST = "RESEARCH_FAST"
    MECHANICAL_NO_MODEL = "MECHANICAL_NO_MODEL"


class EpistemicState(str, Enum):
    """Estados epistêmicos do Idea Evolution Engine."""
    MORE_INVESTIGATION_REQUIRED = "MORE_INVESTIGATION_REQUIRED"
    STALLED = "STALLED"
    HUMAN_DECISION_REQUIRED = "HUMAN_DECISION_REQUIRED"
    READY_TO_TEST = "READY_TO_TEST"


class FioOSOperationalStatus(str, Enum):
    """Respostas operacionais do FioOS para requisições de teste da realidade."""
    AUTHORIZED = "AUTHORIZED"
    BLOCKED = "BLOCKED"
    DEFERRED = "DEFERRED"
    BUDGET_DENIED = "BUDGET_DENIED"
    AUTHORITY_REQUIRED = "AUTHORITY_REQUIRED"
    UNAVAILABLE = "UNAVAILABLE"


class OntologyLayer(str, Enum):
    """As cinco camadas ontológicas de proposições no IEE."""
    CORE = "CORE"
    DERIVED = "DERIVED"
    CANDIDATE = "CANDIDATE"
    DEFERRED = "DEFERRED"
    REJECTED = "REJECTED"


class ClaimVerificationStatus(str, Enum):
    """Status epistêmico de verificação de uma claim."""
    UNTESTED = "UNTESTED"
    SUPPORTED = "SUPPORTED"
    REFUTED = "REFUTED"
    UNCERTAIN = "UNCERTAIN"
    CONTRADICTED = "CONTRADICTED"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"


class IEEOperatingMode(str, Enum):
    """Modos operacionais do Idea Evolution Engine."""
    STANDALONE = "STANDALONE"
    FIOOS_GOVERNED = "FIOOS_GOVERNED"


# ==============================================================================
# CONTRATO 1: InvestigationIntent (IEE -> FioOS)
# ==============================================================================

class EpistemicBudgetHint(BaseModel):
    max_rounds: int = 3
    cost_sensitivity: str = "ZERO_INCREMENTAL_PREFERRED"  # ZERO_INCREMENTAL_PREFERRED | LOW_COST | UNCONSTRAINED


class IntentProvenance(BaseModel):
    created_by: str = "IEE_INVESTIGATION_COORDINATOR"
    created_at: str


class InvestigationIntent(BaseModel):
    """
    Intenção de Investigação enviada pelo IEE para o FioOS.
    INVARIANTE: Não pode conter credenciais, comandos de shell, ToolRequest ou autoridade operacional.
    """
    idea_id: str
    genome_version: str
    uncertainty_id: str
    target_claims: List[str] = Field(default_factory=list)
    question: str
    epistemic_operation: str  # CRITIQUE | DISCRIMINATE | EVIDENCE_GATHERING | REALITY_TEST
    decision_relevance: str
    evidence_required: str
    preferred_topology: str = "SEQUENTIAL_PIPELINE"
    cognitive_requirements: List[CognitiveRequirement] = Field(default_factory=list)
    protected_cores: List[str] = Field(default_factory=list)
    epistemic_budget_hint: EpistemicBudgetHint = Field(default_factory=EpistemicBudgetHint)
    stop_condition: str
    provenance: IntentProvenance

    @field_validator("target_claims")
    @classmethod
    def validate_target_claims_not_empty(cls, v: List[str]) -> List[str]:
        if not v:
            raise ValueError("INVESTIGATION_INTENT_INVALID: target_claims não pode ser vazio.")
        return v

    @model_validator(mode="after")
    def validate_no_operational_secrets_or_tools(self) -> InvestigationIntent:
        # Varredura estrita contra injeção de segredos ou autoridade operacional no intent epistêmico
        forbidden_keywords = [
            "api_key", "bearer ", "sk-", "password", "secret", 
            "exec(", "shell", "curl ", "rm -rf", "tool_call", "granted_authority"
        ]
        intent_repr = f"{self.question} {self.stop_condition} {self.decision_relevance}".lower()
        for kw in forbidden_keywords:
            if kw in intent_repr:
                raise ValueError(f"INVESTIGATION_INTENT_VIOLATION: Detectado elemento operacional proibido: '{kw}'")
        return self


# ==============================================================================
# CONTRATO 2: FioOSMissionPlan (Planejamento Interno FioOS)
# ==============================================================================

class OperationalBudget(BaseModel):
    max_cost_usd: float = 0.0
    max_tokens: int = 100000


class FioOSMissionPlan(BaseModel):
    """
    Plano de Missão Operacional gerado pelo FioOS.
    INVARIANTE: MISSION PLAN != AUTHORIZATION.
    """
    investigation_intent_hash: str
    mission_id: str
    source_identity: str
    lane: str = "BATCH"  # INTERACTIVE | BATCH | SECURE_ENCLAVE
    concrete_model: str
    provider: str
    reasoning_effort: str = "MEDIUM"
    context_allocation_bytes: int = 65536
    tools: List[str] = Field(default_factory=list)
    requested_authority: str = "READ_ONLY"
    budget: OperationalBudget = Field(default_factory=OperationalBudget)
    territory: str = "SANDBOX_EPHEMERAL"
    test_budget: str = "1_EXECUTION"
    stop_condition: str


# ==============================================================================
# CONTRATO 3: ExecutionIdentityBinding (Autorização Temporal FioOS)
# ==============================================================================

class ExecutionIdentityBinding(BaseModel):
    """
    Vínculo temporal de identidade concedido downstream da autorização formal.
    """
    binding_id: str
    mission_id: str
    authorized_identity: str
    workload_token: str
    granted_authority: str
    lease_expires_at: str
    sandbox_container_id: str


# ==============================================================================
# CONTRATO 4: EvidenceEnvelope (FioOS -> IEE)
# ==============================================================================

class OperationalCostReport(BaseModel):
    total_tokens: int = 0
    cost_usd: float = 0.0
    latency_seconds: float = 0.0


class EvidenceEnvelope(BaseModel):
    """
    Envelope de Evidência retornado pelo FioOS ao IEE.
    INVARIANTE: Carrega observações e proveniência, NÃO verdade aceita.
    """
    evidence_id: str
    mission_id: str
    investigation_intent_hash: str
    source_identity: str
    execution_identity: str
    artifact_pointer: str
    artifact_sha256: str
    observation_type: str  # EXECUTION_OUTPUT | CRITIQUE_BUNDLE | EMPIRICAL_DATA | FAILURE_LOG
    raw_verdict: str  # PASS | FAIL | INCONCLUSIVE
    occurred_at: str
    operational_cost: OperationalCostReport
    intervention_record: List[str] = Field(default_factory=list)
    provenance: Dict[str, Any] = Field(default_factory=dict)
    source_metadata: Dict[str, Any] = Field(default_factory=dict)


# ==============================================================================
# CONTRATO 5: EpistemicUpdate (Processamento Interno IEE)
# ==============================================================================

class ClaimStatusDelta(BaseModel):
    claim_id: str
    previous_status: ClaimVerificationStatus
    new_status: ClaimVerificationStatus


class EpistemicUpdate(BaseModel):
    """
    Atualização epistêmica após interpretação do EvidenceEnvelope pelo IEE.
    INVARIANTE: PROPOSED_GENOME_PATCH != APPLIED_GENOME_PATCH.
    """
    proposed_genome_patch: Dict[str, Any]
    claims_changed: List[ClaimStatusDelta] = Field(default_factory=list)
    evidence_links: List[str] = Field(default_factory=list)
    contradictions: List[str] = Field(default_factory=list)
    uncertainties_resolved: List[str] = Field(default_factory=list)
    uncertainties_created: List[str] = Field(default_factory=list)
    decision_delta: str
    next_recommendation: EpistemicState
    termination_state: str = "ACTIVE"


# ==============================================================================
# REGRAS DETERMINÍSTICAS DE TRANSIÇÃO ONTOLÓGICA
# ==============================================================================

class OntologyTransitionValidator:
    """Validador determinístico de regras de transição de estado ontológico."""

    @staticmethod
    def validate_transition(
        current_layer: OntologyLayer,
        target_layer: OntologyLayer,
        human_authority_granted: bool = False,
        has_justification: bool = False,
        has_new_evidence: bool = False,
        reopen_reason: str = "",
    ) -> bool:
        """
        Valida se a transição entre camadas ontológicas respeita a constituição.
        """
        if current_layer == target_layer:
            return True

        # CANDIDATE -> DERIVED: Exige justificativa formal
        if current_layer == OntologyLayer.CANDIDATE and target_layer == OntologyLayer.DERIVED:
            if not has_justification:
                raise ValueError("ONTOLOGY_VIOLATION: CANDIDATE -> DERIVED exige justificativa formal.")
            return True

        # CANDIDATE -> CORE: Exige autorização humana expressa
        if current_layer == OntologyLayer.CANDIDATE and target_layer == OntologyLayer.CORE:
            if not human_authority_granted:
                raise ValueError("ONTOLOGY_VIOLATION: CANDIDATE -> CORE exige autorização humana explícita.")
            return True

        # DERIVED -> CORE: Exige autorização humana expressa
        if current_layer == OntologyLayer.DERIVED and target_layer == OntologyLayer.CORE:
            if not human_authority_granted:
                raise ValueError("ONTOLOGY_VIOLATION: DERIVED -> CORE exige autorização humana explícita.")
            return True

        # REJECTED -> Qualquer estado ativo: Exige nova evidência ou motivo explícito
        if current_layer == OntologyLayer.REJECTED and target_layer in [OntologyLayer.CANDIDATE, OntologyLayer.DERIVED, OntologyLayer.CORE]:
            if not (has_new_evidence or bool(reopen_reason.strip())):
                raise ValueError("ONTOLOGY_VIOLATION: REJECTED -> ACTIVE exige nova evidência ou motivo explícito de reabertura.")
            return True

        # DEFERRED -> Qualquer estado ativo: Exige mudança de condições ou motivo de reabertura
        if current_layer == OntologyLayer.DEFERRED and target_layer in [OntologyLayer.CANDIDATE, OntologyLayer.DERIVED, OntologyLayer.CORE]:
            if not (has_new_evidence or bool(reopen_reason.strip())):
                raise ValueError("ONTOLOGY_VIOLATION: DEFERRED -> ACTIVE exige nova evidência ou motivo explícito de reabertura.")
            return True

        # Qualquer transição para REJECTED ou DEFERRED é permitida por deliberação
        if target_layer in [OntologyLayer.REJECTED, OntologyLayer.DEFERRED]:
            return True

        return True
