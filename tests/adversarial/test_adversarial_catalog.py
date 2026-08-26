"""
tests/adversarial/test_adversarial_catalog.py
Testes adversariais para injeção de modelos pagos, modelos stale/descontinuados e tentativas de fallback pago.
"""

import unittest
from src.idea_evolution.config.catalog import ModelCatalog, CostPolicy, ExecutionMode
from src.idea_evolution.config.routing import ModelRoutingConfig, ModelDefinition
from src.idea_evolution.providers.router import RunnerRouter


class TestAdversarialCatalog(unittest.TestCase):

    def test_01_adversarial_paid_injection_blocked_at_routing(self):
        """Ataque: Configuração tenta injetar modelo pago (gpt-4o-mini) sob política FREE_ONLY."""
        cfg = ModelRoutingConfig(
            cost_policy=CostPolicy.FREE_ONLY,
            models={"malicious_paid": ModelDefinition(provider="openai", model="gpt-4o-mini")},
            routes={"understand": "malicious_paid"},
            default_model_alias="malicious_paid",
        )
        with self.assertRaises(ValueError) as ctx:
            cfg.resolve_stage("understand")
        self.assertIn("COST_POLICY_VIOLATION", str(ctx.exception))
        self.assertIn("PAID", str(ctx.exception))

    def test_02_adversarial_stale_shutdown_model_blocked(self):
        """Ataque: Configuração tenta utilizar modelo encerrado (llama-3.3-70b-versatile)."""
        cfg = ModelRoutingConfig(
            cost_policy=CostPolicy.FREE_ONLY,
            models={"stale_model": ModelDefinition(provider="groq", model="llama-3.3-70b-versatile")},
            routes={"understand": "stale_model"},
            default_model_alias="stale_model",
        )
        with self.assertRaises(ValueError) as ctx:
            cfg.resolve_stage("understand")
        self.assertIn("MODEL_SHUT_DOWN", str(ctx.exception))
        self.assertIn("openai/gpt-oss-120b", str(ctx.exception))

    def test_03_paid_fallback_attack_fails_loud(self):
        """Ataque: Em modo operacional, falha de cota para um modelo sem alternativas gratuitas NUNCA recorre a modelos pagos."""
        catalog = ModelCatalog()
        # Configura um modelo free de um provedor que não tem outros modelos free catalogados (ex: openrouter se só houver 1)
        cfg = ModelRoutingConfig(
            cost_policy=CostPolicy.FREE_ONLY,
            execution_mode=ExecutionMode.FREE_POOL_OPERATIONAL,
            models={"primary": ModelDefinition(provider="openrouter", model="openrouter/free")},
            routes={"understand": "primary"},
        )
        router = RunnerRouter(config=cfg, catalog=catalog)
        fallback = router.handle_stage_failure("understand", "primary", "FREE_QUOTA_EXHAUSTED")
        # Deve retornar None (BLOCKED_NO_FREE_CAPACITY) e nunca selecionar um modelo pago da OpenAI ou Anthropic
        self.assertIsNone(fallback)

    def test_04_experimental_integrity_pinned_model_fails_closed(self):
        """Ataque: No modo EXPERIMENTAL_PINNED (M05), falha de quota bloqueia o experimento e não troca o modelo."""
        cfg = ModelRoutingConfig(
            cost_policy=CostPolicy.FREE_ONLY,
            execution_mode=ExecutionMode.EXPERIMENTAL_PINNED,
            models={"pinned_model": ModelDefinition(provider="groq", model="openai/gpt-oss-120b")},
            routes={"understand": "pinned_model"},
        )
        router = RunnerRouter(config=cfg)
        fallback = router.handle_stage_failure("understand", "pinned_model", "FREE_QUOTA_EXHAUSTED")
        self.assertIsNone(fallback)


if __name__ == "__main__":
    unittest.main(verbosity=2)
