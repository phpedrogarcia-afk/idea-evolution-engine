"""
tests/unit/test_stage_contracts.py
Testes unitários de conformidade de schemas Pydantic e templates de prompts.
"""

import unittest
from pathlib import Path
from src.idea_evolution.stages.contracts import (
    UnderstandOutput,
    AttackOutput,
    CritiqueOutput,
    RevisionOutput,
    AlternativesOutput,
    RealityCheckOutput,
    SynthesizeOutput,
    FinalReviewOutput,
    BaselineRefineOutput,
)
from src.idea_evolution.stages.understand import UnderstandStage
from src.idea_evolution.stages.attack import AttackStage
from src.idea_evolution.stages.alternatives import AlternativesStage
from src.idea_evolution.stages.reality_check import RealityCheckStage
from src.idea_evolution.stages.synthesize import SynthesizeStage
from src.idea_evolution.stages.final_review import FinalReviewStage


class TestStageContracts(unittest.TestCase):

    def test_01_all_prompt_files_exist(self):
        stages = [
            UnderstandStage(),
            AttackStage(),
            AlternativesStage(),
            RealityCheckStage(),
            SynthesizeStage(),
            FinalReviewStage(),
        ]
        for st in stages:
            template = st.load_prompt_template()
            self.assertTrue(len(template) > 50, f"Template do estágio {st.stage_id} está vazio ou truncado.")
            self.assertIn("Output Schema", template)

    def test_02_schema_validation_strictness(self):
        # Validação do UnderstandOutput
        valid_u = UnderstandOutput(
            interpreted_problem="Prob",
            human_intent="Intent",
            proposed_mechanism="Mech",
            structured_idea="Struct",
        )
        self.assertEqual(valid_u.human_intent, "Intent")

        # Validação do FinalReviewOutput
        valid_fr = FinalReviewOutput(
            material_issues_remaining=[],
            essence_drift_detected=False,
            drift_explanation="",
            unresolved_critical_issue=False,
            recommendation="REFINED_IDEA_READY",
            review_summary="Tudo certo",
        )
        self.assertEqual(valid_fr.recommendation, "REFINED_IDEA_READY")


if __name__ == "__main__":
    unittest.main(verbosity=2)
