"""
src/idea_evolution/artifacts/evolution_artifact.py
Artefato Canônico de Produto do FioIdeias V1 (M06 P2/P3).

Representação estruturada, auditável e imutável do desfecho de maturação de uma ideia,
preservando a distinção estrita e determinística entre:
- O que o humano expressou (original_idea -> USER_EXPLICIT)
- O que o sistema interpretou (human_intent -> MODEL_HYPOTHESIS por padrão)
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
FROZEN_LEAN_CORE_HASH_V1_1 = "3fa70e0ede15888ee5650fa08572508748eef1462de0a8bd01aa4a66a58b151f"
FROZEN_LEAN_CORE_HASH_RQ11 = "1d294c2be6b9e52733e2e543b7b921b2f0fb64034ebced95aa08403b6504fa83"
FROZEN_LEAN_CORE_HASH = FROZEN_LEAN_CORE_HASH_RQ11


class TreatmentMode(str, Enum):
    """
    Modos de tratamento suportados pelo FioIdeias V1.
    O padrão inegociável de produto é LEAN_L1 (Condição C).
    """
    LEAN_L1 = "LEAN_L1"                          # Padrão de produto: Lean L1 + Early Epistemic Gate
    FAST_FALLBACK = "FAST_FALLBACK"              # Fallback de contingência / Sanity Baseline (Condição A)
    SUSPENDED_DEEP_LOOP = "SUSPENDED_DEEP_LOOP"  # Suspenso do caminho padrão; pesquisa interna isolada (Condição B)


class IntentImportance(str, Enum):
    CORE_INTENT = "CORE_INTENT"
    MATERIAL_SUBINTENT = "MATERIAL_SUBINTENT"
    EXPLICIT_CONSTRAINT = "EXPLICIT_CONSTRAINT"


class IntentOriginType(str, Enum):
    USER_EXPLICIT = "USER_EXPLICIT"
    MODEL_INTERPRETATION = "MODEL_INTERPRETATION"


class IntentTreatmentStatus(str, Enum):
    PRESERVED = "PRESERVED"
    EXPANDED = "EXPANDED"
    PROVISIONALLY_MODIFIED = "PROVISIONALLY_MODIFIED"
    DEFERRED = "DEFERRED"
    CONFLICT_FOUND = "CONFLICT_FOUND"


class IntentLedgerItem(BaseModel):
    """One attributed intent claim; origin_type records provenance, not authority promotion."""

    intent_id: str = Field(min_length=1)
    source_quote: str = ""
    interpretation: str
    importance: IntentImportance
    origin_type: IntentOriginType
    treatment_in_current_form: str = ""
    status: IntentTreatmentStatus

    @field_validator("intent_id")
    @classmethod
    def validate_intent_id(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("IntentLedgerItem.intent_id não pode ser vazio.")
        return value


class UsefulInsight(BaseModel):
    """Optional insight candidate; it carries no user or decision authority."""

    insight_id: str = Field(min_length=1)
    description: str
    related_intent_ids: List[str] = Field(default_factory=list)
    authority_basis: PromotionAuthorityBasis = PromotionAuthorityBasis.MODEL_HYPOTHESIS

    @field_validator("authority_basis")
    @classmethod
    def keep_insight_non_authoritative(cls, value: PromotionAuthorityBasis) -> PromotionAuthorityBasis:
        if value in (PromotionAuthorityBasis.USER_EXPLICIT, PromotionAuthorityBasis.VALID_USER_DERIVATION):
            raise ValueError("UsefulInsight permanece proposta não autoritativa do modelo.")
        return value


class OpenDecision(BaseModel):
    """An unresolved idea/product choice; its presence does not request human authority."""

    decision_id: str = Field(min_length=1)
    question: str
    related_intent_ids: List[str] = Field(default_factory=list)


class CoverageStatus(str, Enum):
    """Structural coverage result; NO_BLOCKING_GAP_DETECTED is not semantic proof."""

    NOT_EVALUATED = "NOT_EVALUATED"
    NO_BLOCKING_GAP_DETECTED = "NO_BLOCKING_GAP_DETECTED"
    REPAIR_REQUIRED = "REPAIR_REQUIRED"
    UNRESOLVED = "UNRESOLVED"


class CoverageIssueType(str, Enum):
    SOURCE_QUOTE_INVALID = "SOURCE_QUOTE_INVALID"
    MATERIAL_INTENT_UNTREATED = "MATERIAL_INTENT_UNTREATED"
    EXPLICIT_CONSTRAINT_UNTREATED = "EXPLICIT_CONSTRAINT_UNTREATED"
    INTENT_REFERENCE_INVALID = "INTENT_REFERENCE_INVALID"
    CONFLICT_FOUND = "CONFLICT_FOUND"
    PROVISIONAL_MODIFICATION_NOT_EXPOSED = "PROVISIONAL_MODIFICATION_NOT_EXPOSED"
    DEFERRED_ITEM_NOT_EXPOSED = "DEFERRED_ITEM_NOT_EXPOSED"
    CURRENT_FORM_REFERENCE_GAP = "CURRENT_FORM_REFERENCE_GAP"
    STRUCTURAL_COVERAGE_FAILURE = "STRUCTURAL_COVERAGE_FAILURE"


class CoverageIssue(BaseModel):
    """Typed coverage finding; M1 defines its shape, not semantic detection behavior."""

    issue_type: CoverageIssueType
    description: str
    intent_id: Optional[str] = None
    path_id: Optional[str] = None


class CritiqueItem(BaseModel):
    """Item individual de crítica ou vulnerabilidade identificado pelo sistema."""
    vulnerability: str
    severity: str = "MEDIUM"  # HIGH, MEDIUM, LOW
    why_it_matters: str = ""
    affected_aspect: str = ""
    authority_basis: PromotionAuthorityBasis = PromotionAuthorityBasis.MODEL_HYPOTHESIS
    authority_proof_ref: str = ""
    gate_eligible: bool = False


class CandidatePossibility(BaseModel):
    """Possibilidade ou alternativa gerada pelo sistema (estritamente não-autoritativa)."""
    mechanism: str
    authority_basis: PromotionAuthorityBasis = PromotionAuthorityBasis.MODEL_HYPOTHESIS
    ontology_state: OntologyState = OntologyState.CANDIDATE
    justification: str = ""
    tradeoffs: List[str] = Field(default_factory=list)
    # Optional for loading historical possibilities produced before M1.
    path_id: Optional[str] = None
    intent_ids: List[str] = Field(default_factory=list)

    @field_validator("path_id")
    @classmethod
    def validate_path_id(cls, value: Optional[str]) -> Optional[str]:
        if value is not None and not value.strip():
            raise ValueError("CandidatePossibility.path_id não pode ser vazio quando fornecido.")
        return value

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
    # New artifacts use the additive M1 contract. Explicit historical 1.0 remains loadable.
    schema_version: str = SCHEMA_VERSION_1_1
    artifact_id: str
    run_id: str
    treatment_mode: TreatmentMode
    terminal_status: str
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())

    # 2. Entrada Imutável e Intenção Preservada
    original_idea: str
    original_idea_authority: PromotionAuthorityBasis = PromotionAuthorityBasis.USER_EXPLICIT
    human_intent: str
    intent_provenance: PromotionAuthorityBasis = PromotionAuthorityBasis.MODEL_HYPOTHESIS

    # 3. Ideia Refinada e Mudanças Substanciais
    refined_idea: str
    refined_idea_authority: PromotionAuthorityBasis = PromotionAuthorityBasis.MODEL_HYPOTHESIS
    what_changed: List[str] = Field(default_factory=list)

    # 4. Crítica, Premissas e Incertezas
    critique: List[CritiqueItem] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)
    assumptions_authority: PromotionAuthorityBasis = PromotionAuthorityBasis.MODEL_HYPOTHESIS
    uncertainties: List[str] = Field(default_factory=list)
    intent_ledger: List[IntentLedgerItem] = Field(default_factory=list)
    useful_insights: List[UsefulInsight] = Field(default_factory=list)
    open_decisions: List[OpenDecision] = Field(default_factory=list)
    coverage_status: CoverageStatus = CoverageStatus.NOT_EVALUATED
    coverage_issues: List[CoverageIssue] = Field(default_factory=list)

    # 5. Possibilidades e Próximos Passos
    candidate_possibilities: List[CandidatePossibility] = Field(default_factory=list)
    recommended_next_action: str = ""
    recommended_next_action_basis: PromotionAuthorityBasis = PromotionAuthorityBasis.MODEL_HYPOTHESIS
    recommended_next_action_support_ref: str = ""
    recommended_next_action_status: str = "EVIDENCE_NEEDED"
    # Legacy uncertainties are strings, so this exact-text reference avoids inventing IDs.
    recommended_next_action_target_uncertainty: Optional[str] = None
    human_decision_required: bool = False
    human_decision_description: Optional[str] = None
    human_decision_authority_basis: PromotionAuthorityBasis = PromotionAuthorityBasis.MODEL_HYPOTHESIS
    human_decision_support_ref: str = ""

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

        if self.schema_version not in (SCHEMA_VERSION_1_0, SCHEMA_VERSION_1_1):
            raise ValueError(f"EvolutionArtifact: schema_version não suportada: {self.schema_version}.")

        # A 1.0 artifact predates coverage evaluation; it cannot claim a later coverage result.
        if self.schema_version == SCHEMA_VERSION_1_0:
            self.coverage_status = CoverageStatus.NOT_EVALUATED
            self.coverage_issues = []

        intent_ids = [item.intent_id for item in self.intent_ledger]
        if len(intent_ids) != len(set(intent_ids)):
            raise ValueError("EvolutionArtifact: intent_id duplicado no intent_ledger.")
        known_intents = set(intent_ids)

        # Presence of an exact quote proves only that the words occur in the source.
        validate_intent_source_quotes(self.original_idea, self.intent_ledger)
        required_treatment = {
            IntentTreatmentStatus.PRESERVED,
            IntentTreatmentStatus.EXPANDED,
            IntentTreatmentStatus.PROVISIONALLY_MODIFIED,
            IntentTreatmentStatus.CONFLICT_FOUND,
        }
        for item in self.intent_ledger:
            if item.status in required_treatment and not item.treatment_in_current_form.strip():
                raise ValueError(f"IntentLedgerItem {item.intent_id}: treatment_in_current_form obrigatório para {item.status.value}.")

        path_ids = [item.path_id for item in self.candidate_possibilities if item.path_id is not None]
        if len(path_ids) != len(set(path_ids)):
            raise ValueError("EvolutionArtifact: path_id duplicado em candidate_possibilities.")
        known_paths = set(path_ids)
        for possibility in self.candidate_possibilities:
            if len(possibility.intent_ids) != len(set(possibility.intent_ids)):
                raise ValueError(f"CandidatePossibility {possibility.path_id}: intent_id duplicado.")
            unknown = set(possibility.intent_ids) - known_intents
            if unknown:
                raise ValueError(f"CandidatePossibility {possibility.path_id}: intent_ids desconhecidos: {sorted(unknown)}.")

        for collection, label in ((self.useful_insights, "insight_id"), (self.open_decisions, "decision_id")):
            identifiers = [getattr(item, label) for item in collection]
            if len(identifiers) != len(set(identifiers)):
                raise ValueError(f"EvolutionArtifact: {label} duplicado.")
            for item in collection:
                unknown = set(item.related_intent_ids) - known_intents
                if unknown:
                    raise ValueError(f"{label} {getattr(item, label)}: intent_ids desconhecidos: {sorted(unknown)}.")

        for issue in self.coverage_issues:
            if issue.intent_id is not None and issue.intent_id not in known_intents:
                raise ValueError(f"CoverageIssue: intent_id desconhecido: {issue.intent_id}.")
            if issue.path_id is not None and issue.path_id not in known_paths:
                raise ValueError(f"CoverageIssue: path_id desconhecido: {issue.path_id}.")

        conflicts = {item.intent_id for item in self.intent_ledger if item.status == IntentTreatmentStatus.CONFLICT_FOUND}
        conflict_issues = [issue for issue in self.coverage_issues if issue.issue_type == CoverageIssueType.CONFLICT_FOUND]
        issue_conflicts = {issue.intent_id for issue in conflict_issues}
        if conflicts != issue_conflicts or any(issue.intent_id is None for issue in conflict_issues):
            raise ValueError("EvolutionArtifact: status CONFLICT_FOUND e coverage issue devem estar ligados de forma consistente.")

        if self.coverage_status == CoverageStatus.NOT_EVALUATED and self.coverage_issues:
            raise ValueError("EvolutionArtifact: NOT_EVALUATED não pode conter coverage_issues.")
        if self.coverage_status == CoverageStatus.NO_BLOCKING_GAP_DETECTED and self.coverage_issues:
            raise ValueError("EvolutionArtifact: NO_BLOCKING_GAP_DETECTED exige coverage_issues vazio.")
        if self.coverage_status == CoverageStatus.REPAIR_REQUIRED and not self.coverage_issues:
            raise ValueError("EvolutionArtifact: REPAIR_REQUIRED exige ao menos um coverage_issue.")
        if self.recommended_next_action_target_uncertainty is not None and self.recommended_next_action_target_uncertainty not in self.uncertainties:
            raise ValueError("EvolutionArtifact: ação aponta para incerteza que não existe em uncertainties.")

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


def validate_intent_source_quotes(original_idea: str, intent_ledger: List[IntentLedgerItem]) -> None:
    """Reject non-exact source anchors; this proves presence, not interpretation correctness."""
    for item in intent_ledger:
        if item.source_quote and item.source_quote not in original_idea:
            raise ValueError(f"IntentLedgerItem {item.intent_id}: source_quote não é substring exata de original_idea.")
        if item.origin_type == IntentOriginType.USER_EXPLICIT and not item.source_quote:
            raise ValueError(f"IntentLedgerItem {item.intent_id}: USER_EXPLICIT exige source_quote exata.")
