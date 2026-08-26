"""
src/idea_evolution/stages/final_review.py
Estágio 6: FINAL_REVIEW (v0.1) — Detecção de essence drift, speculative accretion e verificação determinística de contradições ontológicas e cross-state invariants.
"""

from typing import Type
import json
from src.idea_evolution.domain.state import SimpleIdeaState, RunStatus, PromotionAuthorityBasis
from src.idea_evolution.stages.stage_base import BaseStage
from src.idea_evolution.stages.contracts import FinalReviewOutput


class FinalReviewStage(BaseStage):
    def __init__(self):
        super().__init__(
            stage_id="FINAL_REVIEW",
            stage_version="0.1.0",
            prompt_filename="final_review_v0_1.md",
        )

    def build_prompt_context(self, state: SimpleIdeaState) -> str:
        template = self.load_prompt_template()
        rej_str = json.dumps([r.proposal for r in state.rejected_changes])
        cand_str = json.dumps(state.candidate_extensions)
        return (
            template
            + f"\n\nComparação de Essência e Integridade Ontológica:\n"
            f"- Intenção Humana Original: {state.human_intent}\n"
            f"- Ideia Original Bruta: {state.original_idea}\n"
            f"- Ideia Refinada Sintetizada: {state.current_idea}\n"
            f"- Mecanismo do Core: {state.core_mechanism} (Justificativa: {state.core_mechanism_justification} | Base: {state.core_mechanism_basis.value})\n"
            f"- Core Testado no Reality Check: {state.tested_core_mechanism} (Hash Testado: {state.tested_core_hash} vs Hash Core: {state.core_mechanism_hash})\n"
            f"- Extensões Candidatas: {cand_str}\n"
            f"- Propostas Rejeitadas: {rej_str}\n"
            f"- Próximo Passo Recomendado: {state.recommended_next_step}\n"
            f"- Riscos Conhecidos: {json.dumps(state.known_risks)}"
        )

    def get_output_schema(self) -> Type[FinalReviewOutput]:
        return FinalReviewOutput

    def apply_output_to_state(self, state: SimpleIdeaState, output: FinalReviewOutput) -> str:
        # 1. Verificação Determinística de Invariantes Cross-State e Contradições Ontológicas
        ontology_contradiction = False
        contradiction_reasons = []

        # Invariante 1: Core aceito deve ser compatível com o core testado no RealityCheck
        if state.core_mechanism_hash and state.tested_core_hash:
            if state.core_mechanism_hash != state.tested_core_hash:
                # Se os hashes diferirem, verifica se há sobreposição semântica real
                core_norm = state.core_mechanism.strip().lower()
                tested_norm = state.tested_core_mechanism.strip().lower()
                if core_norm not in tested_norm and tested_norm not in core_norm:
                    ontology_contradiction = True
                    contradiction_reasons.append(
                        f"CORE_MISMATCH: O RealityCheck testou '{state.tested_core_mechanism}' (hash: {state.tested_core_hash}), "
                        f"mas o core aceito na Síntese é '{state.core_mechanism}' (hash: {state.core_mechanism_hash})."
                    )

        # Invariante 2: Mecanismo do Core não pode ser promovido isoladamente por MODEL_HYPOTHESIS
        if state.core_mechanism:
            if not state.core_mechanism_justification:
                ontology_contradiction = True
                contradiction_reasons.append(f"Mecanismo '{state.core_mechanism}' promovido ao Core sem justificativa registrada.")
            if state.core_mechanism_basis == PromotionAuthorityBasis.MODEL_HYPOTHESIS:
                ontology_contradiction = True
                contradiction_reasons.append(
                    f"CIRCULAR_PROMOTION: Mecanismo '{state.core_mechanism}' promovido ao Core tendo apenas MODEL_HYPOTHESIS como base de autoridade."
                )

        # Invariante 3: Item do Core não pode aparecer simultaneamente em testes exploratórios / não-core
        if state.core_mechanism:
            core_toks = [t for t in state.core_mechanism.lower().replace("-", " ").split() if len(t) >= 4 and t not in ["para", "com", "passo", "baseado"]]
            for exp_tst in state.exploratory_candidate_tests:
                if any(tok in exp_tst.lower() for tok in core_toks if len(tok) >= 4):
                    ontology_contradiction = True
                    contradiction_reasons.append(f"CORE_IN_EXPLORATORY: Mecanismo do Core '{state.core_mechanism}' aparece nos testes exploratórios '{exp_tst}'.")

        # Invariante 4: Proposta rejeitada não pode se tornar o recommended_next_step
        if state.recommended_next_step:
            next_step_lower = state.recommended_next_step.lower()
            for rej in state.rejected_changes:
                rej_toks = [t for t in rej.proposal.lower().replace("-", " ").split() if len(t) >= 4 and t not in ["para", "com", "sem", "uma", "dos", "das"]]
                if any(tok in next_step_lower for tok in rej_toks if len(tok) >= 4):
                    ontology_contradiction = True
                    contradiction_reasons.append(f"REJECTED_AS_NEXT_STEP: O próximo passo recomendado '{state.recommended_next_step}' propõe mecanismo rejeitado '{rej.proposal}'.")

        # Invariante 5: Proposta rejeitada não pode aparecer em candidate_extensions
        rejected_set = {r.proposal.strip().lower() for r in state.rejected_changes}
        for cand in state.candidate_extensions:
            if cand.strip().lower() in rejected_set:
                ontology_contradiction = True
                contradiction_reasons.append(f"Proposta '{cand}' aparece simultaneamente em candidate_extensions e rejected_changes.")

        # Invariante 6: Dependências ou Testes do Core referenciando mecanismos rejeitados
        for rej in state.rejected_changes:
            rej_kw = rej.proposal.strip().lower()
            tokens = [t for t in rej_kw.replace("-", " ").split() if len(t) >= 3 and t not in ["para", "com", "por", "sem", "uma", "dos", "das"]]
            
            for dep in state.reality_dependencies:
                dep_lower = dep.lower()
                if (rej_kw in dep_lower) or any(tok in dep_lower for tok in tokens if len(tok) >= 3):
                    ontology_contradiction = True
                    contradiction_reasons.append(f"Dependência de realidade do Core '{dep}' referencia mecanismo rejeitado '{rej.proposal}'.")
            
            for tst in state.candidate_tests:
                tst_lower = tst.lower()
                if (rej_kw in tst_lower) or any(tok in tst_lower for tok in tokens if len(tok) >= 3):
                    ontology_contradiction = True
                    contradiction_reasons.append(f"Teste do Core '{tst}' referencia mecanismo rejeitado '{rej.proposal}'.")

        state.ontology_contradiction_detected = output.ontology_contradiction_detected or ontology_contradiction
        state.essence_drift_detected = output.essence_drift_detected or output.speculative_accretion_detected or state.ontology_contradiction_detected
        state.speculative_accretion_detected = output.speculative_accretion_detected

        if contradiction_reasons:
            state.remaining_uncertainties.append(f"ALERTA DE CONTRADIÇÃO ONTOLÓGICA / CROSS-STATE: {'; '.join(contradiction_reasons)}")

        if output.essence_drift_detected or output.speculative_accretion_detected:
            state.remaining_uncertainties.append(f"ALERTA DE ESSENCE DRIFT / ACCRETION: {output.drift_explanation}")

        return f"Review Final: recomendação='{output.recommendation}', essence_drift={state.essence_drift_detected}, accretion={output.speculative_accretion_detected}, ontology_contradiction={state.ontology_contradiction_detected}."
