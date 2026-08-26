"""
tests/integration/test_reconstruction_path.py
Testes de integração para o caminho de reconstrução limitada (max 1 ciclo) e prevenção de loop infinito.
"""

import unittest
import shutil
from pathlib import Path
from src.idea_evolution.orchestration.simple_loop import SimpleLoopRunner
from src.idea_evolution.providers.fake import FakeModelRunner
from src.idea_evolution.domain.state import RunStatus

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TEST_RUNS_DIR = REPO_ROOT / "runs_test_reconstruction"


class TestReconstructionPath(unittest.TestCase):

    def setUp(self):
        if TEST_RUNS_DIR.exists():
            shutil.rmtree(TEST_RUNS_DIR)
        TEST_RUNS_DIR.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        if TEST_RUNS_DIR.exists():
            shutil.rmtree(TEST_RUNS_DIR)

    def test_01_single_reconstruction_cycle_success(self):
        # Configurar FakeRunner para rejeitar no primeiro review e aprovar no segundo
        runner = FakeModelRunner(trigger_reconstruction=True)
        loop = SimpleLoopRunner(runner=runner, topology="STANDARD_6_STAGE", runs_dir=TEST_RUNS_DIR)

        state = loop.run("Ideia com problemas iniciais.", run_id="RUN-RECON-001")

        self.assertEqual(state.reconstruction_count, 1)
        self.assertEqual(state.status, RunStatus.REFINED_IDEA_READY)
        # 6 estágios originais + 4 estágios de reconstrução (alternatives, reality_check, synthesize, final_review) = 10 chamadas
        self.assertEqual(len(state.stage_history), 10)

    def test_02_infinite_loop_prevention_on_persistent_rejection(self):
        # Configurar FakeRunner para rejeitar perpetuamente
        class AlwaysRejectRunner(FakeModelRunner):
            def generate(self, prompt_text, output_schema, stage_name, model_name=None, max_repairs=1):
                resp = super().generate(prompt_text, output_schema, stage_name, model_name, max_repairs)
                if stage_name == "FINAL_REVIEW":
                    resp.parsed.recommendation = "RECONSTRUCT"
                    resp.parsed.unresolved_critical_issue = True
                return resp

        runner = AlwaysRejectRunner()
        loop = SimpleLoopRunner(runner=runner, topology="STANDARD_6_STAGE", runs_dir=TEST_RUNS_DIR)

        state = loop.run("Ideia que nunca passa no review.", run_id="RUN-INFINITE-PREVENT-001")

        # Deve parar após exatamente 1 ciclo de reconstrução com status REFINEMENT_INCOMPLETE
        self.assertEqual(state.reconstruction_count, 1)
        self.assertEqual(state.status, RunStatus.REFINEMENT_INCOMPLETE)
        self.assertEqual(len(state.stage_history), 10)


if __name__ == "__main__":
    unittest.main(verbosity=2)
