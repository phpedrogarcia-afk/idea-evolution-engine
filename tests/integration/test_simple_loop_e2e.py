"""
tests/integration/test_simple_loop_e2e.py
Teste de integração de ponta a ponta do Simple Idea Evolution Loop (Condição B) com FakeModelRunner.
"""

import unittest
import shutil
from pathlib import Path
from src.idea_evolution.orchestration.simple_loop import SimpleLoopRunner
from src.idea_evolution.providers.fake import FakeModelRunner
from src.idea_evolution.domain.state import RunStatus

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TEST_RUNS_DIR = REPO_ROOT / "runs_test_e2e"


class TestSimpleLoopE2E(unittest.TestCase):

    def setUp(self):
        if TEST_RUNS_DIR.exists():
            shutil.rmtree(TEST_RUNS_DIR)
        TEST_RUNS_DIR.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        if TEST_RUNS_DIR.exists():
            shutil.rmtree(TEST_RUNS_DIR)

    def test_01_complete_standard_loop_execution(self):
        runner = FakeModelRunner()
        loop = SimpleLoopRunner(runner=runner, topology="STANDARD_6_STAGE", runs_dir=TEST_RUNS_DIR)

        idea_text = "Um sistema para criar cartões flash com IA a partir de PDFs de medicina."
        state = loop.run(idea_text, run_id="RUN-E2E-TEST-001")

        # Verificações de Estado
        self.assertEqual(state.status, RunStatus.REFINED_IDEA_READY)
        self.assertEqual(state.original_idea, idea_text)
        self.assertTrue(len(state.current_idea) > 20)
        self.assertTrue(len(state.human_intent) > 10)
        self.assertTrue(len(state.critical_issues) >= 1)
        self.assertTrue(len(state.alternatives) >= 1)
        self.assertTrue(len(state.accepted_changes) >= 1)
        self.assertEqual(state.reconstruction_count, 0)
        self.assertEqual(len(state.stage_history), 6)  # 6 estágios executados

        # Verificações de Artefatos Físicos
        run_folder = TEST_RUNS_DIR / "RUN-E2E-TEST-001"
        self.assertTrue((run_folder / "input.json").exists())
        self.assertTrue((run_folder / "state.json").exists())
        self.assertTrue((run_folder / "final.json").exists())
        self.assertTrue((run_folder / "final.md").exists())
        self.assertTrue((run_folder / "trace.json").exists())
        self.assertTrue((run_folder / "stages" / "01_UNDERSTAND.json").exists())
        self.assertTrue((run_folder / "stages" / "06_FINAL_REVIEW.json").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
