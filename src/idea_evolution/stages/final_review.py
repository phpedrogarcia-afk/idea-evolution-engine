"""
src/idea_evolution/stages/final_review.py
Estágio 6: FINAL_REVIEW (v0.1) — Detecção de essence drift e verificação final.
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
        return (
            template
            + f"\n\nComparação de Essência:\n- Intenção Humana Original: {state.human_intent}\n- Ideia Original Bruta: {state.original_idea}\n- Ideia Refinada Sintetizada: {state.current_idea}\n- Riscos Conhecidos: {json.dumps(state.known_risks)}"
        )

    def get_output_schema(self) -> Type[FinalReviewOutput]:
        return FinalReviewOutput

    def apply_output_to_state(self, state: SimpleIdeaState, output: FinalReviewOutput) -> str:
        state.essence_drift_detected = output.essence_drift_detected

        if output.essence_drift_detected:
            state.remaining_uncertainties.append(f"ALERTA DE ESSENCE DRIFT: {output.drift_explanation}")

        return f"Review Final: recomendação='{output.recommendation}', essence_drift={output.essence_drift_detected}."
