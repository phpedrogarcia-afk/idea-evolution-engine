"""
src/idea_evolution/service/contracts.py
Contratos de Aplicação para o FioIdeias V1 Service Boundary (P1).

Define modelos de requisição, resposta e taxonomia tipada de falhas operacionais,
encapsulando o núcleo científico Lean L1 sem duplicação ou mutação semântica.
"""

from __future__ import annotations
from enum import Enum
from typing import Optional, Dict, Any, List
from datetime import datetime
from pydantic import BaseModel, Field

from src.idea_evolution.orchestration.lean_loop import LeanRunResult
from src.idea_evolution.artifacts.evolution_artifact import (
    CoverageIssueType,
    CoverageStatus,
    EvolutionArtifact,
    TreatmentMode,
)
from src.idea_evolution.config.cost_policy import ProviderConfig


class ServiceFailureType(str, Enum):
    """Taxonomia tipada de desfechos operacionais e falhas do serviço."""
    INVALID_INPUT = "INVALID_INPUT"
    PROVIDER_FAILURE = "PROVIDER_FAILURE"
    PROVIDER_AUTH_FAILURE = "PROVIDER_AUTH_FAILURE"
    PROVIDER_RATE_LIMIT = "PROVIDER_RATE_LIMIT"
    PROVIDER_SERVER_FAILURE = "PROVIDER_SERVER_FAILURE"
    PROVIDER_UNAVAILABLE = "PROVIDER_UNAVAILABLE"
    COST_POLICY_BLOCKED = "COST_POLICY_BLOCKED"
    STRUCTURED_OUTPUT_FAILURE = "STRUCTURED_OUTPUT_FAILURE"
    DOMAIN_DECISION_OR_STOP = "DOMAIN_DECISION_OR_STOP"
    INTERNAL_APPLICATION_FAILURE = "INTERNAL_APPLICATION_FAILURE"


class MaturationRepairOutcome(str, Enum):
    NOT_NEEDED = "NOT_NEEDED"
    CALL_BUDGET_EXHAUSTED = "CALL_BUDGET_EXHAUSTED"
    AUTHORITY_POLICY_BLOCKED = "AUTHORITY_POLICY_BLOCKED"
    REPAIR_CALL_FAILED = "REPAIR_CALL_FAILED"
    PATCH_REJECTED = "PATCH_REJECTED"
    REPAIR_APPLIED = "REPAIR_APPLIED"
    REPAIR_INCOMPLETE = "REPAIR_INCOMPLETE"


class MaturationRepairTelemetry(BaseModel):
    """Minimal, non-prompt execution record for M4's single repair opportunity."""

    logical_model_calls_used: int = Field(ge=0, le=2)
    repair_attempted: bool = False
    repair_applied: bool = False
    final_coverage_status: CoverageStatus
    repair_outcome: MaturationRepairOutcome
    issue_count_before: int = Field(ge=0)
    issue_types_before: List[CoverageIssueType] = Field(default_factory=list)
    issue_count_after: int = Field(ge=0)
    issue_types_after: List[CoverageIssueType] = Field(default_factory=list)


class EvolutionRequest(BaseModel):
    """
    Contrato de requisição minimalista de produto para evolução de ideias.
    Preserva o texto bruto original para garantir a proveniência humana.
    """
    raw_idea: str
    treatment_mode: TreatmentMode = TreatmentMode.LEAN_L1
    run_id: Optional[str] = None
    model_name: Optional[str] = None
    provider_config: Optional[ProviderConfig] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    allow_experimental_deep_loop: bool = False  # Trava explícita contra uso acidental de Condição B

    def validate_input(self) -> Optional[str]:
        """Validação mínima de entrada em nível de aplicação."""
        if not self.raw_idea or not self.raw_idea.strip():
            return "A ideia crua fornecida está vazia ou contém apenas espaços."
        if len(self.raw_idea.strip()) < 3:
            return "A ideia crua fornecida é excessivamente curta (mínimo 3 caracteres)."
        return None


class EvolutionResponse(BaseModel):
    """
    Contrato estável de resposta da camada de aplicação do FioIdeias V1.
    Encapsula o resultado científico sem competir com o futuro EvolutionArtifact (P2).
    """
    success: bool
    run_id: str
    treatment_used: TreatmentMode
    raw_idea: str
    terminal_status: str
    total_model_calls: int = 0
    human_decision_requested: bool = False
    decision_progress_detected: bool = True
    failure_type: Optional[ServiceFailureType] = None
    error_message: Optional[str] = None
    lean_result: Optional[LeanRunResult] = None
    baseline_result: Optional[Dict[str, Any]] = None
    artifact: Optional[EvolutionArtifact] = None
    maturation_repair: Optional[MaturationRepairTelemetry] = None
    provider_config: Optional[ProviderConfig] = None
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())
