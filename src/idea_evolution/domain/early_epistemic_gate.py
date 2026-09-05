"""
src/idea_evolution/domain/early_epistemic_gate.py
Early Epistemic Gate, Contratos do Lean First Pass, Escalação Condicional e Registros de Decisão e Aluguel Epistêmico.
Implementação offline e desacoplada para a arquitetura Lean IEE L1 (FIOIDEIAS-LEAN-IEE-01).
"""

from __future__ import annotations
import hashlib
from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any
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
    is_explicit_in_source: bool = False
    claimed_basis: PromotionAuthorityBasis = PromotionAuthorityBasis.MODEL_HYPOTHESIS
    justification: str = ""
    tradeoffs: List[str] = Field(default_factory=list)
    alternative_category: AlternativeCategory = AlternativeCategory.OTHER


class LeanVulnerability(BaseModel):
    """Material vulnerability or risk."""
    vulnerability: str
    why_it_matters: str
    severity: str = "MEDIUM"  # HIGH | MEDIUM | LOW
    affected_aspect: str = ""
    category: RiskCategory = RiskCategory.UNKNOWN
    decision_relevance: DecisionRelevance = DecisionRelevance.UNKNOWN


class LeanFirstPassOutput(BaseModel):
    """Lean first pass output contract."""
    interpreted_problem: str
    human_intent: str
    primary_mechanism: LeanCandidateMechanism
    competing_alternatives: List[LeanCandidateMechanism] = Field(default_factory=list)
    key_assumptions: List[str] = Field(default_factory=list)
    material_ambiguities: List[str] = Field(default_factory=list)
    material_vulnerabilities: List[LeanVulnerability] = Field(default_factory=list)
    remaining_uncertainties: List[str] = Field(default_factory=list)
    requires_human_normative_choice: bool = False
    human_choice_description: str = ""
    proposed_next_action: str = ""
    idea_stage: IdeaStage = IdeaStage.UNKNOWN
    idea_stage_justification: str = ""
    falsification_criteria: List[FalsificationCriterion] = Field(default_factory=list)
    engineering_requirements: List[str] = Field(default_factory=list)
    _stage_assessment: Optional[IdeaStageAssessment] = PrivateAttr(default=None)

    @property
    def stage_assessment(self) -> Optional[IdeaStageAssessment]:
        return self._stage_assessment

    @stage_assessment.setter
    def stage_assessment(self, value: Optional[IdeaStageAssessment]) -> None:
        self._stage_assessment = value


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
    falsification_criteria: List[FalsificationCriterion] = Field(default_factory=list)

    @model_validator(mode="after")
    def sync_candidate_next_action(self) -> FocusedEscalationOutput:
        """Sincroniza updated_next_action e candidate_updated_next_action bidirecionalmente."""
        if not self.candidate_updated_next_action and self.updated_next_action:
            self.candidate_updated_next_action = self.updated_next_action
        elif not self.updated_next_action and self.candidate_updated_next_action:
            self.updated_next_action = self.candidate_updated_next_action
        return self


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
        audit_prim = AuthorityProofValidator.audit_proposal_authority(
            original_idea=original_text,
            human_intent=first_pass.human_intent,
            proposal=primary.mechanism,
            claimed_basis=primary.claimed_basis,
            justification=primary.justification,
            evidence_or_decision_basis="",
            human_intervention_flag=human_intervention_flag,
        )
        grounding_records.append(audit_prim)

        if not audit_prim.is_valid:
            # Se o modelo alegou USER_EXPLICIT ou dedução estrita sem fundamentação
            if primary.claimed_basis in (PromotionAuthorityBasis.USER_EXPLICIT, PromotionAuthorityBasis.VALID_USER_DERIVATION):
                authority_spoofing = True
            unsupported_count += 1
            primary.claimed_basis = PromotionAuthorityBasis.MODEL_HYPOTHESIS

        # 2. Auditar alternativas concorrentes
        for alt in first_pass.competing_alternatives:
            audit_alt = AuthorityProofValidator.audit_proposal_authority(
                original_idea=original_text,
                human_intent=first_pass.human_intent,
                proposal=alt.mechanism,
                claimed_basis=alt.claimed_basis,
                justification=alt.justification,
                evidence_or_decision_basis="",
                human_intervention_flag=human_intervention_flag,
            )
            grounding_records.append(audit_alt)
            if not audit_alt.is_valid:
                if alt.claimed_basis in (PromotionAuthorityBasis.USER_EXPLICIT, PromotionAuthorityBasis.VALID_USER_DERIVATION):
                    authority_spoofing = True
                unsupported_count += 1
                alt.claimed_basis = PromotionAuthorityBasis.MODEL_HYPOTHESIS

        # 3. Verificar se há correspondência com Conhecimento Negativo (Negative Knowledge)
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

        # 4. Verificar exigência de Autoridade Humana Normativa (Regra: Missing Human Authority -> STOP, No AI call)
        if first_pass.requires_human_normative_choice or any("normativo" in amb.lower() or "humano" in amb.lower() for amb in first_pass.material_ambiguities):
            return GateEvaluationResult(
                outcome=GateOutcome.REQUEST_HUMAN_DECISION,
                escalation_reason=EscalationReason.NONE,
                grounding_records=grounding_records,
                authority_spoofing_detected=authority_spoofing,
                unsupported_candidate_count=unsupported_count,
                negative_knowledge_match=neg_match,
                stage_assessment=stage_assessment,
                explanation="A transição exige escolha normativa/humana protegida. Mais raciocínio de IA não substitui autoridade humana.",
            )

        # 5. Avaliar vulnerabilidades com base em Relevância Decisória no Estágio (Severity != Priority)
        severe_vulns = [v for v in first_pass.material_vulnerabilities if v.severity.upper() == "HIGH"]
        escalatable_vulns: List[Tuple[LeanVulnerability, DecisionRelevance]] = []

        for v in first_pass.material_vulnerabilities:
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
                explanation=f"Escalação justificada para crítica focada de vulnerabilidade com relevância decisória {target_rel.value} no estágio {stage.value}: {target_vuln.vulnerability}",
            )

        # 6. Avaliar múltiplos mecanismos técnicos concorrentes genuínos
        if len(first_pass.competing_alternatives) >= 1 and any(len(a.tradeoffs) > 0 for a in first_pass.competing_alternatives):
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
                explanation="Escalação justificada para comparação focada entre mecanismos concorrentes.",
            )

        # 7. Avaliar incertezas factuais ou de teste empírico (Reality Uncertainty)
        if any("factual" in u.lower() or "hardware" in u.lower() or "restrito" in u.lower() for u in first_pass.remaining_uncertainties):
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
            explanation="Ideia suficientemente estruturada sem bloqueios críticos imediatos. Retorno imediato após 1 chamada.",
        )

