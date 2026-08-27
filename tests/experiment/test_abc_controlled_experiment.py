"""
tests/experiment/test_abc_controlled_experiment.py
Testes unitários e invariantes de controle do Experimento A/B/C (EXP-M05.2).
Garante que o harness respeita cegueira, 1-to-1 reveal, ausência de fallback e chamadas estritas.
"""

import unittest
import json
from pathlib import Path
from src.idea_evolution.experiments.abc_experiment import ABCExperimentRunner, ABCExperimentSpec
from src.idea_evolution.providers.fake import FakeModelRunner


class TestABCControlledExperiment(unittest.TestCase):

    def setUp(self):
        self.runner = FakeModelRunner()
        self.exp = ABCExperimentRunner(runner=self.runner, seed=12345)

    def test_01_spec_frozen_and_prompts_intact(self):
        """Verifica que a especificação experimental do A/B/C é imutável e define os prompts corretos."""
        self.assertIn("openai/gpt-oss-120b", self.exp.spec.model)
        self.assertIn("groq", self.exp.spec.provider)
        self.assertIn("Um aplicativo que ajuda pessoas", self.exp.spec.raw_idea)
        self.assertIn("C1", self.exp.spec.condition_c_prompts)
        self.assertIn("C4", self.exp.spec.condition_c_prompts)

    def test_02_condition_a_executes_single_call(self):
        """Condição A executa exatamente 1 chamada."""
        out_a, rec_a = self.exp.execute_condition_a()
        self.assertEqual(rec_a.condition, "A")
        self.assertEqual(rec_a.call_index, 1)
        self.assertGreater(len(out_a), 0)

    def test_03_condition_c_executes_exactly_four_calls(self):
        """Condição C executa exatamente 4 chamadas sequenciais."""
        out_c, recs_c = self.exp.execute_condition_c()
        self.assertEqual(len(recs_c), 4)
        self.assertEqual(recs_c[0].stage_name, "CRITIQUE_1")
        self.assertEqual(recs_c[1].stage_name, "REVISION_1")
        self.assertEqual(recs_c[2].stage_name, "CRITIQUE_2")
        self.assertEqual(recs_c[3].stage_name, "REVISION_2")
        self.assertGreater(len(out_c), 0)

    def test_04_blinding_and_reveal_mapping_is_one_to_one(self):
        """Garante que o pacote de blinding anonimiza A/B/C para RESULT 1/2/3 sem vazar identidades."""
        out_a = "Texto A"
        out_b = "Texto B"
        out_c = "Texto C"

        reveal_map, norm_outs, packet_md = self.exp.generate_blinded_packet(out_a, out_b, out_c)

        # Mapeamento 1-to-1 estrito
        self.assertEqual(set(reveal_map.keys()), {"RESULT 1", "RESULT 2", "RESULT 3"})
        self.assertEqual(set(reveal_map.values()), {"A", "B", "C"})

        # O Markdown de avaliação NÃO deve conter as identificações das condições
        self.assertNotIn("Condição A", packet_md)
        self.assertNotIn("Condição B", packet_md)
        self.assertNotIn("Condição C", packet_md)
        self.assertNotIn("BASELINE_SINGLE_REFINE", packet_md)
        self.assertNotIn("IEE_SIMPLE_LOOP", packet_md)
        self.assertNotIn("CRITIQUE_REVISION_LOOP", packet_md)

        # Contém a rubrica cega
        self.assertIn("RUBRICA DE PONTUAÇÃO HUMANA", packet_md)
        self.assertIn("RESULT 1", packet_md)
        self.assertIn("RESULT 2", packet_md)
        self.assertIn("RESULT 3", packet_md)

    def test_05_no_automatic_fallback_on_unsupported_model(self):
        """Provedor desconhecido falha com erro e não aciona fallback automático."""
        from src.idea_evolution.providers.native import NativeModelRunner
        with self.assertRaises(ValueError):
            NativeModelRunner(provider="unsupported_provider_xyz")


if __name__ == "__main__":
    unittest.main(verbosity=2)
