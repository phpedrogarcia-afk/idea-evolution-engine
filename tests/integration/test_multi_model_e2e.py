"""
tests/integration/test_multi_model_e2e.py
Teste de Integração E2E Offline com Roteamento Multi-Modelo e Múltiplos Fake Providers.
"""

import unittest
import tempfile
import json
from pathlib import Path
from src.idea_evolution.config.routing import ModelRoutingConfig, ModelDefinition
from src.idea_evolution.orchestration.simple_loop import SimpleLoopRunner
from src.idea_evolution.providers.router import RunnerRouter
from src.idea_evolution.providers.fake import FakeModelRunner
from src.idea_evolution.domain.state import RunStatus


class TestMultiModelIntegrationE2E(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.runs_path = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_01_multi_model_offline_e2e_state_transportation(self):
        """
        Executa um loop completo onde 3 fake providers/modelos distintos participam.
        Verifica o transporte de estado entre eles e a gravação estrita de proveniência.
        """
        config = ModelRoutingConfig(
            models={
                "analyst": ModelDefinition(provider="fake_a", model="llama-3.3-70b"),
                "critic": ModelDefinition(provider="fake_b", model="claude-3-5-haiku"),
                "synthesizer": ModelDefinition(provider="fake_c", model="gpt-4o-mini"),
            },
            routes={
                "understand": "analyst",
                "attack": "critic",
                "alternatives": "analyst",
                "reality_check": "critic",
                "synthesize": "synthesizer",
                "final_review": "critic",
            },
            default_model_alias="analyst",
        )

        runner = SimpleLoopRunner(
            config=config,
            topology="STANDARD_6_STAGE",
            runs_dir=self.runs_path,
        )

        state = runner.run("Uma plataforma P2P para compartilhamento de ferramentas elétricas.")

        self.assertEqual(state.status, RunStatus.REFINED_IDEA_READY)
        self.assertEqual(len(state.stage_history), 6)

        # 1. UNDERSTAND -> analyst / fake_a / llama-3.3-70b
        stg1 = state.stage_history[0]
        self.assertEqual(stg1.stage_id, "UNDERSTAND")
        self.assertEqual(stg1.logical_alias, "analyst")
        self.assertEqual(stg1.provider, "fake_a")
        self.assertEqual(stg1.model, "llama-3.3-70b")

        # 2. ATTACK -> critic / fake_b / claude-3-5-haiku
        stg2 = state.stage_history[1]
        self.assertEqual(stg2.stage_id, "ATTACK")
        self.assertEqual(stg2.logical_alias, "critic")
        self.assertEqual(stg2.provider, "fake_b")
        self.assertEqual(stg2.model, "claude-3-5-haiku")

        # 3. ALTERNATIVES -> analyst / fake_a / llama-3.3-70b
        stg3 = state.stage_history[2]
        self.assertEqual(stg3.stage_id, "ALTERNATIVES")
        self.assertEqual(stg3.logical_alias, "analyst")
        self.assertEqual(stg3.provider, "fake_a")

        # 4. REALITY_CHECK -> critic / fake_b / claude-3-5-haiku
        stg4 = state.stage_history[3]
        self.assertEqual(stg4.stage_id, "REALITY_CHECK")
        self.assertEqual(stg4.logical_alias, "critic")
        self.assertEqual(stg4.provider, "fake_b")

        # 5. SYNTHESIZE -> synthesizer / fake_c / gpt-4o-mini
        stg5 = state.stage_history[4]
        self.assertEqual(stg5.stage_id, "SYNTHESIZE")
        self.assertEqual(stg5.logical_alias, "synthesizer")
        self.assertEqual(stg5.provider, "fake_c")
        self.assertEqual(stg5.model, "gpt-4o-mini")

        # 6. FINAL_REVIEW -> critic / fake_b / claude-3-5-haiku
        stg6 = state.stage_history[5]
        self.assertEqual(stg6.stage_id, "FINAL_REVIEW")
        self.assertEqual(stg6.logical_alias, "critic")
        self.assertEqual(stg6.provider, "fake_b")

        # Verificar persistência em disco
        run_folder = self.runs_path / state.run_id
        self.assertTrue(run_folder.exists())

        trace_data = json.loads((run_folder / "trace.json").read_text(encoding="utf-8"))
        self.assertEqual(len(trace_data["stages"]), 6)
        self.assertEqual(trace_data["stages"][0]["logical_alias"], "analyst")
        self.assertEqual(trace_data["stages"][1]["logical_alias"], "critic")
        self.assertEqual(trace_data["stages"][4]["logical_alias"], "synthesizer")

        input_data = json.loads((run_folder / "input.json").read_text(encoding="utf-8"))
        self.assertEqual(input_data["metadata"]["routing_config_hash"], config.compute_hash())

    def test_02_critique_revision_multi_model_e2e(self):
        """Topologia Iterative Critique-Revision executa 9 estágios multi-modelo com proveniência completa."""
        config = ModelRoutingConfig(
            models={
                "author": ModelDefinition(provider="fake_a", model="model-author"),
                "logical_reviewer": ModelDefinition(provider="fake_b", model="model-logic"),
                "practical_reviewer": ModelDefinition(provider="fake_c", model="model-practical"),
            },
            routes={
                "understand": "author",
                "critique_1": "logical_reviewer",
                "revision_1": "author",
                "critique_2": "practical_reviewer",
                "revision_2": "author",
                "alternatives": "author",
                "reality_check": "practical_reviewer",
                "synthesize": "author",
                "final_review": "logical_reviewer",
            },
            default_model_alias="author",
        )

        runner = SimpleLoopRunner(
            config=config,
            topology="ITERATIVE_CRITIQUE_REVISION",
            runs_dir=self.runs_path,
        )

        state = runner.run("Sistema de assinatura de café personalizado.")
        self.assertEqual(state.status, RunStatus.REFINED_IDEA_READY)
        self.assertEqual(len(state.stage_history), 9)

        aliases = [h.logical_alias for h in state.stage_history]
        expected = [
            "author",
            "logical_reviewer",
            "author",
            "practical_reviewer",
            "author",
            "author",
            "practical_reviewer",
            "author",
            "logical_reviewer",
        ]
        self.assertEqual(aliases, expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
