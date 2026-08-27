"""
tests/unit/test_fioed_replay.py
Testes unitários e determinísticos do harness de replay offline FioED (M05.3).
"""

import unittest
from pathlib import Path

from src.idea_evolution.experiments.fioed_replay import FioEDReplayHarness


class TestFioEDReplay(unittest.TestCase):

    def setUp(self):
        self.repo_root = Path(__file__).resolve().parent.parent.parent
        self.harness = FioEDReplayHarness(self.repo_root)

    def test_inventory_and_hashes_deterministic(self):
        """Replay Inventory — Localiza os artefatos brutos reais e calcula hashes determinísticos."""
        inv = self.harness.inventory_raw_artifacts()
        self.assertGreater(len(inv), 0)
        # Verifica se todos os hashes SHA256 são válidos de 64 caracteres hex
        for rec in inv:
            self.assertEqual(len(rec.sha256_hash), 64)
            self.assertTrue(Path(self.repo_root / rec.artifact_path).exists())

    def test_replay_determinism_same_input_same_output(self):
        """Replay Determinism — Executar o replay duas vezes produz exatamente os mesmos resultados."""
        run1 = self.harness.execute_all_replays()
        run2 = self.harness.execute_all_replays()

        self.assertEqual(run1["findings_summary"], run2["findings_summary"])
        self.assertEqual(run1["conditions"]["condition_b"]["evidence_free_persistence_steps"], run2["conditions"]["condition_b"]["evidence_free_persistence_steps"])

    def test_condition_b_waste_identified_by_fioed_signals(self):
        """Condition B Replay — FioED identifica empiricamente o desperdício epistêmico da Condição B."""
        results = self.harness.execute_all_replays()
        cond_a = results["conditions"]["condition_a"]
        cond_b = results["conditions"]["condition_b"]
        cond_c = results["conditions"]["condition_c"]

        # Condição B tem significativamente mais passos de persistência sem evidência (9 passos vs 0 em A e 2 em C)
        self.assertGreater(cond_b["evidence_free_persistence_steps"], cond_a["evidence_free_persistence_steps"])
        self.assertGreater(cond_b["evidence_free_persistence_steps"], cond_c["evidence_free_persistence_steps"])

        # Condição B acumulou mais regressões decisórias
        self.assertGreater(len(cond_b["decision_regression_events"]), len(cond_a["decision_regression_events"]))

        # Flag de AttachmentRisk e SourceRefresh disparados em B
        self.assertTrue(cond_b["attachment_risk_signal"])
        self.assertTrue(cond_b["source_refresh_required"])

    def test_no_ideaworth_score_generated(self):
        """IdeaWorth Policy — O harness não produz nenhum score escalar de valor da ideia."""
        results = self.harness.execute_all_replays()
        for cond_key, cond_data in results["conditions"].items():
            self.assertNotIn("idea_worth_score", cond_data)
            self.assertNotIn("universal_value_score", cond_data)


if __name__ == "__main__":
    unittest.main(verbosity=2)
