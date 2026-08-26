"""
src/idea_evolution/stages/final_review.py
Estágio 6: FINAL_REVIEW (v0.1) — Detecção de essence drift, speculative accretion e verificação determinística de contradições ontológicas.
"""

from typing import Type
import json
from src.idea_evolution.domain.state import SimpleIdeaState, RunStatus
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
            f"- Mecanismo do Core: {state.core_mechanism} (Justificativa: {state.core_mechanism_justification})\n"
            f"- Extensões Candidatas: {cand_str}\n"
            f"- Propostas Rejeitadas: {rej_str}\n"
            f"- Riscos Conhecidos: {json.dumps(state.known_risks)}"
        )

    def get_output_schema(self) -> Type[FinalReviewOutput]:
        return FinalReviewOutput

    def apply_output_to_state(self, state: SimpleIdeaState, output: FinalReviewOutput) -> str:
        # 1. Verificação Determinística de Contradições Ontológicas
        ontology_contradiction = False
        contradiction_reasons = []

        # Contradição A: Mecanismo do Core não possui justificativa de promoção registrada
        if state.core_mechanism and not state.core_mechanism_justification:
            ontology_contradiction = True
            contradiction_reasons.append(f"Mecanismo '{state.core_mechanism}' promovido ao Core sem justificativa de promoção registrada.")

        # Contradição B: Item simultaneamente em Candidatas e Rejeitadas
        rejected_set = {r.proposal.strip().lower() for r in state.rejected_changes}
        for cand in state.candidate_extensions:
            if cand.strip().lower() in rejected_set:
                ontology_contradiction = True
                contradiction_reasons.append(f"Proposta '{cand}' aparece simultaneamente em candidate_extensions e rejected_changes.")

        # Contradição C: Dependências ou Testes do Core contendo propostas rejeitadas
        for rej in state.rejected_changes:
            rej_kw = rej.proposal.strip().lower()
            # Gera tokens significativos do item rejeitado (ex: "LLM", "Mind-Map", "Clarificação")
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
            state.remaining_uncertainties.append(f"ALERTA DE CONTRADIÇÃO ONTOLÓGICA: {'; '.join(contradiction_reasons)}")

        if output.essence_drift_detected or output.speculative_accretion_detected:
            state.remaining_uncertainties.append(f"ALERTA DE ESSENCE DRIFT / ACCRETION: {output.drift_explanation}")

        return f"Review Final: recomendação='{output.recommendation}', essence_drift={state.essence_drift_detected}, accretion={output.speculative_accretion_detected}, ontology_contradiction={state.ontology_contradiction_detected}."
