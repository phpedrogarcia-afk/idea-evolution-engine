"""
src/idea_evolution/stages/alternatives.py
Estágio 3: ALTERNATIVES (v0.1) — Geração de 2 a 4 mecanismos causais alternativos.
"""

from typing import Type
import json
from src.idea_evolution.domain.state import SimpleIdeaState, AlternativeMechanism
from src.idea_evolution.stages.stage_base import BaseStage
from src.idea_evolution.stages.contracts import AlternativesOutput


class AlternativesStage(BaseStage):
    def __init__(self):
        super().__init__(
            stage_id="ALTERNATIVES",
            stage_version="0.1.0",
            prompt_filename="alternatives_v0_1.md",
        )

    def build_prompt_context(self, state: SimpleIdeaState) -> str:
        template = self.load_prompt_template()
        issues_str = json.dumps([ci.issue for ci in state.critical_issues])
        return (
            template.replace("{human_intent}", state.human_intent)
            .replace("{current_idea}", state.current_idea)
            .replace("{critical_issues}", issues_str)
        )

    def get_output_schema(self) -> Type[AlternativesOutput]:
        return AlternativesOutput

    def apply_output_to_state(self, state: SimpleIdeaState, output: AlternativesOutput) -> str:
        state.alternatives = [
            AlternativeMechanism(
                mechanism=alt.mechanism,
                addresses_issues=alt.addresses_issues,
                preserves_intent=alt.preserves_intent,
                tradeoffs=alt.tradeoffs,
                novelty_or_difference=alt.novelty_or_difference,
            )
            for alt in output.alternatives
        ]
        return f"{len(output.alternatives)} mecanismos alternativos gerados."
