"""
src/idea_evolution/stages/understand.py
Estágio 1: UNDERSTAND (v0.1) — Extração de problema, intenção e premissas.
"""

from typing import Type
from src.idea_evolution.domain.state import SimpleIdeaState
from src.idea_evolution.stages.stage_base import BaseStage
from src.idea_evolution.stages.contracts import UnderstandOutput


class UnderstandStage(BaseStage):
    def __init__(self):
        super().__init__(
            stage_id="UNDERSTAND",
            stage_version="0.1.0",
            prompt_filename="understand_v0_1.md",
        )

    def build_prompt_context(self, state: SimpleIdeaState) -> str:
        template = self.load_prompt_template()
        return template.replace("{original_idea}", state.original_idea)

    def get_output_schema(self) -> Type[UnderstandOutput]:
        return UnderstandOutput

    def apply_output_to_state(self, state: SimpleIdeaState, output: UnderstandOutput) -> str:
        state.problem_statement = output.interpreted_problem
        state.human_intent = output.human_intent
        state.current_idea = output.structured_idea
        state.actors_or_users = output.actors_or_users
        state.assumptions = output.assumptions
        state.ambiguities = output.ambiguities
        state.strengths = output.strengths

        return f"Intenção extraída: '{output.human_intent[:60]}...' | {len(output.assumptions)} premissas mapeadas."
