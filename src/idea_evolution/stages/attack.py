"""
src/idea_evolution/stages/attack.py
Estágio 2: ATTACK (v0.1) — Crítica adversarial severa e vulnerabilidades.
"""

from typing import Type
import json
from src.idea_evolution.domain.state import SimpleIdeaState, CriticalIssue
from src.idea_evolution.stages.stage_base import BaseStage
from src.idea_evolution.stages.contracts import AttackOutput


class AttackStage(BaseStage):
    def __init__(self):
        super().__init__(
            stage_id="ATTACK",
            stage_version="0.1.0",
            prompt_filename="attack_v0_1.md",
        )

    def build_prompt_context(self, state: SimpleIdeaState) -> str:
        template = self.load_prompt_template()
        return (
            template.replace("{original_idea}", state.original_idea)
            .replace("{structured_idea}", state.current_idea)
            .replace("{assumptions}", json.dumps(state.assumptions))
            .replace("{proposed_mechanism}", state.problem_statement)
        )

    def get_output_schema(self) -> Type[AttackOutput]:
        return AttackOutput

    def apply_output_to_state(self, state: SimpleIdeaState, output: AttackOutput) -> str:
        state.critical_issues = [
            CriticalIssue(
                issue=ci.issue,
                why_it_matters=ci.why_it_matters,
                severity=ci.severity,
                affected_part=ci.affected_part,
            )
            for ci in output.critical_issues
        ]
        state.fragile_assumptions = output.fragile_assumptions
        state.contradictions = output.contradictions
        state.failure_modes = output.failure_modes

        return f"{len(output.critical_issues)} vulnerabilidades críticas e {len(output.failure_modes)} modos de falha identificados."
