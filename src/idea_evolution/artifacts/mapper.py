"""
src/idea_evolution/artifacts/mapper.py
Mapeador Determinístico de Desfechos de Execução para EvolutionArtifact (M06 P2).

Transforma os resultados brutos da inferência científica em um artefato canônico de produto,
sem realizar nenhuma chamada de modelo adicional e sem fabricar campos epistêmicos.
"""

from __future__ import annotations
from typing import Optional, Dict, Any, List
from datetime import datetime

from src.idea_evolution.orchestration.lean_loop import LeanRunResult
from src.idea_evolution.domain.state import SimpleIdeaState, PromotionAuthorityBasis, OntologyState
from src.idea_evolution.domain.grounding import AuthorityProofValidator
from src.idea_evolution.artifacts.evolution_artifact import (
    EvolutionArtifact,
    CritiqueItem,
    CandidatePossibility,
    TreatmentMode,
    FROZEN_LEAN_CORE_HASH,
)
from src.idea_evolution.domain.decision_relevance import (
    IdeaStage,
    RiskCategory,
    DecisionRelevance,
    FalsePrecisionGuard,
    NextActionArbitrationPolicy,
    DecisionRelevancePolicy,
)


class EvolutionArtifactMapper:
    """Mapeia desfechos científicos para o schema de produto EvolutionArtifact."""

    @classmethod
    def map_lean_result(
        cls,
        lean_res: LeanRunResult,
        original_idea: Optional[str] = None,
        model_name: Optional[str] = None,
        provider: Optional[str] = None,
    ) -> EvolutionArtifact:
        """
        Mapeia deterministicamente um LeanRunResult para EvolutionArtifact.
        Custo = 0 chamadas de IA. Zero novos campos semânticos.
        """
        run_id = lean_res.run_id
        orig_idea = original_idea if original_idea is not None else lean_res.source_anchor.original_content
        first_pass = lean_res.first_pass
        escalation = lean_res.escalation_result

        # 1. Intenção Humana e Proveniência
        human_intent = first_pass.human_intent if first_pass else orig_idea
        intent_prov = (
            PromotionAuthorityBasis.VALID_USER_DERIVATION
            if first_pass
            else PromotionAuthorityBasis.USER_EXPLICIT
        )

        # 2. Ideia Refinada Canônica (Separação entre Refinamento de Produto e Requisito Técnico)
        stage = getattr(first_pass, "idea_stage", IdeaStage.UNKNOWN) if first_pass else IdeaStage.UNKNOWN
        base_mechanism = (
            first_pass.primary_mechanism.mechanism
            if first_pass and first_pass.primary_mechanism and first_pass.primary_mechanism.mechanism
            else orig_idea
        )
        deferred_security_requirement: Optional[str] = None

        refined_idea = ""
        if escalation and escalation.hypothesis_mutated and escalation.mutated_hypothesis_description:
            # Em descoberta/validação, não permite que controles técnicos/segurança mutem a hipótese de produto
            if (
                stage in (IdeaStage.DISCOVERY, IdeaStage.VALIDATION, IdeaStage.UNKNOWN)
                and DecisionRelevancePolicy.is_engineering_security_override(
                    escalation.mutated_hypothesis_description, base_mechanism
                )
                and not DecisionRelevancePolicy.is_user_explicit_security_request(orig_idea)
            ):
                refined_idea = base_mechanism
                deferred_security_requirement = escalation.mutated_hypothesis_description
            else:
                refined_idea = escalation.mutated_hypothesis_description
        elif first_pass and first_pass.primary_mechanism and first_pass.primary_mechanism.mechanism:
            refined_idea = first_pass.primary_mechanism.mechanism
        else:
            refined_idea = orig_idea

        # Sanitização de precisão numérica sem evidência declarada
        sanitized_refined, _ = FalsePrecisionGuard.sanitize_unsupported_precision(refined_idea, source_text=orig_idea)
        refined_idea = sanitized_refined


        # 3. O Que Mudou (Deltas Estruturais)
        what_changed: List[str] = []
        if lean_res.decision_delta:
            delta = lean_res.decision_delta
            if delta.resolved_items:
                what_changed.extend([f"Item resolvido: {item}" for item in delta.resolved_items])
            if delta.new_material_options:
                what_changed.extend([f"Nova opção: {opt}" for opt in delta.new_material_options])
            if delta.rejected_options:
                what_changed.extend([f"Opção descartada: {opt}" for opt in delta.rejected_options])
            if delta.next_action_changed:
                what_changed.append("Próximo passo atualizado pela análise.")
        if escalation and escalation.decision_progress_made and escalation.focused_critique_or_analysis:
            what_changed.append(f"Crítica focada: {escalation.focused_critique_or_analysis}")


        # 4. Crítica e Vulnerabilidades
        critique_items: List[CritiqueItem] = []
        if first_pass:
            for v in first_pass.material_vulnerabilities:
                critique_items.append(
                    CritiqueItem(
                        vulnerability=v.vulnerability,
                        severity=v.severity.upper() if v.severity else "MEDIUM",
                        why_it_matters=v.why_it_matters or "",
                        affected_aspect=v.affected_aspect or "",
                    )
                )
        if escalation and escalation.focused_critique_or_analysis:
            sev = "HIGH" if escalation.escalation_reason.value == "MATERIAL_VULNERABILITY" else "MEDIUM"
            critique_items.append(
                CritiqueItem(
                    vulnerability=f"Análise focada ({escalation.escalation_reason.value}): {escalation.focused_critique_or_analysis}",
                    severity=sev,
                    why_it_matters="Aprofundamento resultante de escalação epistêmica disparada pelo Gate.",
                    affected_aspect="Focalização",
                )
            )
        if deferred_security_requirement:
            critique_items.append(
                CritiqueItem(
                    vulnerability=f"Requisito Técnico/Segurança Identificado: {deferred_security_requirement}",
                    severity="HIGH",
                    why_it_matters="Requisito de engenharia preservado como especificação técnica sem descaracterizar a proposta de produto em estágio inicial.",
                    affected_aspect="Segurança / Infraestrutura",
                )
            )

        # 5. Premissas e Incertezas
        assumptions = list(first_pass.key_assumptions) if first_pass else []
        uncertainties: List[str] = []
        if first_pass:
            uncertainties.extend(first_pass.remaining_uncertainties)
            uncertainties.extend(first_pass.material_ambiguities)
            if first_pass.requires_human_normative_choice:
                desc = first_pass.human_choice_description or "Decisão normativa de valor humano necessária"
                uncertainties.append(f"Ponto de decisão humana: {desc}")

        # 6. Possibilidades Concorrentes (Garantia de Não-Autoridade e Preservação de Status)
        candidates: List[CandidatePossibility] = []
        rejected_options = []
        if lean_res.decision_delta and lean_res.decision_delta.rejected_options:
            rejected_options = [r.lower() for r in lean_res.decision_delta.rejected_options]

        if first_pass:
            for alt in first_pass.competing_alternatives:
                is_rejected = any(
                    alt.mechanism.lower() in rej or rej in alt.mechanism.lower()
                    for rej in rejected_options
                )
                candidates.append(
                    CandidatePossibility(
                        mechanism=alt.mechanism,
                        authority_basis=PromotionAuthorityBasis.MODEL_HYPOTHESIS,
                        ontology_state=OntologyState.REJECTED if is_rejected else OntologyState.CANDIDATE,
                        justification=alt.justification or "",
                        tradeoffs=list(alt.tradeoffs),
                    )
                )

        # 7. Próximo Passo Recomendado e Autoridade Normativa (Arbitragem Determinística)
        human_decision = lean_res.human_decision_requested or (
            first_pass is not None and first_pass.requires_human_normative_choice
        )
        human_desc = first_pass.human_choice_description if first_pass else None

        next_action = ""
        if human_decision:
            next_action = f"Decisão humana requerida: {human_desc or 'Definir preferência normativa antes de avançar.'}"
        else:
            fp_action = first_pass.proposed_next_action if first_pass else ""
            esc_action = escalation.updated_next_action if escalation else None
            next_action, _ = NextActionArbitrationPolicy.arbitrate(
                first_pass_next_action=fp_action,
                escalation_candidate_next_action=esc_action,
                stage=stage,
                original_idea=orig_idea,
                requires_human_decision=human_decision,
                human_decision_description=human_desc,
            )
            if not next_action:
                next_action = "Avaliar formulação refinada."

        return EvolutionArtifact(
            artifact_id=f"ART-{run_id}",
            run_id=run_id,
            treatment_mode=TreatmentMode.LEAN_L1,
            terminal_status=lean_res.terminal_status,
            original_idea=orig_idea,
            original_idea_authority=PromotionAuthorityBasis.USER_EXPLICIT,
            human_intent=human_intent,
            intent_provenance=intent_prov,
            refined_idea=refined_idea,
            refined_idea_authority=PromotionAuthorityBasis.MODEL_HYPOTHESIS,
            what_changed=what_changed,
            critique=critique_items,
            assumptions=assumptions,
            assumptions_authority=PromotionAuthorityBasis.MODEL_HYPOTHESIS,
            uncertainties=uncertainties,
            candidate_possibilities=candidates,
            recommended_next_action=next_action,
            human_decision_required=human_decision,
            human_decision_description=human_desc,
            source_anchor=lean_res.source_anchor,
            scientific_core_hash=FROZEN_LEAN_CORE_HASH,
            model_name=model_name,
            provider=provider,
            total_model_calls=lean_res.total_model_calls,
        )

    @classmethod
    def map_baseline_result(
        cls,
        baseline_data: Dict[str, Any],
        original_idea: str,
        run_id: str,
        model_name: Optional[str] = None,
        provider: Optional[str] = None,
    ) -> EvolutionArtifact:
        """
        Mapeia a saída da Condição A (Baseline) sem fabricar campos ausentes.
        """
        parsed = baseline_data.get("parsed_output", {})
        refined = parsed.get("refined_version", original_idea)
        intent = parsed.get("summary", original_idea)
        next_step = parsed.get("next_step", "")

        critique_items: List[CritiqueItem] = []
        for t in parsed.get("tradeoffs", []):
            critique_items.append(
                CritiqueItem(
                    vulnerability=t,
                    severity="MEDIUM",
                    why_it_matters="Identificado no refinamento de prompt único.",
                    affected_aspect="Trade-off",
                )
            )

        return EvolutionArtifact(
            artifact_id=f"ART-{run_id}",
            run_id=run_id,
            treatment_mode=TreatmentMode.FAST_FALLBACK,
            terminal_status="COMPLETED" if baseline_data.get("success", False) else "BASELINE_FAILED",
            original_idea=original_idea,
            original_idea_authority=PromotionAuthorityBasis.USER_EXPLICIT,
            human_intent=intent,
            intent_provenance=PromotionAuthorityBasis.VALID_USER_DERIVATION,
            refined_idea=refined,
            refined_idea_authority=PromotionAuthorityBasis.MODEL_HYPOTHESIS,
            what_changed=[],  # Sem fabricação
            critique=critique_items,
            assumptions=[],   # Sem fabricação
            assumptions_authority=PromotionAuthorityBasis.MODEL_HYPOTHESIS,
            uncertainties=[], # Sem fabricação
            candidate_possibilities=[], # Sem fabricação
            recommended_next_action=next_step,
            human_decision_required=False,
            human_decision_description=None,
            source_anchor=None,
            scientific_core_hash=None,
            model_name=model_name,
            provider=provider,
            total_model_calls=1,
        )

    @classmethod
    def map_simple_state(
        cls,
        state: SimpleIdeaState,
        run_id: str,
        model_name: Optional[str] = None,
        provider: Optional[str] = None,
    ) -> EvolutionArtifact:
        """
        Mapeia a Condição B (Simple Loop) para pesquisa interna/experimental isolada.
        Garante que tentativas de spoofing de autoridade nos registros internos de proposta
        sejam contidas na fronteira de produto.
        """
        critique_items: List[CritiqueItem] = []
        for issue in state.critical_issues:
            critique_items.append(
                CritiqueItem(
                    vulnerability=issue.issue,
                    severity=issue.severity.upper() if issue.severity else "MEDIUM",
                    why_it_matters=issue.why_it_matters or "",
                    affected_aspect=issue.affected_part or "",
                    authority_basis=PromotionAuthorityBasis.MODEL_HYPOTHESIS,
                )
            )

        candidates: List[CandidatePossibility] = []
        for alt in state.alternatives:
            candidates.append(
                CandidatePossibility(
                    mechanism=alt.mechanism,
                    authority_basis=PromotionAuthorityBasis.MODEL_HYPOTHESIS,
                    ontology_state=OntologyState.CANDIDATE,
                    justification=alt.novelty_or_difference or "",
                    tradeoffs=list(alt.tradeoffs),
                )
            )

        # Auditoria determinística de propostas para conter spoofing antes de entrar no artefato
        for p in state.proposal_records:
            if p.promotion_basis == PromotionAuthorityBasis.USER_EXPLICIT:
                is_valid, _, _ = AuthorityProofValidator.validate_user_explicit(state.original_idea, p.proposal)
                if not is_valid:
                    # Contenção de spoofing: demove deterministamente para MODEL_HYPOTHESIS
                    p.promotion_basis = PromotionAuthorityBasis.MODEL_HYPOTHESIS

        changes = list(state.accepted_changes)
        next_step = state.candidate_tests[0] if state.candidate_tests else "Revisar relatório de deliberação."

        return EvolutionArtifact(
            artifact_id=f"ART-{run_id}",
            run_id=run_id,
            treatment_mode=TreatmentMode.SUSPENDED_DEEP_LOOP,
            terminal_status=state.status.value if hasattr(state, "status") else getattr(state, "run_status", "COMPLETED"),
            original_idea=state.original_idea,
            original_idea_authority=PromotionAuthorityBasis.USER_EXPLICIT,
            human_intent=state.human_intent or state.original_idea,
            intent_provenance=PromotionAuthorityBasis.VALID_USER_DERIVATION,
            refined_idea=state.current_idea or state.original_idea,
            refined_idea_authority=PromotionAuthorityBasis.MODEL_HYPOTHESIS,
            what_changed=changes,
            critique=critique_items,
            assumptions=list(state.reality_dependencies),
            assumptions_authority=PromotionAuthorityBasis.MODEL_HYPOTHESIS,
            uncertainties=[],
            candidate_possibilities=candidates,
            recommended_next_action=next_step,
            human_decision_required=False,
            human_decision_description=None,
            source_anchor=None,
            scientific_core_hash=None,
            model_name=model_name,
            provider=provider,
            total_model_calls=getattr(state, "reconstruction_count", 0) + 1,
        )
