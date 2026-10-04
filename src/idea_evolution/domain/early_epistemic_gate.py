"""
src/idea_evolution/domain/early_epistemic_gate.py
Early Epistemic Gate, Contratos do Lean First Pass, Escalação Condicional e Registros de Decisão e Aluguel Epistêmico.
Implementação offline e desacoplada para a arquitetura Lean IEE L1 (FIOIDEIAS-LEAN-IEE-01).
"""

from __future__ import annotations
import hashlib
from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any, Tuple
from pydantic import BaseModel, Field, model_validator, PrivateAttr

from src.idea_evolution.domain.state import OntologyState, PromotionAuthorityBasis
from src.idea_evolution.domain.epistemic_contracts import SourceAnchor, SourceAnchorKind, NegativeKnowledgeRecord
from src.idea_evolution.domain.grounding import AuthorityProofValidator, GroundingRecord
from src.idea_evolution.domain.decision_relevance import (
    IdeaStage,
    RiskCategory,
    DecisionRelevance,
    AlternativeCategory,
    FalsificationCriterion,
    EngineeringRequirement,
    RequirementType,
    IdeaStageAssessment,
    IdeaStageGroundingPolicy,
    DecisionRelevancePolicy,
    FalsePrecisionGuard,
    NextActionArbitrationPolicy,
)


class GateOutcome(str, Enum):
    """Resultados possíveis da avaliação do Early Epistemic Gate (Custo de chamadas = 0)."""
    RETURN_NOW = "RETURN_NOW"
    ESCALATE_FOCUSED = "ESCALATE_FOCUSED"
    REQUEST_HUMAN_DECISION = "REQUEST_HUMAN_DECISION"
    PRESERVE_UNKNOWN = "PRESERVE_UNKNOWN"
    STOP_NO_USEFUL_WORK = "STOP_NO_USEFUL_WORK"


class EscalationReason(str, Enum):
    """Motivos tipados de escalação permitidos pelo Early Gate."""
    NONE = "NONE"
    MATERIAL_VULNERABILITY = "MATERIAL_VULNERABILITY"
    COMPETING_MECHANISMS = "COMPETING_MECHANISMS"
    REALITY_UNCERTAINTY = "REALITY_UNCERTAINTY"
    AMBIGUITY_RESOLUTION = "AMBIGUITY_RESOLUTION"


class EpistemicRentDecision(str, Enum):
    """Veredito de aluguel epistêmico para justificar um passo adicional."""
    JUSTIFIED = "JUSTIFIED"
    EXPLORATORY = "EXPLORATORY"  # Permite ideação aberta sob incerteza com budget limitado
    NOT_JUSTIFIED = "NOT_JUSTIFIED"
    UNKNOWN = "UNKNOWN"


class LeanCandidateMechanism(BaseModel):
    """Proposed candidate mechanism."""
    mechanism: str
    intent_ids: List[str] = Field(default_factory=list)
    is_explicit_in_source: bool = False
    claimed_basis: PromotionAuthorityBasis = PromotionAuthorityBasis.MODEL_HYPOTHESIS
    authority_proof_ref: str = ""
    justification: str = ""
    tradeoffs: List[str] = Field(default_factory=list)
    alternative_category: AlternativeCategory = AlternativeCategory.OTHER
    _gate_eligible: bool = PrivateAttr(default=False)

    @property
    def gate_eligible(self) -> bool:
        return self._gate_eligible

    @gate_eligible.setter
    def gate_eligible(self, value: bool) -> None:
        self._gate_eligible = value


class FirstPassIntentImportance(str, Enum):
    CORE_INTENT = "CORE_INTENT"
    MATERIAL_SUBINTENT = "MATERIAL_SUBINTENT"
    EXPLICIT_CONSTRAINT = "EXPLICIT_CONSTRAINT"


class FirstPassIntentOriginType(str, Enum):
    USER_EXPLICIT = "USER_EXPLICIT"
    MODEL_INTERPRETATION = "MODEL_INTERPRETATION"


class FirstPassIntentTreatmentStatus(str, Enum):
    PRESERVED = "PRESERVED"
    EXPANDED = "EXPANDED"
    PROVISIONALLY_MODIFIED = "PROVISIONALLY_MODIFIED"
    DEFERRED = "DEFERRED"
    CONFLICT_FOUND = "CONFLICT_FOUND"


class FirstPassIntentItem(BaseModel):
    """Model-produced intent claim, kept separate from its source authority."""

    intent_id: str = Field(min_length=1)
    source_quote: str
    interpretation: str
    # Plain strings keep the provider schema compact; validate_strong_maturation
    # enforces the same closed vocabularies before any artifact is created.
    importance: str
    origin_type: str
    treatment_in_current_form: str
    status: str


class GateAuthority(BaseModel):
    """Procedência compacta e reutilizável para conteúdo que pode influenciar um gate."""
    basis: PromotionAuthorityBasis = PromotionAuthorityBasis.MODEL_HYPOTHESIS
    support_ref: str = ""
    derivation: str = ""


def _compact_first_pass_schema(schema: Dict[str, Any]) -> None:
    """Remove metadados não semânticos para respeitar o limite do transporte strict."""
    def compact(node: Any) -> None:
        if isinstance(node, dict):
            node.pop("title", None)
            node.pop("description", None)
            node.pop("default", None)
            for value in node.values():
                compact(value)
        elif isinstance(node, list):
            for value in node:
                compact(value)

    compact(schema)


class LeanVulnerability(BaseModel):
    """Material vulnerability or risk."""
    vulnerability: str
    why_it_matters: str
    severity: str = "MEDIUM"  # HIGH | MEDIUM | LOW
    affected_aspect: str = ""
    category: RiskCategory = RiskCategory.UNKNOWN
    decision_relevance: DecisionRelevance = DecisionRelevance.UNKNOWN
    authority: GateAuthority = Field(default_factory=GateAuthority)
    _gate_eligible: bool = PrivateAttr(default=False)
    _effective_severity: str = PrivateAttr(default="UNCONFIRMED")

    @property
    def gate_eligible(self) -> bool:
        return self._gate_eligible

    @gate_eligible.setter
    def gate_eligible(self, value: bool) -> None:
        self._gate_eligible = value

    @property
    def effective_severity(self) -> str:
        return self._effective_severity

    @effective_severity.setter
    def effective_severity(self, value: str) -> None:
        self._effective_severity = value


class LeanFirstPassOutput(BaseModel):
    """Structured strong first-pass output; legacy constructors keep safe defaults."""
    interpreted_problem: str
    human_intent: str
    primary_mechanism: LeanCandidateMechanism
    current_form: str = ""
    intent_ledger: List[FirstPassIntentItem] = Field(default_factory=list)
    useful_insights: List[str] = Field(default_factory=list)
    open_decisions: List[str] = Field(default_factory=list)
    proposed_next_action_target_uncertainty: str = ""
    competing_alternatives: List[LeanCandidateMechanism] = Field(default_factory=list)
    key_assumptions: List[str] = Field(default_factory=list)
    material_ambiguities: List[str] = Field(default_factory=list)
    material_vulnerabilities: List[LeanVulnerability] = Field(default_factory=list)
    remaining_uncertainties: List[str] = Field(default_factory=list)
    uncertainty_authority: GateAuthority = Field(default_factory=GateAuthority)
    requires_human_normative_choice: bool = False
    human_choice_description: str = ""
    normative_authority: GateAuthority = Field(default_factory=GateAuthority)
    proposed_next_action: str = ""
    action_authority: GateAuthority = Field(default_factory=GateAuthority)
    idea_stage: IdeaStage = IdeaStage.UNKNOWN
    idea_stage_justification: str = ""
    falsification_criteria: List[FalsificationCriterion] = Field(default_factory=list)
    engineering_requirements: List[str] = Field(default_factory=list)
    _stage_assessment: Optional[IdeaStageAssessment] = PrivateAttr(default=None)
    _normative_gate_eligible: bool = PrivateAttr(default=False)
    _next_action_gate_eligible: bool = PrivateAttr(default=False)

    @classmethod
    def model_json_schema(cls, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        schema = super().model_json_schema(*args, **kwargs)
        _compact_first_pass_schema(schema)
        # These are required for live M2 generation even though defaults retain
        # compatibility for existing in-process gate/test constructors.
        required = schema.setdefault("required", [])
        for name in (
            "current_form",
            "intent_ledger",
            "useful_insights",
            "open_decisions",
            "proposed_next_action",
            "proposed_next_action_target_uncertainty",
        ):
            if name not in required:
                required.append(name)
        for definition in schema.get("$defs", {}).values():
            if definition.get("title") == "LeanCandidateMechanism" or "mechanism" in definition.get("properties", {}):
                mechanism_required = definition.setdefault("required", [])
                for name in ("intent_ids",):
                    if name not in mechanism_required:
                        mechanism_required.append(name)
        return schema

    def validate_strong_maturation(self, original_idea: str) -> None:
        """Fail closed on missing M2 structure, bad anchors, IDs, or references."""
        if not self.current_form.strip():
            raise ValueError("LEAN_FIRST_PASS exige current_form explícito e não vazio.")
        if not self.proposed_next_action.strip():
            raise ValueError("LEAN_FIRST_PASS exige proposed_next_action não vazio.")
        if not self.intent_ledger:
            raise ValueError("LEAN_FIRST_PASS exige intent_ledger material.")

        intent_ids = [item.intent_id for item in self.intent_ledger]
        if len(intent_ids) != len(set(intent_ids)):
            raise ValueError("LEAN_FIRST_PASS contém intent_id duplicado.")
        known_intents = set(intent_ids)
        for item in self.intent_ledger:
            try:
                FirstPassIntentImportance(item.importance)
                FirstPassIntentOriginType(item.origin_type)
                FirstPassIntentTreatmentStatus(item.status)
            except ValueError as exc:
                raise ValueError(f"IntentLedgerItem {item.intent_id}: enum M1/M2 inválido.") from exc
            quote = item.source_quote
            if item.origin_type == FirstPassIntentOriginType.USER_EXPLICIT and (not quote or quote not in original_idea):
                raise ValueError(f"IntentLedgerItem {item.intent_id}: USER_EXPLICIT exige source_quote exata da ideia original.")
            if quote and quote not in original_idea:
                raise ValueError(f"IntentLedgerItem {item.intent_id}: source_quote não é substring exata da ideia original.")
            if (
                item.status in {
                    FirstPassIntentTreatmentStatus.PRESERVED,
                    FirstPassIntentTreatmentStatus.EXPANDED,
                    FirstPassIntentTreatmentStatus.PROVISIONALLY_MODIFIED,
                    FirstPassIntentTreatmentStatus.CONFLICT_FOUND,
                }
                and not item.treatment_in_current_form.strip()
            ):
                raise ValueError(f"IntentLedgerItem {item.intent_id}: tratamento no current_form está ausente.")

        if not any(
            FirstPassIntentImportance(item.importance) == FirstPassIntentImportance.CORE_INTENT
            for item in self.intent_ledger
        ):
            raise ValueError("LEAN_FIRST_PASS intent_ledger deve representar CORE_INTENT.")

        paths = [self.primary_mechanism, *self.competing_alternatives]
        for path_index, path in enumerate(paths, start=1):
            if not path.intent_ids:
                raise ValueError(f"Candidate path {path_index} deve referenciar ao menos um intent_id.")
            if len(path.intent_ids) != len(set(path.intent_ids)):
                raise ValueError(f"Candidate path {path_index} contém intent_id duplicado.")
            unknown = set(path.intent_ids) - known_intents
            if unknown:
                raise ValueError(f"Candidate path {path_index} referencia intent_id desconhecido: {sorted(unknown)}.")

        if any(not insight.strip() for insight in self.useful_insights):
            raise ValueError("LEAN_FIRST_PASS useful_insights não pode conter itens vazios.")
        if any(not decision.strip() for decision in self.open_decisions):
            raise ValueError("LEAN_FIRST_PASS open_decisions não pode conter itens vazios.")

        known_uncertainties = set(self.remaining_uncertainties + self.material_ambiguities)
        target = self.proposed_next_action_target_uncertainty.strip()
        if known_uncertainties and not target:
            raise ValueError("LEAN_FIRST_PASS exige próximo passo vinculado a uma incerteza existente.")
        if target and target not in known_uncertainties:
            raise ValueError("LEAN_FIRST_PASS next action aponta para incerteza inexistente.")

    @property
    def stage_assessment(self) -> Optional[IdeaStageAssessment]:
        return self._stage_assessment

    @stage_assessment.setter
    def stage_assessment(self, value: Optional[IdeaStageAssessment]) -> None:
        self._stage_assessment = value

    @property
    def normative_gate_eligible(self) -> bool:
        return self._normative_gate_eligible

    @normative_gate_eligible.setter
    def normative_gate_eligible(self, value: bool) -> None:
        self._normative_gate_eligible = value

    @property
    def next_action_gate_eligible(self) -> bool:
        return self._next_action_gate_eligible

    @next_action_gate_eligible.setter
    def next_action_gate_eligible(self, value: bool) -> None:
        self._next_action_gate_eligible = value


class FocusedEscalationOutput(BaseModel):
    """
    Contrato Pydantic para o estágio FOCUSED_ESCALATION (máximo 1 chamada sob escalação).
    Focado estritamente na incerteza que justificou o aluguel epistêmico.
    """
    escalation_reason: EscalationReason
    target_hypothesis: str
    focused_critique_or_analysis: str = ""
    resolved_tradeoffs: List[str] = Field(default_factory=list)
    discriminating_tests: List[str] = Field(default_factory=list)
    hypothesis_mutated: bool = False
    mutated_hypothesis_description: str = ""
    decision_progress_made: bool = True
    updated_next_action: str = ""
    candidate_updated_next_action: Optional[str] = None
    action_authority: GateAuthority = Field(default_factory=GateAuthority)
    falsification_criteria: List[FalsificationCriterion] = Field(default_factory=list)
    _next_action_gate_eligible: bool = PrivateAttr(default=False)

    @model_validator(mode="after")
    def sync_candidate_next_action(self) -> FocusedEscalationOutput:
        """Sincroniza updated_next_action e candidate_updated_next_action bidirecionalmente."""
        if not self.candidate_updated_next_action and self.updated_next_action:
            self.candidate_updated_next_action = self.updated_next_action
        elif not self.updated_next_action and self.candidate_updated_next_action:
            self.updated_next_action = self.candidate_updated_next_action
        return self

    @property
    def next_action_gate_eligible(self) -> bool:
        return self._next_action_gate_eligible

    @next_action_gate_eligible.setter
    def next_action_gate_eligible(self, value: bool) -> None:
        self._next_action_gate_eligible = value


class DecisionDeltaEventType(str, Enum):
    """Tipos de eventos discretos de destravamento ou regressão da fronteira de decisão."""
    AMBIGUITY_RESOLVED = "AMBIGUITY_RESOLVED"
    ASSUMPTION_EXPOSED = "ASSUMPTION_EXPOSED"
    OPTION_ADDED = "OPTION_ADDED"
    OPTION_REJECTED = "OPTION_REJECTED"
    TEST_IDENTIFIED = "TEST_IDENTIFIED"
    HUMAN_DECISION_IDENTIFIED = "HUMAN_DECISION_IDENTIFIED"
    EVIDENCE_CHANGED_DECISION = "EVIDENCE_CHANGED_DECISION"
    FALSE_REQUIREMENT_PREVENTED = "FALSE_REQUIREMENT_PREVENTED"
    TENSION_CLARIFIED = "TENSION_CLARIFIED"
    NEXT_ACTION_CHANGED = "NEXT_ACTION_CHANGED"
    # Regressões Decisórias
    SOURCE_DRIFT_INCREASED = "SOURCE_DRIFT_INCREASED"
    UNSUPPORTED_REQUIREMENT_ADDED = "UNSUPPORTED_REQUIREMENT_ADDED"
    FALSE_CERTAINTY_CREATED = "FALSE_CERTAINTY_CREATED"
    VALID_OPTION_ERASED = "VALID_OPTION_ERASED"
    TENSION_SILENTLY_REMOVED = "TENSION_SILENTLY_REMOVED"


class DecisionDeltaRecord(BaseModel):
    """
    Registro estruturado de DecisionDelta (O que mudou que ajuda o humano a decidir o que fazer a seguir).
    NÃO é um score numérico artificial; é um registro factual de deltas.
    """
    delta_id: str
    delta_events: List[DecisionDeltaEventType] = Field(default_factory=list)
    before_uncertainties: List[str] = Field(default_factory=list)
    after_uncertainties: List[str] = Field(default_factory=list)
    resolved_items: List[str] = Field(default_factory=list)
    new_material_options: List[str] = Field(default_factory=list)
    rejected_options: List[str] = Field(default_factory=list)
    human_decision_required: bool = False
    next_action_changed: bool = False
    created_by_stage: str = "LEAN_FIRST_PASS"
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())


class EpistemicRentRecord(BaseModel):
    """
    Registro determinístico de justificação de custo de inferência adicional.
    EVERY ADDITIONAL CALL MUST HAVE AN EXPLICIT REASON.
    """
    record_id: str
    escalation_reason: EscalationReason
    expected_decision_delta: str
    additional_call_cost: int = 1
    rent_decision: EpistemicRentDecision = EpistemicRentDecision.JUSTIFIED
    justification_summary: str = ""
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())


class AttentionSnapshot(BaseModel):
    """
    Snapshot determinístico do campo global de atenção epistêmica A(X_t).
    Não é um resumo gerado por IA; é um objeto estruturado de dados observáveis.
    ATTENTION_SNAPSHOT != REALITY (Completeness status é sempre REPRESENTATION_ONLY).
    """
    snapshot_id: str
    source_anchor_refs: List[str] = Field(default_factory=list)
    material_claims_count: int = 0
    grounded_claims_count: int = 0
    ungrounded_claims_count: int = 0
    max_intermediary_depth: int = 0
    evidence_free_elaboration_count: int = 0
    authority_spoofing_detected: bool = False
    unresolved_tensions_count: int = 0
    source_refresh_required: bool = False
    attachment_risk_detected: bool = False
    drift_risk_vector: List[int] = Field(default_factory=list)
    completeness_status: str = "REPRESENTATION_ONLY"
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())



class MemoryAdmissionVerdict(str, Enum):
    ADMIT_NEGATIVE_KNOWLEDGE = "ADMIT_NEGATIVE_KNOWLEDGE"
    ADMIT_DONOR_KNOWLEDGE = "ADMIT_DONOR_KNOWLEDGE"
    ADMIT_HUMAN_DECISION = "ADMIT_HUMAN_DECISION"
    REJECT_EPHEMERAL_SPECULATION = "REJECT_EPHEMERAL_SPECULATION"


class MemoryAdmissionDecision(BaseModel):
    """
    Decisão determinística de admissão em memória institucional durável.
    CONVERSATION != DURABLE MEMORY.
    """
    decision: MemoryAdmissionVerdict
    candidate_content: str
    has_provenance: bool
    has_scope_and_reopen: bool
    has_decision_relevance: bool
    reason: str


class GateEvaluationResult(BaseModel):
    """Resultado da avaliação determinística do Early Epistemic Gate."""
    outcome: GateOutcome
    escalation_reason: EscalationReason = EscalationReason.NONE
    grounding_records: List[GroundingRecord] = Field(default_factory=list)
    authority_spoofing_detected: bool = False
    unsupported_candidate_count: int = 0
    negative_knowledge_match: Optional[str] = None
    rent_record: Optional[EpistemicRentRecord] = None
    attention_snapshot: Optional[AttentionSnapshot] = None
    explanation: str = ""
    escalation_risk_category: RiskCategory = RiskCategory.UNKNOWN
    stage_assessment: Optional[IdeaStageAssessment] = None
    ineligible_gate_claims: List[str] = Field(default_factory=list)



class EarlyEpistemicGate:
    """
    Portão Epistêmico Precoce Determinístico (Custo = 0 chamadas de IA).
    Avalia a saída da primeira passada e determina se a ideia pode retornar imediatamente,
    se exige autoridade humana ou se justifica exatamente 1 chamada de escalação focada.
    """

    @classmethod
    def evaluate(
        cls,
        source_anchor: SourceAnchor,
        first_pass: LeanFirstPassOutput,
        negative_knowledge_pool: Optional[List[NegativeKnowledgeRecord]] = None,
        human_intervention_flag: bool = False,
    ) -> GateEvaluationResult:
        if first_pass is None:
            raise ValueError("EarlyEpistemicGate.evaluate: first_pass cannot be None.")

        original_text = source_anchor.original_content
        grounding_records: List[GroundingRecord] = []
        authority_spoofing = False
        unsupported_count = 0
        ineligible_gate_claims: List[str] = []

        # 0. Ancoragem determinística de estágio operacional (Seções 9 a 13)
        stage_declared = getattr(first_pass, "idea_stage", IdeaStage.UNKNOWN)
        stage_just = getattr(first_pass, "idea_stage_justification", "")
        stage_assessment = IdeaStageGroundingPolicy.ground_stage(
            declared_stage=stage_declared,
            declared_justification=stage_just,
            source_text=original_text,
        )
        first_pass.stage_assessment = stage_assessment
        first_pass.idea_stage = stage_assessment.current_stage
        stage = stage_assessment.current_stage

        # 1. Auditar mecanismo primário contra autoridade e proveniência
        primary = first_pass.primary_mechanism
        audit_prim = AuthorityProofValidator.audit_gate_claim(
            original_idea=original_text,
            human_intent=first_pass.human_intent,
            proposition=primary.mechanism,
            claimed_basis=primary.claimed_basis,
            derivation_proof=primary.justification,
            authority_proof_ref=primary.authority_proof_ref,
            human_intervention_flag=human_intervention_flag,
        )
        grounding_records.append(audit_prim)
        primary.gate_eligible = audit_prim.is_valid

        if not audit_prim.is_valid:
            # Hipóteses continuam permitidas, mas permanecem contabilizadas como
            # elaboração sem âncora. Apenas bases elevadas inválidas são spoofing.
            if primary.claimed_basis in (PromotionAuthorityBasis.USER_EXPLICIT, PromotionAuthorityBasis.VALID_USER_DERIVATION):
                authority_spoofing = True
            unsupported_count += 1
            primary.claimed_basis = PromotionAuthorityBasis.MODEL_HYPOTHESIS

        # 2. Auditar alternativas concorrentes
        for alt in first_pass.competing_alternatives:
            audit_alt = AuthorityProofValidator.audit_gate_claim(
                original_idea=original_text,
                human_intent=first_pass.human_intent,
                proposition=alt.mechanism,
                claimed_basis=alt.claimed_basis,
                derivation_proof=alt.justification,
                authority_proof_ref=alt.authority_proof_ref,
                human_intervention_flag=human_intervention_flag,
            )
            grounding_records.append(audit_alt)
            alt.gate_eligible = audit_alt.is_valid
            if not audit_alt.is_valid:
                if alt.claimed_basis in (PromotionAuthorityBasis.USER_EXPLICIT, PromotionAuthorityBasis.VALID_USER_DERIVATION):
                    authority_spoofing = True
                unsupported_count += 1
                alt.claimed_basis = PromotionAuthorityBasis.MODEL_HYPOTHESIS

        # 3. Auditar a ação proposta antes que ela possa ser escolhida como ação final.
        if first_pass.proposed_next_action:
            action_audit = AuthorityProofValidator.audit_gate_claim(
                original_idea=original_text,
                human_intent=first_pass.human_intent,
                proposition=first_pass.proposed_next_action,
                claimed_basis=first_pass.action_authority.basis,
                derivation_proof=first_pass.action_authority.derivation,
                authority_proof_ref=first_pass.action_authority.support_ref,
                human_intervention_flag=human_intervention_flag,
            )
            grounding_records.append(action_audit)
            first_pass.next_action_gate_eligible = action_audit.is_valid
            if not action_audit.is_valid:
                ineligible_gate_claims.append(
                    f"NEXT_ACTION: {action_audit.failure_reason}"
                )
                if first_pass.action_authority.basis in (
                    PromotionAuthorityBasis.USER_EXPLICIT,
                    PromotionAuthorityBasis.VALID_USER_DERIVATION,
                ):
                    authority_spoofing = True
                    unsupported_count += 1
                first_pass.action_authority.basis = PromotionAuthorityBasis.MODEL_HYPOTHESIS

        # 4. Verificar se há correspondência com Conhecimento Negativo (Negative Knowledge)
        neg_match: Optional[str] = None
        if negative_knowledge_pool:
            all_mechs = [primary.mechanism] + [a.mechanism for a in first_pass.competing_alternatives]
            for nk in negative_knowledge_pool:
                for mech in all_mechs:
                    if nk.mechanism_or_claim.lower() in mech.lower() or mech.lower() in nk.mechanism_or_claim.lower():
                        neg_match = f"[{nk.record_id}] Mecanismo '{mech}' coincide com lição podada prévia: {nk.what_not_to_repeat}"
                        break
                if neg_match:
                    break

        # 5. Autoridade normativa exige claim auditada; flag/linguagem do modelo não bastam.
        normative_claimed = first_pass.requires_human_normative_choice or any(
            "normativo" in amb.lower() or "humano" in amb.lower()
            for amb in first_pass.material_ambiguities
        )
        if normative_claimed:
            normative_proposition = (
                first_pass.human_choice_description
                or next(
                    (amb for amb in first_pass.material_ambiguities if "normativo" in amb.lower() or "humano" in amb.lower()),
                    "Escolha normativa humana",
                )
            )
            normative_audit = AuthorityProofValidator.audit_gate_claim(
                original_idea=original_text,
                human_intent=first_pass.human_intent,
                proposition=normative_proposition,
                claimed_basis=first_pass.normative_authority.basis,
                derivation_proof=first_pass.normative_authority.derivation,
                authority_proof_ref=first_pass.normative_authority.support_ref,
                human_intervention_flag=human_intervention_flag,
            )
            grounding_records.append(normative_audit)
            first_pass.normative_gate_eligible = normative_audit.is_valid
            if not normative_audit.is_valid:
                ineligible_gate_claims.append(
                    f"NORMATIVE_CHOICE: {normative_audit.failure_reason}"
                )
                if first_pass.normative_authority.basis in (
                    PromotionAuthorityBasis.USER_EXPLICIT,
                    PromotionAuthorityBasis.VALID_USER_DERIVATION,
                ):
                    authority_spoofing = True
                    unsupported_count += 1
                first_pass.normative_authority.basis = PromotionAuthorityBasis.MODEL_HYPOTHESIS

        if normative_claimed and first_pass.normative_gate_eligible:
            return GateEvaluationResult(
                outcome=GateOutcome.REQUEST_HUMAN_DECISION,
                escalation_reason=EscalationReason.NONE,
                grounding_records=grounding_records,
                authority_spoofing_detected=authority_spoofing,
                unsupported_candidate_count=unsupported_count,
                negative_knowledge_match=neg_match,
                stage_assessment=stage_assessment,
                ineligible_gate_claims=ineligible_gate_claims,
                explanation="A transição exige escolha normativa/humana protegida. Mais raciocínio de IA não substitui autoridade humana.",
            )

        # 6. Vulnerabilidade só recebe severidade efetiva e relevância se sua procedência for elegível.
        escalatable_vulns: List[Tuple[LeanVulnerability, DecisionRelevance]] = []

        for v in first_pass.material_vulnerabilities:
            vuln_audit = AuthorityProofValidator.audit_gate_claim(
                original_idea=original_text,
                human_intent=first_pass.human_intent,
                proposition=v.vulnerability,
                claimed_basis=v.authority.basis,
                derivation_proof=v.authority.derivation or v.why_it_matters,
                authority_proof_ref=v.authority.support_ref,
                human_intervention_flag=human_intervention_flag,
            )
            grounding_records.append(vuln_audit)
            v.gate_eligible = vuln_audit.is_valid
            if not vuln_audit.is_valid:
                v.effective_severity = "UNCONFIRMED"
                v.decision_relevance = DecisionRelevance.UNKNOWN
                ineligible_gate_claims.append(
                    f"VULNERABILITY: {v.vulnerability} :: {vuln_audit.failure_reason}"
                )
                if v.authority.basis in (
                    PromotionAuthorityBasis.USER_EXPLICIT,
                    PromotionAuthorityBasis.VALID_USER_DERIVATION,
                ):
                    authority_spoofing = True
                    unsupported_count += 1
                v.authority.basis = PromotionAuthorityBasis.MODEL_HYPOTHESIS
                continue

            v.effective_severity = v.severity.upper()
            v_cat = getattr(v, "category", RiskCategory.UNKNOWN)
            if v_cat == RiskCategory.UNKNOWN:
                v_cat = DecisionRelevancePolicy.infer_category(v.vulnerability, v_cat)
                v.category = v_cat
            v_req_type = DecisionRelevancePolicy.infer_requirement_type(v.vulnerability, v_cat)
            rel = DecisionRelevancePolicy.evaluate_vulnerability_relevance(
                vulnerability_text=v.vulnerability,
                severity=v.severity,
                category=v_cat,
                stage=stage,
                original_idea=original_text,
                explicit_relevance=getattr(v, "decision_relevance", DecisionRelevance.UNKNOWN),
                requirement_type=v_req_type,
            )
            v.decision_relevance = rel
            if rel in (DecisionRelevance.CRITICAL_NOW, DecisionRelevance.HIGH_NOW):
                escalatable_vulns.append((v, rel))

        severe_vulns = [
            v for v in first_pass.material_vulnerabilities
            if v.gate_eligible and v.effective_severity in ("HIGH", "CRITICAL")
        ]

        if escalatable_vulns:
            target_vuln, target_rel = escalatable_vulns[0]
            target_cat = getattr(target_vuln, "category", RiskCategory.UNKNOWN)
            rent = EpistemicRentRecord(
                record_id=f"RENT-{hashlib.sha256(target_vuln.vulnerability.encode()).hexdigest()[:8]}",
                escalation_reason=EscalationReason.MATERIAL_VULNERABILITY,
                expected_decision_delta=f"Expor e mitigar incerteza crítica para decisão imediata ({target_rel.value}): {target_vuln.vulnerability}",
                additional_call_cost=1,
                rent_decision=EpistemicRentDecision.JUSTIFIED,
                justification_summary=f"Vulnerabilidade com relevância decisória imediata ({target_rel.value}) identificada para o estágio {stage.value}.",
            )
            return GateEvaluationResult(
                outcome=GateOutcome.ESCALATE_FOCUSED,
                escalation_reason=EscalationReason.MATERIAL_VULNERABILITY,
                grounding_records=grounding_records,
                authority_spoofing_detected=authority_spoofing,
                unsupported_candidate_count=unsupported_count,
                negative_knowledge_match=neg_match,
                rent_record=rent,
                escalation_risk_category=target_cat,
                stage_assessment=stage_assessment,
                ineligible_gate_claims=ineligible_gate_claims,
                explanation=f"Escalação justificada para crítica focada de vulnerabilidade com relevância decisória {target_rel.value} no estágio {stage.value}: {target_vuln.vulnerability}",
            )

        # 6. Avaliar múltiplos mecanismos técnicos concorrentes genuínos
        eligible_alternatives = [
            alternative for alternative in first_pass.competing_alternatives
            if alternative.gate_eligible and alternative.tradeoffs
        ]
        if primary.gate_eligible and eligible_alternatives:
            rent = EpistemicRentRecord(
                record_id=f"RENT-{hashlib.sha256(primary.mechanism.encode()).hexdigest()[:8]}",
                escalation_reason=EscalationReason.COMPETING_MECHANISMS,
                expected_decision_delta="Comparar trade-offs de mecanismos concorrentes para destravar escolha técnica.",
                additional_call_cost=1,
                rent_decision=EpistemicRentDecision.JUSTIFIED,
                justification_summary="Existem 2 ou mais mecanismos técnicos viáveis com trade-offs concorrentes.",
            )
            return GateEvaluationResult(
                outcome=GateOutcome.ESCALATE_FOCUSED,
                escalation_reason=EscalationReason.COMPETING_MECHANISMS,
                grounding_records=grounding_records,
                authority_spoofing_detected=authority_spoofing,
                unsupported_candidate_count=unsupported_count,
                negative_knowledge_match=neg_match,
                rent_record=rent,
                escalation_risk_category=RiskCategory.PRODUCT,
                stage_assessment=stage_assessment,
                ineligible_gate_claims=ineligible_gate_claims,
                explanation="Escalação justificada para comparação focada entre mecanismos concorrentes.",
            )

        # 7. Avaliar incertezas factuais ou de teste empírico (Reality Uncertainty)
        reality_uncertainty = next((
            uncertainty for uncertainty in first_pass.remaining_uncertainties
            if "factual" in uncertainty.lower()
            or "hardware" in uncertainty.lower()
            or "restrito" in uncertainty.lower()
        ), None)
        reality_uncertainty_eligible = False
        if reality_uncertainty:
            uncertainty_audit = AuthorityProofValidator.audit_gate_claim(
                original_idea=original_text,
                human_intent=first_pass.human_intent,
                proposition=reality_uncertainty,
                claimed_basis=first_pass.uncertainty_authority.basis,
                derivation_proof=first_pass.uncertainty_authority.derivation,
                authority_proof_ref=first_pass.uncertainty_authority.support_ref,
                human_intervention_flag=human_intervention_flag,
            )
            grounding_records.append(uncertainty_audit)
            reality_uncertainty_eligible = uncertainty_audit.is_valid
            if not uncertainty_audit.is_valid:
                ineligible_gate_claims.append(
                    f"REALITY_UNCERTAINTY: {uncertainty_audit.failure_reason}"
                )
                if first_pass.uncertainty_authority.basis in (
                    PromotionAuthorityBasis.USER_EXPLICIT,
                    PromotionAuthorityBasis.VALID_USER_DERIVATION,
                ):
                    authority_spoofing = True
                    unsupported_count += 1
                first_pass.uncertainty_authority.basis = PromotionAuthorityBasis.MODEL_HYPOTHESIS

        if reality_uncertainty and reality_uncertainty_eligible:
            rent = EpistemicRentRecord(
                record_id=f"RENT-{hashlib.sha256(original_text.encode()).hexdigest()[:8]}",
                escalation_reason=EscalationReason.REALITY_UNCERTAINTY,
                expected_decision_delta="Desenhar teste empírico ou discriminação factual para incerteza de hardware/realidade.",
                additional_call_cost=1,
                rent_decision=EpistemicRentDecision.JUSTIFIED,
                justification_summary="Incerteza factual/empírica profunda que exige delineamento de teste discriminativo.",
            )
            return GateEvaluationResult(
                outcome=GateOutcome.ESCALATE_FOCUSED,
                escalation_reason=EscalationReason.REALITY_UNCERTAINTY,
                grounding_records=grounding_records,
                authority_spoofing_detected=authority_spoofing,
                unsupported_candidate_count=unsupported_count,
                negative_knowledge_match=neg_match,
                rent_record=rent,
                escalation_risk_category=RiskCategory.TECHNICAL_FEASIBILITY,
                stage_assessment=stage_assessment,
                ineligible_gate_claims=ineligible_gate_claims,
                explanation="Escalação justificada para delineamento de teste empírico da realidade.",
            )

        # 8. Construir AttentionSnapshot determinístico A(X_t)
        total_claims = 1 + len(first_pass.competing_alternatives)
        grounded_count = total_claims - unsupported_count
        interm_depth = 1 if grounded_count > 0 else 2
        ev_free_count = 1 if unsupported_count > 0 else 0
        src_refresh = (interm_depth >= 2 and unsupported_count > 0)
        attach_risk = (ev_free_count >= 1 and len(first_pass.remaining_uncertainties) == 0 and len(severe_vulns) == 0)

        snapshot = AttentionSnapshot(
            snapshot_id=f"ATTN-{hashlib.sha256(original_text.encode()).hexdigest()[:8]}",
            source_anchor_refs=[source_anchor.source_id],
            material_claims_count=total_claims,
            grounded_claims_count=grounded_count,
            ungrounded_claims_count=unsupported_count,
            max_intermediary_depth=interm_depth,
            evidence_free_elaboration_count=ev_free_count,
            authority_spoofing_detected=authority_spoofing,
            unresolved_tensions_count=len(first_pass.material_ambiguities),
            source_refresh_required=src_refresh,
            attachment_risk_detected=attach_risk,
            drift_risk_vector=[unsupported_count, interm_depth, ev_free_count, len(first_pass.material_ambiguities), 1 if authority_spoofing else 0],
        )

        # Regra Fundamental de Contenção de Desperdício Epistêmico (Epistemic Waste Prevention):
        # A mera existência de hipóteses inventadas pelo modelo (unsupported_count > 0)
        # NÃO autoriza escalação nem outra chamada de modelo.
        return GateEvaluationResult(
            outcome=GateOutcome.RETURN_NOW,
            escalation_reason=EscalationReason.NONE,
            grounding_records=grounding_records,
            authority_spoofing_detected=authority_spoofing,
            unsupported_candidate_count=unsupported_count,
            negative_knowledge_match=neg_match,
            attention_snapshot=snapshot,
            stage_assessment=stage_assessment,
            ineligible_gate_claims=ineligible_gate_claims,
            explanation="Ideia suficientemente estruturada sem bloqueios críticos imediatos. Retorno imediato após 1 chamada.",
        )
