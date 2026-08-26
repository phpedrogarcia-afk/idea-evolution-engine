"""
src/idea_evolution/stages/revision.py
Estágio de Revisão Evolutiva Intermediária para a Condição C.
"""

from typing import Type
import json
from src.idea_evolution.domain.state import SimpleIdeaState
from src.idea_evolution.stages.stage_base import BaseStage
from src.idea_evolution.stages.contracts import RevisionOutput


class RevisionStage(BaseStage):
    def __init__(self, revision_index: int = 1):
        super().__init__(
            stage_id=f"REVISION_{revision_index}",
            stage_version="0.1.0",
            prompt_filename="revision_v0_1.md",
        )
        self.revision_index = revision_index

    def build_prompt_context(self, state: SimpleIdeaState) -> str:
        template = self.load_prompt_template()
        issues_summary = [f"- [{ci.severity}] {ci.issue}" for ci in state.critical_issues]
        return (
            template
            + f"\n\nIntenção Humana:\n{state.human_intent}\n\nVersão Atual da Ideia:\n{state.current_idea}\n\nCríticas a Responder:\n"
            + "\n".join(issues_summary)
        )

    def get_output_schema(self) -> Type[RevisionOutput]:
        return RevisionOutput

    def apply_output_to_state(self, state: SimpleIdeaState, output: RevisionOutput) -> str:
        state.current_idea = output.revised_idea
        state.accepted_changes.extend(output.changes_applied)
        return f"Revisão #{self.revision_index}: {len(output.changes_applied)} melhorias incorporadas."
