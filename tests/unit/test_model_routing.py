"""
tests/unit/test_model_routing.py
Testes unitários para ModelRoutingConfig, RunnerRouter e validação determinística de rotas.
"""

import unittest
from pathlib import Path
from src.idea_evolution.config.routing import ModelRoutingConfig, ModelDefinition
from src.idea_evolution.providers.router import RunnerRouter
from src.idea_evolution.providers.fake import FakeModelRunner


class TestModelRouting(unittest.TestCase):

    def test_01_config_hash_determinism(self):
        """O hash da configuração de rotas é determinístico e independente da ordem das chaves."""
        cfg1 = ModelRoutingConfig(
            models={
                "b_critic": ModelDefinition(provider="fake_b", model="mock-b"),
                "a_analyst": ModelDefinition(provider="fake_a", model="mock-a"),
            },
            routes={"attack": "b_critic", "understand": "a_analyst"},
        )
        cfg2 = ModelRoutingConfig(
            models={
                "a_analyst": ModelDefinition(provider="fake_a", model="mock-a"),
                "b_critic": ModelDefinition(provider="fake_b", model="mock-b"),
            },
            routes={"understand": "a_analyst", "attack": "b_critic"},
        )
        self.assertEqual(cfg1.compute_hash(), cfg2.compute_hash())
        self.assertTrue(len(cfg1.compute_hash()) == 64)

    def test_02_unknown_model_alias_fails_loud(self):
        """Se uma rota aponta para um alias não definido em models, deve falhar ruidosamente."""
        cfg = ModelRoutingConfig(
            models={"analyst": ModelDefinition(provider="fake", model="m1")},
            routes={"understand": "non_existent_alias"},
        )
        with self.assertRaises(KeyError) as ctx:
            cfg.resolve_stage("understand")
        self.assertIn("UNKNOWN_MODEL_ALIAS", str(ctx.exception))

    def test_03_missing_route_fails_loud(self):
        """Se um estágio não tem rota e não há default_model_alias, deve falhar com erro explícito."""
        cfg = ModelRoutingConfig(
            models={"analyst": ModelDefinition(provider="fake", model="m1")},
            routes={"understand": "analyst"},
            default_model_alias=None,
        )
        with self.assertRaises(KeyError) as ctx:
            cfg.resolve_stage("attack")
        self.assertIn("ROUTE_CONFIGURATION_INVALID", str(ctx.exception))

    def test_04_default_single_model_fallback(self):
        """Configuração de modelo único padrão resolve qualquer estágio para o default."""
        cfg = ModelRoutingConfig.default_single_model(provider="fake", model="default-m")
        alias, model_def = cfg.resolve_stage("synthesize")
        self.assertEqual(alias, "default")
        self.assertEqual(model_def.provider, "fake")
        self.assertEqual(model_def.model, "default-m")

    def test_05_runner_router_instantiation_and_isolation(self):
        """RunnerRouter instancia os executores corretos sem misturar instâncias."""
        cfg = ModelRoutingConfig(
            models={
                "analyst": ModelDefinition(provider="fake_a", model="model-a"),
                "critic": ModelDefinition(provider="fake_b", model="model-b"),
            },
            routes={"understand": "analyst", "attack": "critic"},
        )
        router = RunnerRouter(config=cfg)
        r1, m1, a1 = router.get_runner_for_stage("UNDERSTAND")
        r2, m2, a2 = router.get_runner_for_stage("ATTACK")

        self.assertEqual(a1, "analyst")
        self.assertEqual(m1, "model-a")
        self.assertEqual(r1.provider, "fake_a")

        self.assertEqual(a2, "critic")
        self.assertEqual(m2, "model-b")
        self.assertEqual(r2.provider, "fake_b")
        self.assertNotEqual(r1, r2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
