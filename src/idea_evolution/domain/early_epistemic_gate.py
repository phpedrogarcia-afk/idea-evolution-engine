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
from pydantic import BaseModel, Field

from src.idea_evolution.domain.state import OntologyState, PromotionAuthorityBasis
from src.idea_evolution.domain.epistemic_contracts import SourceAnchor, SourceAnchorKind, NegativeKnowledgeRecord
from src.idea_evolution.domain.grounding import AuthorityProofValidator, GroundingRecord


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
    NOT_JUSTIFIED = "NOT_JUSTIFIED"
    UNKNOWN = "UNKNOWN"


class LeanCandidateMechanism(BaseModel):
    """Mecanismo ou hipótese proposta na primeira passada."""
    mechanism: str
    is_explicit_in_source: bool = False
    claimed_basis: PromotionAuthorityBasis = PromotionAuthorityBasis.MODEL_HYPOTHESIS
    justification: str = ""
    tradeoffs: List[str] = Field(default_factory=list)


class LeanVulnerability(BaseModel):
    """Vulnerabilidade ou risco material identificado na primeira passada."""
    vulnerability: str
    why_it_matters: str
    severity: str = "MEDIUM"  # HIGH | MEDIUM | LOW
    affected_aspect: str = ""


class LeanFirstPassOutput(BaseModel):
    """
    Contrato Pydantic para o estágio LEAN_FIRST_PASS (1 chamada de modelo).
    Mapeia a interpretação mínima estruturada sem inchaço multiestágio.
    """
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


class DecisionDeltaRecord(BaseModel):
    """
    Registro estruturado de DecisionDelta (O que mudou que ajuda o humano a decidir o que fazer a seguir).
    NÃO é um score numérico artificial; é um registro factual de deltas.
    """
    delta_id: str
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


class GateEvaluationResult(BaseModel):
    """Resultado da avaliação determinística do Early Epistemic Gate."""
    outcome: GateOutcome
    escalation_reason: EscalationReason = EscalationReason.NONE
    grounding_records: List[GroundingRecord] = Field(default_factory=list)
    authority_spoofing_detected: bool = False
    unsupported_candidate_count: int = 0
    negative_knowledge_match: Optional[str] = None
    rent_record: Optional[EpistemicRentRecord] = None
    explanation: str = ""


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
        original_text = source_anchor.original_content
        grounding_records: List[GroundingRecord] = []
        authority_spoofing = False
        unsupported_count = 0

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
                explanation="A transição exige escolha normativa/humana protegida. Mais raciocínio de IA não substitui autoridade humana.",
            )

        # 5. Avaliar vulnerabilidades materiais severas (HIGH severity)
        severe_vulns = [v for v in first_pass.material_vulnerabilities if v.severity.upper() == "HIGH"]
        if severe_vulns:
            rent = EpistemicRentRecord(
                record_id=f"RENT-{hashlib.sha256(severe_vulns[0].vulnerability.encode()).hexdigest()[:8]}",
                escalation_reason=EscalationReason.MATERIAL_VULNERABILITY,
                expected_decision_delta=f"Expor e mitigar falha crítica: {severe_vulns[0].vulnerability}",
                additional_call_cost=1,
                rent_decision=EpistemicRentDecision.JUSTIFIED,
                justification_summary="Vulnerabilidade severa identificada cujo teste ou crítica focada altera diretamente o próximo passo humano.",
            )
            return GateEvaluationResult(
                outcome=GateOutcome.ESCALATE_FOCUSED,
                escalation_reason=EscalationReason.MATERIAL_VULNERABILITY,
                grounding_records=grounding_records,
                authority_spoofing_detected=authority_spoofing,
                unsupported_candidate_count=unsupported_count,
                negative_knowledge_match=neg_match,
                rent_record=rent,
                explanation=f"Escalação justificada para crítica focada de vulnerabilidade HIGH: {severe_vulns[0].vulnerability}",
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
                explanation="Escalação justificada para delineamento de teste empírico da realidade.",
            )

        # 8. Regra Fundamental de Contenção de Desperdício Epistêmico (Epistemic Waste Prevention):
        # A mera existência de hipóteses inventadas pelo modelo (unsupported_count > 0)
        # NÃO autoriza escalação nem outra chamada de modelo.
        return GateEvaluationResult(
            outcome=GateOutcome.RETURN_NOW,
            escalation_reason=EscalationReason.NONE,
            grounding_records=grounding_records,
            authority_spoofing_detected=authority_spoofing,
            unsupported_candidate_count=unsupported_count,
            negative_knowledge_match=neg_match,
            explanation="Ideia suficientemente estruturada sem bloqueios críticos imediatos. Retorno imediato após 1 chamada.",
        )
