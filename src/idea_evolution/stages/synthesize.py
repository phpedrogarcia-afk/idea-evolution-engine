"""
src/idea_evolution/stages/synthesize.py
Estágio 4 (na nova topologia): SYNTHESIZE (v0.1) — Síntese estruturada com validação determinística de autoridade (Grounding Validation) e linhagem referencial.
"""

from typing import Type
import json
import hashlib
from src.idea_evolution.domain.state import (
    SimpleIdeaState,
    RejectedProposal,
    ProposalRecord,
    OntologyState,
    PromotionAuthorityBasis,
)
from src.idea_evolution.domain.grounding import AuthorityProofValidator
from src.idea_evolution.stages.stage_base import BaseStage
from src.idea_evolution.stages.contracts import SynthesizeOutput


class SynthesizeStage(BaseStage):
    def __init__(self):
        super().__init__(
            stage_id="SYNTHESIZE",
            stage_version="0.1.0",
            prompt_filename="synthesize_v0_1.md",
        )

    def build_prompt_context(self, state: SimpleIdeaState) -> str:
        template = self.load_prompt_template()
        alt_str = json.dumps([{"mech": a.mechanism, "tradeoffs": a.tradeoffs} for a in state.alternatives])
        issues_str = json.dumps([ci.issue for ci in state.critical_issues])
        return (
            template
            + f"\n\nContexto Atual:\n- Intenção Humana: {state.human_intent}\n- Ideia Original: {state.original_idea}\n- Ideia Atual: {state.current_idea}\n- Issues Mapeadas: {issues_str}\n- Alternativas: {alt_str}"
        )

    def get_output_schema(self) -> Type[SynthesizeOutput]:
        return SynthesizeOutput

    def apply_output_to_state(self, state: SimpleIdeaState, output: SynthesizeOutput) -> str:
        state.current_idea = output.refined_idea
        state.core_mechanism = output.core_mechanism
        state.core_mechanism_justification = output.core_mechanism_justification

        # Mapeia basis de autoridade alegada para o Core
        try:
            claimed_basis = PromotionAuthorityBasis(output.core_mechanism_basis)
        except Exception:
            claimed_basis = PromotionAuthorityBasis.MODEL_HYPOTHESIS

        # 1. Auditoria Determinística de Autoridade do Core
        if output.core_mechanism:
            grounding_rec = AuthorityProofValidator.audit_proposal_authority(
                original_idea=state.original_idea,
                human_intent=state.human_intent,
                proposal=output.core_mechanism,
                claimed_basis=claimed_basis,
                justification=output.core_mechanism_justification,
                evidence_or_decision_basis=output.core_mechanism_justification,
                human_intervention_flag=state.human_intervention,
            )
            if not grounding_rec.is_valid:
                # Rebaixa para MODEL_HYPOTHESIS e registra o alerta
                state.core_mechanism_basis = PromotionAuthorityBasis.MODEL_HYPOTHESIS
                state.remaining_uncertainties.append(
                    f"AUTHORITY_SPOOFING_BLOCKED: A base alegada '{claimed_basis.value}' para o Core foi rejeitada pelo validador determinístico. Motivo: {grounding_rec.failure_reason}"
                )
            else:
                state.core_mechanism_basis = claimed_basis
        else:
            state.core_mechanism_basis = PromotionAuthorityBasis.MODEL_HYPOTHESIS

        # Computa hash referencial do core aceito
        if output.core_mechanism:
            state.core_mechanism_hash = hashlib.sha256(output.core_mechanism.strip().lower().encode("utf-8")).hexdigest()[:16]
        else:
            state.core_mechanism_hash = ""

        # Lista de propostas aceitas
        state.accepted_changes = [
            f"{item.proposal} (Justificativa: {item.promotion_reason} | Base: {item.promotion_basis})"
            for item in output.accepted_changes
        ]

        # Lista de rejeitados
        state.rejected_changes = [
            RejectedProposal(
                proposal=r.proposal,
                reason_rejected=r.reason_rejected,
                source_stage=r.source_stage,
            )
            for r in output.rejected_changes
        ]
        rejected_proposals_set = {r.proposal.strip().lower() for r in output.rejected_changes}

        # Candidatas: Exclusão estrita de qualquer item que já foi rejeitado
        cleaned_candidates = [
            cand for cand in output.candidate_possibilities
            if cand.strip().lower() not in rejected_proposals_set
        ]
        state.candidate_extensions = cleaned_candidates

        # Construção da linhagem estável ProposalRecord com auditoria de autoridade
        records = []
        if output.core_mechanism:
            records.append(
                ProposalRecord(
                    proposal=output.core_mechanism,
                    ontology_state=OntologyState.CORE if state.core_mechanism_basis != PromotionAuthorityBasis.MODEL_HYPOTHESIS else OntologyState.CANDIDATE,
                    source_stage="SYNTHESIZE",
                    promotion_reason=output.core_mechanism_justification,
                    promotion_basis=state.core_mechanism_basis,
                    evidence_or_decision_basis="Core design selection",
                )
            )
        for acc in output.accepted_changes:
            try:
                acc_claimed_basis = PromotionAuthorityBasis(acc.promotion_basis)
            except Exception:
                acc_claimed_basis = PromotionAuthorityBasis.MODEL_HYPOTHESIS

            acc_grounding = AuthorityProofValidator.audit_proposal_authority(
                original_idea=state.original_idea,
                human_intent=state.human_intent,
                proposal=acc.proposal,
                claimed_basis=acc_claimed_basis,
                justification=acc.promotion_reason,
                evidence_or_decision_basis=acc.evidence_or_decision_basis,
                human_intervention_flag=state.human_intervention,
            )
            validated_basis = acc_claimed_basis if acc_grounding.is_valid else PromotionAuthorityBasis.MODEL_HYPOTHESIS

            records.append(
                ProposalRecord(
                    proposal=acc.proposal,
                    ontology_state=OntologyState.DERIVED if acc_grounding.is_valid else OntologyState.CANDIDATE,
                    source_stage=acc.source_stage or "ALTERNATIVES",
                    promotion_reason=acc.promotion_reason,
                    promotion_basis=validated_basis,
                    evidence_or_decision_basis=acc.evidence_or_decision_basis,
                )
            )
        for cand in cleaned_candidates:
            records.append(
                ProposalRecord(
                    proposal=cand,
                    ontology_state=OntologyState.CANDIDATE,
                    source_stage="SYNTHESIZE",
                    promotion_basis=PromotionAuthorityBasis.MODEL_HYPOTHESIS,
                )
            )
        for rej in output.rejected_changes:
            records.append(
                ProposalRecord(
                    proposal=rej.proposal,
                    ontology_state=OntologyState.REJECTED,
                    source_stage=rej.source_stage or "SYNTHESIZE",
                    rejection_reason=rej.reason_rejected,
                )
            )
        state.proposal_records = records

        if output.remaining_uncertainties:
            state.remaining_uncertainties.extend(output.remaining_uncertainties)
        state.known_risks = output.known_risks
        state.recommended_next_step = output.recommended_next_step

        return f"Síntese concluída: Core '{output.core_mechanism[:40]}...' (Base: {state.core_mechanism_basis.value} | Hash: {state.core_mechanism_hash}), {len(output.accepted_changes)} aceitas, {len(cleaned_candidates)} candidatas, {len(output.rejected_changes)} rejeitadas."
