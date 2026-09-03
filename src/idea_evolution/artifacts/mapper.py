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
from src.idea_evolution.domain.state import SimpleIdeaState, PromotionAuthorityBasis
from src.idea_evolution.artifacts.evolution_artifact import (
    EvolutionArtifact,
    CritiqueItem,
    CandidatePossibility,
    TreatmentMode,
    FROZEN_LEAN_CORE_HASH,
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

        # 2. Ideia Refinada Canônica
        refined_idea = ""
        if escalation and escalation.hypothesis_mutated and escalation.mutated_hypothesis_description:
            refined_idea = escalation.mutated_hypothesis_description
        elif first_pass and first_pass.primary_mechanism and first_pass.primary_mechanism.mechanism:
            refined_idea = first_pass.primary_mechanism.mechanism
        else:
            refined_idea = orig_idea


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

        # 5. Premissas e Incertezas
        assumptions = list(first_pass.key_assumptions) if first_pass else []
        uncertainties: List[str] = []
        if first_pass:
            uncertainties.extend(first_pass.remaining_uncertainties)
            uncertainties.extend(first_pass.material_ambiguities)
            if first_pass.requires_human_normative_choice:
                desc = first_pass.human_choice_description or "Decisão normativa de valor humano necessária"
                uncertainties.append(f"Ponto de decisão humana: {desc}")

        # 6. Possibilidades Concorrentes (Garantia de Não-Autoridade)
        candidates: List[CandidatePossibility] = []
        if first_pass:
            for alt in first_pass.competing_alternatives:
                candidates.append(
                    CandidatePossibility(
                        mechanism=alt.mechanism,
                        authority_basis=PromotionAuthorityBasis.MODEL_HYPOTHESIS,
                        justification=alt.justification or "",
                        tradeoffs=list(alt.tradeoffs),
                    )
                )

        # 7. Próximo Passo Recomendado e Autoridade Normativa
        human_decision = lean_res.human_decision_requested or (
            first_pass is not None and first_pass.requires_human_normative_choice
        )
        human_desc = first_pass.human_choice_description if first_pass else None

        next_action = ""
        if human_decision:
            next_action = f"Decisão humana requerida: {human_desc or 'Definir preferência normativa antes de avançar.'}"
        elif escalation and escalation.updated_next_action:
            next_action = escalation.updated_next_action
        elif first_pass and first_pass.proposed_next_action:
            next_action = first_pass.proposed_next_action
        else:
            next_action = "Avaliar formulação refinada."

        return EvolutionArtifact(
            artifact_id=f"ART-{run_id}",
            run_id=run_id,
            treatment_mode=TreatmentMode.LEAN_L1,
            terminal_status=lean_res.terminal_status,
            original_idea=orig_idea,
            human_intent=human_intent,
            intent_provenance=intent_prov,
            refined_idea=refined_idea,
            what_changed=what_changed,
            critique=critique_items,
            assumptions=assumptions,
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
            human_intent=intent,
            intent_provenance=PromotionAuthorityBasis.VALID_USER_DERIVATION,
            refined_idea=refined,
            what_changed=[],  # Sem fabricação
            critique=critique_items,
            assumptions=[],   # Sem fabricação
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
        """
        critique_items: List[CritiqueItem] = []
        for issue in state.critical_issues:
            critique_items.append(
                CritiqueItem(
                    vulnerability=issue.issue,
                    severity=issue.severity.upper() if issue.severity else "MEDIUM",
                    why_it_matters=issue.why_it_matters or "",
                    affected_aspect=issue.affected_part or "",
                )
            )

        candidates: List[CandidatePossibility] = []
        for alt in state.alternatives:
            candidates.append(
                CandidatePossibility(
                    mechanism=alt.alternative_summary,
                    authority_basis=PromotionAuthorityBasis.MODEL_HYPOTHESIS,
                    justification=alt.why_considered or "",
                    tradeoffs=list(alt.pros_and_cons),
                )
            )

        changes = [c.change_description for c in state.accepted_changes]
        next_step = state.candidate_tests[0] if state.candidate_tests else "Revisar relatório de deliberação."

        return EvolutionArtifact(
            artifact_id=f"ART-{run_id}",
            run_id=run_id,
            treatment_mode=TreatmentMode.SUSPENDED_DEEP_LOOP,
            terminal_status=state.run_status.value,
            original_idea=state.original_idea,
            human_intent=state.human_intent or state.original_idea,
            intent_provenance=PromotionAuthorityBasis.VALID_USER_DERIVATION,
            refined_idea=state.current_idea or state.original_idea,
            what_changed=changes,
            critique=critique_items,
            assumptions=list(state.reality_dependencies),
            uncertainties=[],
            candidate_possibilities=candidates,
            recommended_next_action=next_step,
            human_decision_required=False,
            human_decision_description=None,
            source_anchor=None,
            scientific_core_hash=None,
            model_name=model_name,
            provider=provider,
            total_model_calls=state.reconstruction_attempts + 1,
        )
