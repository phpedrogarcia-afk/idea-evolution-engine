"""
tests/unit/test_model_catalog.py
Testes unitários para ModelCatalog, CostPolicy, PrivacyClass e Governança de Ciclo de Vida.
"""

import unittest
from src.idea_evolution.config.catalog import (
    ModelCatalog,
    CostPolicy,
    ExecutionMode,
    CostClass,
    LifecycleStatus,
    PrivacyClass,
)
from src.idea_evolution.config.routing import ModelRoutingConfig, ModelDefinition
from src.idea_evolution.providers.router import RunnerRouter


class TestModelCatalog(unittest.TestCase):

    def setUp(self):
        self.catalog = ModelCatalog()

    def test_01_deprecated_and_shutdown_model_rejected(self):
        """Modelos com status SHUT_DOWN são rejeitados com sugestão de substituto."""
        is_ok, reason = self.catalog.validate_eligibility("groq", "llama-3.3-70b-versatile")
        self.assertFalse(is_ok)
        self.assertIn("MODEL_SHUT_DOWN", reason)
        self.assertIn("openai/gpt-oss-120b", reason)

        is_ok_gem, reason_gem = self.catalog.validate_eligibility("gemini", "gemini-2.0-flash")
        self.assertFalse(is_ok_gem)
        self.assertIn("MODEL_SHUT_DOWN", reason_gem)
        self.assertIn("gemini-3.7-flash", reason_gem)

    def test_02_free_only_rejects_paid_candidate(self):
        """Sob política FREE_ONLY, modelos pagos como gpt-4o-mini são estritamente rejeitados."""
        is_ok, reason = self.catalog.validate_eligibility(
            "openai", "gpt-4o-mini", cost_policy=CostPolicy.FREE_ONLY
        )
        self.assertFalse(is_ok)
        self.assertIn("COST_POLICY_VIOLATION", reason)

    def test_03_free_only_accepts_free_tier_and_local(self):
        """Sob política FREE_ONLY, modelos FREE_TIER e locais são aprovados."""
        is_ok1, _ = self.catalog.validate_eligibility("groq", "openai/gpt-oss-120b", cost_policy=CostPolicy.FREE_ONLY)
        is_ok2, _ = self.catalog.validate_eligibility("groq", "qwen/qwen3.6-27b", cost_policy=CostPolicy.FREE_ONLY)
        is_ok3, _ = self.catalog.validate_eligibility("gemini", "gemini-3.7-flash", cost_policy=CostPolicy.FREE_ONLY)
        is_ok4, _ = self.catalog.validate_eligibility("fake", "default-model", cost_policy=CostPolicy.FREE_ONLY)

        self.assertTrue(is_ok1)
        self.assertTrue(is_ok2)
        self.assertTrue(is_ok3)
        self.assertTrue(is_ok4)

    def test_04_promotional_credit_conditional(self):
        """Modelos com PROMOTIONAL_CREDIT são rejeitados em FREE_ONLY mas permitidos em ALLOW_PROMOTIONAL."""
        is_ok_free, _ = self.catalog.validate_eligibility(
            "anthropic", "claude-3-5-haiku-20241022", cost_policy=CostPolicy.FREE_ONLY
        )
        self.assertFalse(is_ok_free)

        is_ok_promo, _ = self.catalog.validate_eligibility(
            "anthropic", "claude-3-5-haiku-20241022", cost_policy=CostPolicy.ALLOW_PROMOTIONAL
        )
        self.assertTrue(is_ok_promo)

    def test_05_privacy_ineligible_provider_exclusion(self):
        """Quando exclude_product_improvement_use=True, provedores que usam dados no free tier são excluídos."""
        is_ok, reason = self.catalog.validate_eligibility(
            "gemini", "gemini-3.7-flash", exclude_product_improvement_use=True
        )
        self.assertFalse(is_ok)
        self.assertIn("PRIVACY_POLICY_VIOLATION", reason)

    def test_06_operational_mode_permits_next_free_on_quota_exhaustion(self):
        """Em modo operacional FREE_POOL_OPERATIONAL, esgotamento de quota seleciona o próximo free elegível."""
        cfg = ModelRoutingConfig(
            cost_policy=CostPolicy.FREE_ONLY,
            execution_mode=ExecutionMode.FREE_POOL_OPERATIONAL,
            models={"primary": ModelDefinition(provider="groq", model="openai/gpt-oss-120b")},
            routes={"understand": "primary"},
        )
        router = RunnerRouter(config=cfg, catalog=self.catalog)
        fallback = router.handle_stage_failure("understand", "primary", "FREE_QUOTA_EXHAUSTED")
        self.assertIsNotNone(fallback)
        runner, model_id, alias = fallback
        self.assertEqual(model_id, "qwen/qwen3.6-27b")

    def test_07_schema_and_semantic_failures_do_not_trigger_fallback(self):
        """Falhas de schema ou semântica NUNCA trocam de provedor, mesmo em modo operacional."""
        cfg = ModelRoutingConfig(
            cost_policy=CostPolicy.FREE_ONLY,
            execution_mode=ExecutionMode.FREE_POOL_OPERATIONAL,
            models={"primary": ModelDefinition(provider="groq", model="openai/gpt-oss-120b")},
            routes={"understand": "primary"},
        )
        router = RunnerRouter(config=cfg, catalog=self.catalog)
        fallback_schema = router.handle_stage_failure("understand", "primary", "SCHEMA_INVALID")
        fallback_sem = router.handle_stage_failure("understand", "primary", "SEMANTIC_FAILURE")
        self.assertIsNone(fallback_schema)
        self.assertIsNone(fallback_sem)

    def test_08_experimental_mode_never_auto_fallbacks(self):
        """No modo EXPERIMENTAL_PINNED (M05), NENHUMA falha aciona troca de modelo."""
        cfg = ModelRoutingConfig(
            cost_policy=CostPolicy.FREE_ONLY,
            execution_mode=ExecutionMode.EXPERIMENTAL_PINNED,
            models={"primary": ModelDefinition(provider="groq", model="openai/gpt-oss-120b")},
            routes={"understand": "primary"},
        )
        router = RunnerRouter(config=cfg, catalog=self.catalog)
        fallback = router.handle_stage_failure("understand", "primary", "FREE_QUOTA_EXHAUSTED")
        self.assertIsNone(fallback)


if __name__ == "__main__":
    unittest.main(verbosity=2)
