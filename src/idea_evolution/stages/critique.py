"""
src/idea_evolution/stages/critique.py
Estágios de Crítica Especializada para a Condição C (Iterative Critique-Revision).
"""

from typing import Type
import json
from src.idea_evolution.domain.state import SimpleIdeaState, CriticalIssue
from src.idea_evolution.stages.stage_base import BaseStage
from src.idea_evolution.stages.contracts import CritiqueOutput


class LogicalCritiqueStage(BaseStage):
    def __init__(self):
        super().__init__(
            stage_id="CRITIQUE_1",
            stage_version="0.1.0",
            prompt_filename="critique_logical_v0_1.md",
        )

    def build_prompt_context(self, state: SimpleIdeaState) -> str:
        template = self.load_prompt_template()
        return template + f"\n\nContexto da Ideia:\n{state.current_idea}\nPremissas: {json.dumps(state.assumptions)}"

    def get_output_schema(self) -> Type[CritiqueOutput]:
        return CritiqueOutput

    def apply_output_to_state(self, state: SimpleIdeaState, output: CritiqueOutput) -> str:
        new_issues = [
            CriticalIssue(
                issue=ci.issue,
                why_it_matters=ci.why_it_matters,
                severity=ci.severity,
                affected_part=ci.affected_part,
            )
            for ci in output.critical_issues
        ]
        state.critical_issues.extend(new_issues)
        state.fragile_assumptions.extend(output.fragile_assumptions)
        state.contradictions.extend(output.contradictions)
        return f"Crítica Lógica: {len(output.critical_issues)} falhas estruturais apontadas."


class FeasibilityCritiqueStage(BaseStage):
    def __init__(self):
        super().__init__(
            stage_id="CRITIQUE_2",
            stage_version="0.1.0",
            prompt_filename="critique_feasibility_v0_1.md",
        )

    def build_prompt_context(self, state: SimpleIdeaState) -> str:
        template = self.load_prompt_template()
        return template + f"\n\nVersão Revisada:\n{state.current_idea}\nIntenção: {state.human_intent}"

    def get_output_schema(self) -> Type[CritiqueOutput]:
        return CritiqueOutput

    def apply_output_to_state(self, state: SimpleIdeaState, output: CritiqueOutput) -> str:
        new_issues = [
            CriticalIssue(
                issue=ci.issue,
                why_it_matters=ci.why_it_matters,
                severity=ci.severity,
                affected_part=ci.affected_part,
            )
            for ci in output.critical_issues
        ]
        state.critical_issues.extend(new_issues)
        state.failure_modes.extend(output.failure_modes)
        return f"Crítica de Viabilidade: {len(output.critical_issues)} riscos práticos apontados."
