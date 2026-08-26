"""
src/idea_evolution/stages/synthesize.py
Estágio 5: SYNTHESIZE (v0.1) — Síntese estruturada, mudanças aceitas e rejeitadas.
"""

from typing import Type
import json
from src.idea_evolution.domain.state import SimpleIdeaState, RejectedProposal
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
            + f"\n\nContexto Atual:\n- Intenção: {state.human_intent}\n- Ideia Original: {state.original_idea}\n- Ideia Atual: {state.current_idea}\n- Issues: {issues_str}\n- Alternativas: {alt_str}"
        )

    def get_output_schema(self) -> Type[SynthesizeOutput]:
        return SynthesizeOutput

    def apply_output_to_state(self, state: SimpleIdeaState, output: SynthesizeOutput) -> str:
        state.current_idea = output.refined_idea
        state.core_mechanism = output.core_mechanism
        state.accepted_changes = output.accepted_changes
        state.candidate_extensions = output.candidate_possibilities
        state.rejected_changes = [
            RejectedProposal(
                proposal=r.proposal,
                reason_rejected=r.reason_rejected,
                source_stage=r.source_stage,
            )
            for r in output.rejected_changes
        ]
        state.remaining_uncertainties = output.remaining_uncertainties
        state.known_risks = output.known_risks
        state.recommended_next_step = output.recommended_next_step

        return f"Síntese concluída: {len(output.accepted_changes)} aceitas, {len(output.candidate_possibilities)} candidatas, {len(output.rejected_changes)} rejeitadas."
