"""
tests/experiment/test_comparison_packet.py
Testes do protocolo experimental EXP-M04-001 e geração do pacote de comparação cega (Condition A vs B vs C).
"""

import unittest
import shutil
import json
from pathlib import Path
from src.idea_evolution.orchestration.baseline import BaselineRunner
from src.idea_evolution.orchestration.simple_loop import SimpleLoopRunner
from src.idea_evolution.providers.fake import FakeModelRunner

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
FIXTURES_DIR = REPO_ROOT / "fixtures"
TEST_RUNS_DIR = REPO_ROOT / "runs_test_experiment"
EXP_DIR = REPO_ROOT / "experiments" / "MISSION-04"


class TestComparisonPacket(unittest.TestCase):

    def setUp(self):
        if TEST_RUNS_DIR.exists():
            shutil.rmtree(TEST_RUNS_DIR)
        TEST_RUNS_DIR.mkdir(parents=True, exist_ok=True)
        EXP_DIR.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        if TEST_RUNS_DIR.exists():
            shutil.rmtree(TEST_RUNS_DIR)

    def test_01_execute_and_generate_comparison_packet(self):
        runner = FakeModelRunner()
        fixtures = sorted(list(FIXTURES_DIR.glob("*.json")))
        self.assertTrue(len(fixtures) >= 3, "Devem existir ao menos 3 fixtures padronizadas.")

        packet_lines = []
        packet_lines.append("# EXPERIMENTO EXP-M04-001 — PACOTE DE AVALIAÇÃO CEGA")
        packet_lines.append("\n> **Protocolo:** Comparação cega entre Baseline (A), Simple Loop Padrão (B) e Critique-Revision Iterativo (C).\n")

        for f_path in fixtures:
            f_data = json.loads(f_path.read_text(encoding="utf-8"))
            idea_text = f_data["original_idea"]
            f_id = f_data["fixture_id"]
            f_name = f_data["name"]

            # Condição A: Baseline
            b_runner = BaselineRunner(runner)
            res_a = b_runner.run(idea_text, run_id=f"EXP-{f_id}-COND-A", runs_dir=TEST_RUNS_DIR)

            # Condição B: Simple Loop
            loop_b = SimpleLoopRunner(runner, topology="STANDARD_6_STAGE", runs_dir=TEST_RUNS_DIR)
            res_b = loop_b.run(idea_text, run_id=f"EXP-{f_id}-COND-B")

            # Condição C: Critique-Revision
            loop_c = SimpleLoopRunner(runner, topology="ITERATIVE_CRITIQUE_REVISION", runs_dir=TEST_RUNS_DIR)
            res_c = loop_c.run(idea_text, run_id=f"EXP-{f_id}-COND-C")

            packet_lines.append(f"## Fixture: {f_id} — {f_name}")
            packet_lines.append(f"**Ideia Bruta:**\n> {idea_text}\n")

            packet_lines.append("### Output Mascarado 1")
            packet_lines.append(f"{res_a['parsed_output'].get('refined_version', '')}\n")

            packet_lines.append("### Output Mascarado 2")
            packet_lines.append(f"{res_b.current_idea}\n")

            packet_lines.append("### Output Mascarado 3")
            packet_lines.append(f"{res_c.current_idea}\n")

            packet_lines.append("**Rubrica de Avaliação Humana:**")
            packet_lines.append("1. Qual versão preservou com maior fidelidade a intenção original sem desvio de essência?")
            packet_lines.append("2. Qual versão identificou as vulnerabilidades e riscos mais severos e reais?")
            packet_lines.append("3. Qual versão propôs o próximo passo mais acionável e testável?")
            packet_lines.append("4. Houve ganho justificável no Output 3 sobre o Output 2 considerando a profundidade da crítica?\n")
            packet_lines.append("---\n")

        packet_file = EXP_DIR / "comparison-packet.md"
        packet_file.write_text("\n".join(packet_lines), encoding="utf-8")

        self.assertTrue(packet_file.exists())
        content = packet_file.read_text(encoding="utf-8")
        self.assertIn("FIX-001", content)
        self.assertIn("FIX-002", content)
        self.assertIn("FIX-003", content)


if __name__ == "__main__":
    unittest.main(verbosity=2)
