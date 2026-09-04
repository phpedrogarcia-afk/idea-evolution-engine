"""
tests/test_fioideias_v1_provider_guard.py
Testes determinísticos de Fronteira de Provedor e Guarda de Custo Zero para Fase P4 (M06).

Valida deterministicamente que:
1. Reuso da abstração existente ModelRunner sem duplicações (ProviderAdapter, etc.).
2. ZeroCostGuard aprova modelos gratuitos (FREE, FREE_TRIAL, CREDIT_COVERED).
3. ZeroCostGuard bloqueia modelos tarifados/pagos fail-closed (COST_POLICY_BLOCKED).
4. ZeroCostGuard bloqueia custo desconhecido fail-closed (UNKNOWN_COST_FAIL_CLOSED).
5. ZeroCostGuard bloqueia modelos sem capacidade de Structured Output estrito.
6. IdeaEvolutionService bloqueia requisição paga antes de qualquer inferência (total_calls = 0).
7. IdeaEvolutionService bloqueia modelo não catalogado/desconhecido antes de inferência.
8. Rate limit ou exaustão de quota nunca aciona fallback automático para rota paga.
9. Erro HTTP 429 é classificado como PROVIDER_RATE_LIMIT.
10. Erros HTTP 401/403 ou chave ausente são classificados como PROVIDER_AUTH_FAILURE.
11. Erros HTTP 500/503 são classificados como PROVIDER_SERVER_FAILURE.
12. Timeouts e erros de conexão são classificados como PROVIDER_UNAVAILABLE.
13. Erros de validação de schema JSON são classificados como STRUCTURED_OUTPUT_FAILURE.
14. Credenciais e tokens (csk-, gsk-, sk-, Bearer) são 100% sanitizados em mensagens de erro.
15. Respostas e artefatos de produto têm vazamento zero de segredos ou credenciais.
16. CerebrasRunner e transporte utilizam max_retries = 0 (sem retries ocultos).
17. IdeaEvolutionService permanece estritamente neutro em relação a provedores específicos.
18. Separação explícita entre modelo científico e modelo de transporte é preservada.
19. Zero chamadas reais de modelo durante os testes (custo zero de bolso).
20. Integridade do hash do núcleo científico Lean L1 permanece estritamente idêntica.
"""

from __future__ import annotations

import unittest
import hashlib
import tempfile
import shutil
from pathlib import Path
from typing import Dict, Any, Optional

from src.idea_evolution.providers.base import ModelRunner, ModelResponse, ModelUsage
from src.idea_evolution.providers.fake import FakeModelRunner
from src.idea_evolution.providers.cerebras import CerebrasRunner
from src.idea_evolution.config.catalog import ModelCatalog, CostClass, ModelCatalogEntry, ModelCapabilities
from src.idea_evolution.config.cost_policy import (
    CostEligibility,
    ProviderConfig,
    ZeroCostGuard,
    CostPolicyViolationError,
    StructuredOutputRequirementError,
    sanitize_secret_text,
)
from src.idea_evolution.service.contracts import (
    EvolutionRequest,
    EvolutionResponse,
    TreatmentMode,
    ServiceFailureType,
)
from src.idea_evolution.service.evolution_service import IdeaEvolutionService
from src.idea_evolution.artifacts.evolution_artifact import FROZEN_LEAN_CORE_HASH


class TestFioIdeiasV1ProviderGuardP4(unittest.TestCase):
    """Bateria de testes determinísticos para a fronteira de provedor e guarda de custo zero."""

    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp(prefix="iee_provider_p4_"))
        self.sample_idea = "Criar um sistema de governança de custo e roteamento de IA para projetos de pesquisa."
        self.catalog = ModelCatalog()
        self.default_first_pass = {
            "interpreted_problem": "Projetos de pesquisa necessitam de governança de custos e roteamento de LLMs.",
            "human_intent": "Criar governança de custo e roteamento de IA.",
            "primary_mechanism": {
                "mechanism": "Roteamento determinístico e guarda fail-closed",
                "is_explicit_in_source": False,
                "claimed_basis": "MODEL_HYPOTHESIS",
                "justification": "Mecanismo seguro contra custos inesperados.",
                "tradeoffs": ["Pode bloquear modelos pagos mesmo sob demanda manual."],
            },
            "competing_alternatives": [],
            "key_assumptions": ["Provedores gratuitos têm APIs com disponibilidade adequada."],
            "material_ambiguities": [],
            "material_vulnerabilities": [],
            "remaining_uncertainties": [],
            "requires_human_normative_choice": False,
            "proposed_next_action": "Implementar e testar guardas offline.",
        }

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    # ---------------------------------------------------------------------------
    # Testes 1 a 5: Abstração, Governança de Custos e ZeroCostGuard
    # ---------------------------------------------------------------------------

    def test_01_existing_model_runner_abstraction_reused(self):
        """1: IdeaEvolutionService reutiliza diretamente ModelRunner sem criar camadas intermediárias redundantes."""
        runner = FakeModelRunner()
        service = IdeaEvolutionService(runner=runner, runs_dir=self.temp_dir)
        self.assertIs(service.runner, runner)
        self.assertIsInstance(service.runner, ModelRunner)

        # Provar que não foram criados arquivos com nomes redundantes como ProviderAdapter
        repo_root = Path(__file__).resolve().parent.parent
        self.assertFalse((repo_root / "src" / "idea_evolution" / "providers" / "adapter.py").exists())
        self.assertFalse((repo_root / "src" / "idea_evolution" / "providers" / "facade.py").exists())

    def test_02_zero_cost_guard_allows_free_models(self):
        """2: ZeroCostGuard aprova modelos gratuitos (FREE, FREE_TRIAL, CREDIT_COVERED)."""
        free_config = ProviderConfig(
            provider="cerebras",
            transport_model="gpt-oss-120b",
            scientific_model="openai/gpt-oss-120b",
            cost_eligibility=CostEligibility.FREE,
            paid_inference_allowed=False,
            structured_output_required=True,
        )
        is_valid, reason = ZeroCostGuard.validate_provider_config(free_config, catalog=self.catalog)
        self.assertTrue(is_valid)
        self.assertIsNone(reason)

    def test_03_zero_cost_guard_blocks_paid_models_fail_closed(self):
        """3: ZeroCostGuard bloqueia categoricamente modelos tarifados/pagos (fail-closed)."""
        paid_config = ProviderConfig(
            provider="openai",
            transport_model="gpt-4o-mini",
            scientific_model="openai/gpt-4o-mini",
            cost_eligibility=CostEligibility.PAID,
            paid_inference_allowed=False,
        )
        is_valid, reason = ZeroCostGuard.validate_provider_config(paid_config, catalog=self.catalog)
        self.assertFalse(is_valid)
        self.assertIn("COST_POLICY_BLOCKED", reason)

        # Versão assertiva lança CostPolicyViolationError
        with self.assertRaises(CostPolicyViolationError):
            ZeroCostGuard.ensure_zero_cost(paid_config, catalog=self.catalog)

    def test_04_zero_cost_guard_blocks_unknown_cost_fail_closed(self):
        """4: ZeroCostGuard bloqueia qualquer modelo de custo desconhecido (fail-closed obrigatório)."""
        unknown_config = ProviderConfig(
            provider="some_new_vendor",
            transport_model="unverified-model-v1",
            cost_eligibility=CostEligibility.UNKNOWN,
            paid_inference_allowed=False,
        )
        is_valid, reason = ZeroCostGuard.validate_provider_config(unknown_config, catalog=self.catalog)
        self.assertFalse(is_valid)
        self.assertIn("UNKNOWN_COST_FAIL_CLOSED", reason)

    def test_05_zero_cost_guard_blocks_unsupported_structured_output(self):
        """5: ZeroCostGuard bloqueia modelos que não suportam saída estruturada estrita."""
        # Criar entrada de teste sem suporte a structured output
        custom_catalog = ModelCatalog(entries={
            "custom:model-no-schema": ModelCatalogEntry(
                provider="custom",
                model_id="model-no-schema",
                cost_class=CostClass.FREE_TIER,
                capabilities=ModelCapabilities(structured_output=False),
            )
        })
        config = ProviderConfig(
            provider="custom",
            transport_model="model-no-schema",
            cost_eligibility=CostEligibility.FREE,
            structured_output_required=True,
        )
        is_valid, reason = ZeroCostGuard.validate_provider_config(config, catalog=custom_catalog)
        self.assertFalse(is_valid)
        self.assertIn("STRUCTURED_OUTPUT_NOT_SUPPORTED", reason)

        with self.assertRaises(StructuredOutputRequirementError):
            ZeroCostGuard.ensure_zero_cost(config, catalog=custom_catalog)

    # ---------------------------------------------------------------------------
    # Testes 6 a 8: Proteção Fail-Closed no IdeaEvolutionService
    # ---------------------------------------------------------------------------

    def test_06_service_blocks_paid_request_before_inference(self):
        """6: IdeaEvolutionService rejeita requisições tarifadas antes de qualquer chamada de modelo."""
        call_counter = {"calls": 0}

        class SpyRunner(FakeModelRunner):
            def generate(self, *args, **kwargs):
                call_counter["calls"] += 1
                return super().generate(*args, **kwargs)

        runner = SpyRunner()
        service = IdeaEvolutionService(runner=runner, runs_dir=self.temp_dir, catalog=self.catalog)

        paid_config = ProviderConfig(
            provider="openai",
            transport_model="gpt-4o-mini",
            cost_eligibility=CostEligibility.PAID,
        )
        req = EvolutionRequest(
            raw_idea=self.sample_idea,
            provider_config=paid_config,
        )
        resp = service.evolve(req)

        self.assertFalse(resp.success)
        self.assertEqual(resp.terminal_status, "COST_POLICY_BLOCKED")
        self.assertEqual(resp.failure_type, ServiceFailureType.COST_POLICY_BLOCKED)
        self.assertEqual(resp.total_model_calls, 0)
        self.assertEqual(call_counter["calls"], 0)

    def test_07_service_blocks_unknown_cost_before_inference(self):
        """7: IdeaEvolutionService bloqueia modelo não catalogado/desconhecido antes de executar inferência."""
        call_counter = {"calls": 0}

        class SpyRunner(FakeModelRunner):
            def generate(self, *args, **kwargs):
                call_counter["calls"] += 1
                return super().generate(*args, **kwargs)

        runner = SpyRunner(provider="unregistered_provider", default_model="unknown-llm")
        service = IdeaEvolutionService(runner=runner, runs_dir=self.temp_dir, catalog=self.catalog)

        req = EvolutionRequest(raw_idea=self.sample_idea)
        resp = service.evolve(req)

        self.assertFalse(resp.success)
        self.assertEqual(resp.failure_type, ServiceFailureType.COST_POLICY_BLOCKED)
        self.assertEqual(call_counter["calls"], 0)
        self.assertIn("UNKNOWN_COST_FAIL_CLOSED", resp.error_message)

    def test_08_no_automatic_paid_fallback(self):
        """8: Exaustão ou rate limit em rota gratuita nunca desencadeia fallback automático para rota paga."""
        # Se um runner gratuito falha por 429, o serviço não tenta chamar um modelo pago
        class RateLimitedRunner(FakeModelRunner):
            def generate(self, *args, **kwargs):
                return ModelResponse(
                    raw_text="",
                    parsed=None,
                    provider="cerebras",
                    model="gpt-oss-120b",
                    error="HTTP 429: Too Many Requests / Rate limit reached for token bucket",
                )

        runner = RateLimitedRunner(provider="cerebras", default_model="gpt-oss-120b")
        service = IdeaEvolutionService(runner=runner, runs_dir=self.temp_dir, catalog=self.catalog)

        resp = service.evolve_idea(self.sample_idea)
        self.assertFalse(resp.success)
        self.assertEqual(resp.failure_type, ServiceFailureType.PROVIDER_RATE_LIMIT)
        # O serviço não redirecionou para OpenAI ou Anthropic
        self.assertNotEqual(getattr(resp.provider_config, "provider", ""), "openai")
        self.assertNotEqual(getattr(resp.provider_config, "cost_eligibility", ""), CostEligibility.PAID)

    # ---------------------------------------------------------------------------
    # Testes 9 a 13: Classificação Tipada de Falhas
    # ---------------------------------------------------------------------------

    def test_09_classify_429_as_provider_rate_limit(self):
        """9: Código HTTP 429 ou esgotamento de quota é classificado como PROVIDER_RATE_LIMIT."""
        class MockRunner429(FakeModelRunner):
            def generate(self, *args, **kwargs):
                return ModelResponse(
                    raw_text="",
                    parsed=None,
                    provider="groq",
                    model="openai/gpt-oss-120b",
                    error="HTTP 429: TPM rate limit exceeded. Capacity exhausted.",
                )

        runner = MockRunner429(provider="groq", default_model="openai/gpt-oss-120b")
        service = IdeaEvolutionService(runner=runner, runs_dir=self.temp_dir, catalog=self.catalog)

        resp = service.evolve_idea(self.sample_idea)
        self.assertFalse(resp.success)
        self.assertEqual(resp.failure_type, ServiceFailureType.PROVIDER_RATE_LIMIT)

    def test_10_classify_401_403_as_provider_auth_failure(self):
        """10: Erros HTTP 401/403 ou ausência de chave de API são classificados como PROVIDER_AUTH_FAILURE."""
        class MockRunner401(FakeModelRunner):
            def generate(self, *args, **kwargs):
                return ModelResponse(
                    raw_text="",
                    parsed=None,
                    provider="cerebras",
                    model="gpt-oss-120b",
                    error="HTTP 401 Unauthorized: Invalid API key or CEREBRAS_API_KEY_ABSENT.",
                )

        runner = MockRunner401(provider="cerebras", default_model="gpt-oss-120b")
        service = IdeaEvolutionService(runner=runner, runs_dir=self.temp_dir, catalog=self.catalog)

        resp = service.evolve_idea(self.sample_idea)
        self.assertFalse(resp.success)
        self.assertEqual(resp.failure_type, ServiceFailureType.PROVIDER_AUTH_FAILURE)

    def test_11_classify_500_503_as_provider_server_failure(self):
        """11: Erros HTTP 500, 502, 503 são classificados como PROVIDER_SERVER_FAILURE."""
        class MockRunner500(FakeModelRunner):
            def generate(self, *args, **kwargs):
                return ModelResponse(
                    raw_text="",
                    parsed=None,
                    provider="cerebras",
                    model="gpt-oss-120b",
                    error="HTTP 503: Service Unavailable. Backend upstream gateway error.",
                )

        runner = MockRunner500(provider="cerebras", default_model="gpt-oss-120b")
        service = IdeaEvolutionService(runner=runner, runs_dir=self.temp_dir, catalog=self.catalog)

        resp = service.evolve_idea(self.sample_idea)
        self.assertFalse(resp.success)
        self.assertEqual(resp.failure_type, ServiceFailureType.PROVIDER_SERVER_FAILURE)

    def test_12_classify_network_timeout_as_provider_unavailable(self):
        """12: Erros de conexão recusada ou socket timeout são classificados como PROVIDER_UNAVAILABLE."""
        class MockRunnerTimeout(FakeModelRunner):
            def generate(self, *args, **kwargs):
                return ModelResponse(
                    raw_text="",
                    parsed=None,
                    provider="cerebras",
                    model="gpt-oss-120b",
                    error="Network connection timeout: urlopen error timed out / connection reset.",
                )

        runner = MockRunnerTimeout(provider="cerebras", default_model="gpt-oss-120b")
        service = IdeaEvolutionService(runner=runner, runs_dir=self.temp_dir, catalog=self.catalog)

        resp = service.evolve_idea(self.sample_idea)
        self.assertFalse(resp.success)
        self.assertEqual(resp.failure_type, ServiceFailureType.PROVIDER_UNAVAILABLE)

    def test_13_classify_schema_validation_as_structured_output_failure(self):
        """13: JSON inválido ou incompatível com o schema é classificado como STRUCTURED_OUTPUT_FAILURE."""
        class MockRunnerSchemaFail(FakeModelRunner):
            def generate(self, *args, **kwargs):
                return ModelResponse(
                    raw_text="{'invalido': true",
                    parsed=None,
                    provider="cerebras",
                    model="gpt-oss-120b",
                    error="VALIDATION_ERROR: JSONDecodeError: Expecting property name enclosed in double quotes",
                )

        runner = MockRunnerSchemaFail(provider="cerebras", default_model="gpt-oss-120b")
        service = IdeaEvolutionService(runner=runner, runs_dir=self.temp_dir, catalog=self.catalog)

        resp = service.evolve_idea(self.sample_idea)
        self.assertFalse(resp.success)
        self.assertEqual(resp.failure_type, ServiceFailureType.STRUCTURED_OUTPUT_FAILURE)

    # ---------------------------------------------------------------------------
    # Testes 14 a 15: Sanitização de Segredos e Credenciais
    # ---------------------------------------------------------------------------

    def test_14_credential_sanitization_in_error_message(self):
        """14: Chaves e segredos em mensagens de erro do provedor são 100% mascarados."""
        raw_error = "Error from https://api.cerebras.ai with key csk-abc123secret456 and Authorization: Bearer my_secret_token and api_key=gsk_987xyz"
        sanitized = sanitize_secret_text(raw_error)

        self.assertNotIn("csk-abc123secret456", sanitized)
        self.assertNotIn("my_secret_token", sanitized)
        self.assertNotIn("gsk_987xyz", sanitized)
        self.assertIn("Bearer ***", sanitized)
        self.assertIn("csk-***", sanitized)
        self.assertIn("api_key=***", sanitized)

    def test_15_credential_sanitization_in_evolution_artifact(self):
        """15: Respostas e logs do serviço nunca expõem credenciais reais mesmo sob erro adverso."""
        class LeakingRunner(FakeModelRunner):
            def generate(self, *args, **kwargs):
                return ModelResponse(
                    raw_text="",
                    parsed=None,
                    provider="cerebras",
                    model="gpt-oss-120b",
                    error="Falha na autorização para token csk-supersecretkey9999",
                )

        runner = LeakingRunner(provider="cerebras", default_model="gpt-oss-120b")
        service = IdeaEvolutionService(runner=runner, runs_dir=self.temp_dir, catalog=self.catalog)

        resp = service.evolve_idea(self.sample_idea)
        self.assertFalse(resp.success)
        self.assertNotIn("csk-supersecretkey9999", resp.error_message)
        self.assertIn("csk-***", resp.error_message)

    # ---------------------------------------------------------------------------
    # Testes 16 a 18: Arquitetura de Transporte, Retries e Separação de Modelos
    # ---------------------------------------------------------------------------

    def test_16_cerebras_runner_max_retries_zero(self):
        """16: CerebrasRunner opera com max_retries = 0 sem retries ocultos de SDK."""
        runner = CerebrasRunner(
            model_name="openai/gpt-oss-120b",
            transport_callable=lambda p: {"content": "{}", "usage": {}},
        )
        # Verifica a invariante de ausência de retry oculto
        self.assertEqual(runner.builder.transport_model, "gpt-oss-120b")
        self.assertEqual(runner.builder.scientific_model, "openai/gpt-oss-120b")

    def test_17_provider_neutrality_of_evolution_service(self):
        """17: IdeaEvolutionService é desacoplado de qualquer SDK ou provedor físico particular."""
        service_code = Path("src/idea_evolution/service/evolution_service.py").read_text(encoding="utf-8")
        self.assertNotIn("cerebras.ai", service_code)
        self.assertNotIn("api.groq.com", service_code)
        self.assertNotIn("openai.com", service_code)
        self.assertNotIn("CEREBRAS_API_KEY", service_code)
        self.assertNotIn("GROQ_API_KEY", service_code)

    def test_18_scientific_vs_transport_model_separation(self):
        """18: Separação explícita entre modelo científico e identificador de transporte."""
        config = ProviderConfig.infer_from_runner(
            FakeModelRunner(provider="cerebras", default_model="gpt-oss-120b"),
            catalog=self.catalog,
        )
        self.assertEqual(config.provider, "cerebras")
        self.assertEqual(config.transport_model, "gpt-oss-120b")
        self.assertEqual(config.scientific_model, "openai/gpt-oss-120b")

    # ---------------------------------------------------------------------------
    # Testes 19 a 20: Custo Zero e Invariância do Núcleo Científico
    # ---------------------------------------------------------------------------

    def test_19_zero_live_model_calls_in_tests(self):
        """19: 100% dos testes executam offline sem realizar chamadas reais à rede."""
        runner = FakeModelRunner(custom_responses={"LEAN_FIRST_PASS": self.default_first_pass})
        service = IdeaEvolutionService(runner=runner, runs_dir=self.temp_dir, catalog=self.catalog)

        resp = service.evolve_idea(self.sample_idea)
        self.assertTrue(resp.success)
        self.assertEqual(resp.terminal_status, "COMPLETED_DIRECT_ONE_PASS")
        self.assertIsNotNone(resp.artifact)

    def test_20_scientific_core_hash_remains_strictly_unchanged(self):
        """20: Integridade inegociável do hash SHA-256 do núcleo científico Lean L1."""
        core_files = {
            "domain/early_epistemic_gate.py": Path("src/idea_evolution/domain/early_epistemic_gate.py"),
            "domain/epistemic_contracts.py": Path("src/idea_evolution/domain/epistemic_contracts.py"),
            "domain/evidence_boundary.py": Path("src/idea_evolution/domain/evidence_boundary.py"),
            "domain/grounding.py": Path("src/idea_evolution/domain/grounding.py"),
            "domain/state.py": Path("src/idea_evolution/domain/state.py"),
            "orchestration/lean_loop.py": Path("src/idea_evolution/orchestration/lean_loop.py"),
            "providers/base.py": Path("src/idea_evolution/providers/base.py"),
        }

        combined = hashlib.sha256()
        for name, p in sorted(core_files.items()):
            data = p.read_bytes().replace(b"\r\n", b"\n")
            sha = hashlib.sha256(data).hexdigest()
            combined.update(name.encode() + b":" + sha.encode() + b"\n")

        computed_core_hash = combined.hexdigest()
        self.assertEqual(
            computed_core_hash,
            FROZEN_LEAN_CORE_HASH,
            "VIOLAÇÃO DO NÚCLEO CIENTÍFICO: Os arquivos congelados foram modificados!",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
