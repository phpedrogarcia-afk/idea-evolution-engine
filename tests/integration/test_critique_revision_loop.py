"""
tests/integration/test_critique_revision_loop.py
Testes de integração para a Condição C: Iterative Critique-Revision (MultiAgent Research Ideator inspiration).
"""

import unittest
import shutil
from pathlib import Path
from src.idea_evolution.orchestration.simple_loop import SimpleLoopRunner
from src.idea_evolution.providers.fake import FakeModelRunner
from src.idea_evolution.domain.state import RunStatus

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TEST_RUNS_DIR = REPO_ROOT / "runs_test_critique_rev"


class TestCritiqueRevisionLoop(unittest.TestCase):

    def setUp(self):
        if TEST_RUNS_DIR.exists():
            shutil.rmtree(TEST_RUNS_DIR)
        TEST_RUNS_DIR.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        if TEST_RUNS_DIR.exists():
            shutil.rmtree(TEST_RUNS_DIR)

    def test_01_critique_revision_execution_order(self):
        runner = FakeModelRunner()
        loop = SimpleLoopRunner(runner=runner, topology="ITERATIVE_CRITIQUE_REVISION", runs_dir=TEST_RUNS_DIR)

        idea_text = "Uma plataforma de micro-crédito comunitário baseada em confiança."
        state = loop.run(idea_text, run_id="RUN-CRITIQUE-REV-001")

        self.assertEqual(state.status, RunStatus.REFINED_IDEA_READY)
        # Ordem de estágios esperada:
        # 1. UNDERSTAND
        # 2. CRITIQUE_1
        # 3. REVISION_1
        # 4. CRITIQUE_2
        # 5. REVISION_2
        # 6. ALTERNATIVES
        # 7. SYNTHESIZE
        # 8. REALITY_CHECK
        # 9. FINAL_REVIEW
        # Total = 9 estágios
        self.assertEqual(len(state.stage_history), 9)

        executed_stages = [entry.stage_id for entry in state.stage_history]
        expected_stages = [
            "UNDERSTAND",
            "CRITIQUE_1",
            "REVISION_1",
            "CRITIQUE_2",
            "REVISION_2",
            "ALTERNATIVES",
            "SYNTHESIZE",
            "REALITY_CHECK",
            "FINAL_REVIEW",
        ]
        self.assertEqual(executed_stages, expected_stages)


if __name__ == "__main__":
    unittest.main(verbosity=2)
