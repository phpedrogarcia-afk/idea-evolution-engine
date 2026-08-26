"""
src/idea_evolution/stages/reality_check.py
Estágio 4: REALITY_CHECK (v0.1) — Mapeamento de dependências e testes do mundo real com isolamento estrito entre Core e Exploratório.
"""

from typing import Type
import json
from src.idea_evolution.domain.state import SimpleIdeaState
from src.idea_evolution.stages.stage_base import BaseStage
from src.idea_evolution.stages.contracts import RealityCheckOutput


class RealityCheckStage(BaseStage):
    def __init__(self):
        super().__init__(
            stage_id="REALITY_CHECK",
            stage_version="0.1.0",
            prompt_filename="reality_check_v0_1.md",
        )

    def build_prompt_context(self, state: SimpleIdeaState) -> str:
        template = self.load_prompt_template()
        alt_str = json.dumps([a.mechanism for a in state.alternatives])
        return (
            template.replace("{human_intent}", state.human_intent)
            .replace("{current_idea}", state.current_idea)
            .replace("{alternatives}", alt_str)
        )

    def get_output_schema(self) -> Type[RealityCheckOutput]:
        return RealityCheckOutput

    def apply_output_to_state(self, state: SimpleIdeaState, output: RealityCheckOutput) -> str:
        state.reality_dependencies = output.reality_dependencies
        state.claims_needing_evidence = output.claims_needing_evidence
        state.candidate_tests = output.candidate_tests
        state.exploratory_candidate_tests = output.exploratory_candidate_tests
        return f"{len(output.reality_dependencies)} dependências do Core, {len(output.candidate_tests)} testes do Core e {len(output.exploratory_candidate_tests)} testes exploratórios mapeados."
