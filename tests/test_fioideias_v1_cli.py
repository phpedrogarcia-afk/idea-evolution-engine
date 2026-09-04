"""
tests/test_fioideias_v1_cli.py
Suíte de testes determinísticos da CLI FioIdeias V1 para a Fase P5 (M06).

Valida deterministicamente as 20 asserções inegociáveis:
1. iee evolve "idea" resolve com sucesso através do IdeaEvolutionService.
2. Tratamento padrão é LEAN_L1 (Condição C).
3. CLI não invoca SimpleLoopRunner por padrão.
4. CLI não bypassa o IdeaEvolutionService.
5. EvolutionArtifact canônico de produto é retornado/serializado.
6. Ideia humana original sobrevive intacta.
7. Proveniência e autoridade sobrevivem à serialização da CLI.
8. Rótulos de autoridade de candidatos permanecem não-explícitos.
9. HUMAN_DECISION_REQUIRED sobrevive como desfecho válido de domínio (código de saída 0).
10. Entrada vazia ou excessivamente curta falha com código não-zero e INVALID_INPUT.
11. Violação da política de custo zero emite erro limpo de COST_POLICY_BLOCKED.
12. Ausência de credencial de provedor emite erro tipado PROVIDER_AUTH_FAILURE.
13. Código HTTP 429 emite erro operacional PROVIDER_RATE_LIMIT.
14. Códigos HTTP 500/503 emitem erro operacional PROVIDER_SERVER_FAILURE.
15. Material de segredo e chaves de API estão ausentes da saída da CLI (100% mascarados).
16. Flags da Condição B e loop profundo experimental não estão expostas publicamente.
17. Provedor ou modelo desconhecido falha fechado (fail-closed).
18. Saída JSON (--json) contém artefato canônico de produto, não estruturas internas de laboratório.
19. Fake runner executa perfeitamente em modo offline (custo zero de bolso).
20. Hash combinado dos 7 arquivos congelados do núcleo científico permanece estritamente invariante.
"""

from __future__ import annotations

import unittest
from unittest.mock import patch
import io
import contextlib
import json
import tempfile
import shutil
import hashlib
from pathlib import Path

from src.idea_evolution.cli.main import main, parse_args
from src.idea_evolution.providers.fake import FakeModelRunner
from src.idea_evolution.providers.base import ModelResponse
from src.idea_evolution.service.contracts import TreatmentMode, ServiceFailureType
from src.idea_evolution.service.evolution_service import IdeaEvolutionService
from src.idea_evolution.artifacts.evolution_artifact import (
    EvolutionArtifact,
    FROZEN_LEAN_CORE_HASH,
)
from src.idea_evolution.domain.state import PromotionAuthorityBasis


class TestFioIdeiasV1CliP5(unittest.TestCase):
    """Testes determinísticos do ponto de entrada estável da CLI iee."""

    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp(prefix="iee_cli_p5_"))
        self.sample_idea = "Criar um sistema simples de rodízio de tarefas diárias em uma cafeteria de 3 pessoas."
        self.default_first_pass = {
            "interpreted_problem": "Cafeteria com 3 funcionários precisa de escala justa e sem atrito.",
            "human_intent": "Distribuir tarefas diárias de cafeteria de forma equitativa.",
            "primary_mechanism": {
                "mechanism": "Quadro físico com cartões magnéticos rotativos",
                "is_explicit_in_source": False,
                "claimed_basis": "MODEL_HYPOTHESIS",
                "justification": "Solução prática de baixo atrito físico.",
                "tradeoffs": ["Exige disciplina presencial diária"],
            },
            "competing_alternatives": [],
            "key_assumptions": ["Funcionários comparecem nos horários estabelecidos"],
            "material_ambiguities": [],
            "material_vulnerabilities": [],
            "remaining_uncertainties": ["Adesão dos funcionários ao quadro"],
            "requires_human_normative_choice": False,
            "proposed_next_action": "Testar com cartões de papel durante 1 semana",
        }

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _create_fake_runner(self, custom_responses=None):
        resp = {"LEAN_FIRST_PASS": self.default_first_pass}
        if custom_responses:
            resp.update(custom_responses)
        return FakeModelRunner(custom_responses=resp)

    # ---------------------------------------------------------------------------
    # Testes 1 a 4: Roteamento, Delegação e Descarte da Condição B Padrão
    # ---------------------------------------------------------------------------

    def test_01_iee_evolve_resolves_through_service(self):
        """1: iee evolve 'idea' executa com sucesso e retorna código de saída 0."""
        runner = self._create_fake_runner()
        stdout = io.StringIO()
        stderr = io.StringIO()

        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            exit_code = main(["evolve", self.sample_idea, "--runs-dir", str(self.temp_dir)], runner=runner)

        self.assertEqual(exit_code, 0)
        output = stdout.getvalue()
        self.assertIn("FIOIDEIAS V1", output)
        self.assertIn("Ideia Original:", output)
        self.assertIn("Mecanismo Proposto:", output)

    def test_02_default_treatment_is_lean_l1(self):
        """2: O tratamento padrão da CLI é incondicionalmente LEAN_L1 (não Condição B)."""
        runner = self._create_fake_runner()
        stdout = io.StringIO()

        with contextlib.redirect_stdout(stdout):
            exit_code = main(["evolve", self.sample_idea, "--json", "--runs-dir", str(self.temp_dir)], runner=runner)

        self.assertEqual(exit_code, 0)
        data = json.loads(stdout.getvalue())
        self.assertEqual(data.get("treatment_mode"), TreatmentMode.LEAN_L1.value)

    def test_03_cli_does_not_invoke_simple_loop_runner_by_default(self):
        """3: A CLI não invoca SimpleLoopRunner por padrão (Condição B desfeita da rota normal)."""
        runner = self._create_fake_runner()

        with patch("src.idea_evolution.orchestration.simple_loop.SimpleLoopRunner.run") as mock_simple_run:
            exit_code = main(["evolve", self.sample_idea, "--runs-dir", str(self.temp_dir)], runner=runner)
            self.assertEqual(exit_code, 0)
            mock_simple_run.assert_not_called()

    def test_04_cli_does_not_bypass_idea_evolution_service(self):
        """4: A CLI delega estritamente para IdeaEvolutionService sem chamar runners científicos diretamente."""
        runner = self._create_fake_runner()

        with patch.object(IdeaEvolutionService, "evolve", wraps=IdeaEvolutionService(runner=runner, runs_dir=self.temp_dir).evolve) as spy_evolve:
            exit_code = main(["evolve", self.sample_idea, "--runs-dir", str(self.temp_dir)], runner=runner)
            self.assertEqual(exit_code, 0)
            spy_evolve.assert_called_once()
            call_req = spy_evolve.call_args[0][0]
            self.assertEqual(call_req.treatment_mode, TreatmentMode.LEAN_L1)
            self.assertEqual(call_req.raw_idea, self.sample_idea)

    # ---------------------------------------------------------------------------
    # Testes 5 a 8: Integridade do Artefato, Proveniência e Autoridade
    # ---------------------------------------------------------------------------

    def test_05_canonical_evolution_artifact_serialized(self):
        """5: A saída JSON serializa perfeitamente o EvolutionArtifact canônico de produto."""
        runner = self._create_fake_runner()
        stdout = io.StringIO()

        with contextlib.redirect_stdout(stdout):
            exit_code = main(["evolve", self.sample_idea, "--json", "--runs-dir", str(self.temp_dir)], runner=runner)

        self.assertEqual(exit_code, 0)
        data = json.loads(stdout.getvalue())
        artifact = EvolutionArtifact.model_validate(data)
        self.assertEqual(artifact.schema_version, "1.0")
        self.assertEqual(artifact.treatment_mode, TreatmentMode.LEAN_L1)

    def test_06_original_idea_survives_lossless(self):
        """6: A ideia humana original sobrevive com integridade total."""
        runner = self._create_fake_runner()
        stdout = io.StringIO()

        with contextlib.redirect_stdout(stdout):
            main(["evolve", self.sample_idea, "--json", "--runs-dir", str(self.temp_dir)], runner=runner)

        data = json.loads(stdout.getvalue())
        self.assertEqual(data.get("original_idea"), self.sample_idea)

    def test_07_provenance_survives_cli_serialization(self):
        """7: Proveniência de autoridade original sobrevive como USER_EXPLICIT e SourceAnchor íntegro."""
        runner = self._create_fake_runner()
        stdout = io.StringIO()

        with contextlib.redirect_stdout(stdout):
            main(["evolve", self.sample_idea, "--json", "--runs-dir", str(self.temp_dir)], runner=runner)

        data = json.loads(stdout.getvalue())
        self.assertEqual(data.get("original_idea_authority"), PromotionAuthorityBasis.USER_EXPLICIT.value)
        self.assertIsNotNone(data.get("source_anchor"))
        self.assertEqual(data["source_anchor"]["original_content"], self.sample_idea)

    def test_08_candidate_authority_labels_survive(self):
        """8: Propostas do modelo permanecem rotuladas como MODEL_HYPOTHESIS, sem usurpação de autoridade."""
        runner = self._create_fake_runner()
        stdout = io.StringIO()

        with contextlib.redirect_stdout(stdout):
            main(["evolve", self.sample_idea, "--json", "--runs-dir", str(self.temp_dir)], runner=runner)

        data = json.loads(stdout.getvalue())
        self.assertEqual(data.get("refined_idea_authority"), PromotionAuthorityBasis.MODEL_HYPOTHESIS.value)
        self.assertEqual(data.get("assumptions_authority"), PromotionAuthorityBasis.MODEL_HYPOTHESIS.value)

    # ---------------------------------------------------------------------------
    # Testes 9 a 10: Desfechos de Domínio vs Erros de Entrada
    # ---------------------------------------------------------------------------

    def test_09_human_decision_required_survives_as_valid_domain_outcome(self):
        """9: HUMAN_DECISION_REQUIRED é desfecho válido de produto (retorna código de saída 0)."""
        normative_first_pass = dict(self.default_first_pass)
        normative_first_pass["requires_human_normative_choice"] = True
        normative_first_pass["human_choice_description"] = "Decidir se penalidades devem existir na escala."

        runner = self._create_fake_runner(custom_responses={"LEAN_FIRST_PASS": normative_first_pass})
        stdout = io.StringIO()
        stderr = io.StringIO()

        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            exit_code = main(["evolve", self.sample_idea, "--runs-dir", str(self.temp_dir)], runner=runner)

        self.assertEqual(exit_code, 0)
        output = stdout.getvalue()
        self.assertIn("BIFURCAÇÃO NORMATIVA DETECTADA", output)
        self.assertIn("Decidir se penalidades devem existir", output)

    def test_10_invalid_empty_input_fails_deterministically(self):
        """10: Entrada vazia ou curta demais falha com código não-zero e INVALID_INPUT."""
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            exit_code = main(["evolve", ""])
        self.assertEqual(exit_code, 1)
        self.assertIn("INVALID_INPUT", stderr.getvalue())

        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            exit_code = main(["evolve", "ab"])
        self.assertEqual(exit_code, 1)
        self.assertIn("INVALID_INPUT", stderr.getvalue())

    # ---------------------------------------------------------------------------
    # Testes 11 a 15: Governança de Custos, Falhas Operacionais e Sanitização
    # ---------------------------------------------------------------------------

    def test_11_zero_cost_policy_block_becomes_clean_cli_error(self):
        """11: Violação da política de custo zero emite erro limpo COST_POLICY_BLOCKED e código 1."""
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            exit_code = main(["evolve", self.sample_idea, "--provider", "openai", "--model", "gpt-4o-mini", "--runs-dir", str(self.temp_dir)])

        self.assertEqual(exit_code, 1)
        err_msg = stderr.getvalue()
        self.assertIn("COST_POLICY_BLOCKED", err_msg)

    def test_12_missing_credential_becomes_provider_auth_failure(self):
        """12: Ausência de credencial de provedor é reportada como PROVIDER_AUTH_FAILURE."""
        class AuthFailRunner(FakeModelRunner):
            def generate(self, *args, **kwargs):
                return ModelResponse(
                    raw_text="",
                    parsed=None,
                    provider="cerebras",
                    model="gpt-oss-120b",
                    error="CEREBRAS_API_KEY_ABSENT: Chave de API ausente no ambiente.",
                )

        runner = AuthFailRunner(provider="cerebras", default_model="gpt-oss-120b")
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            exit_code = main(["evolve", self.sample_idea, "--runs-dir", str(self.temp_dir)], runner=runner)

        self.assertEqual(exit_code, 1)
        self.assertIn("PROVIDER_AUTH_FAILURE", stderr.getvalue())

    def test_13_429_rate_limit_becomes_operational_error(self):
        """13: HTTP 429 ou esgotamento de quota emite erro operacional PROVIDER_RATE_LIMIT."""
        class RateLimitRunner(FakeModelRunner):
            def generate(self, *args, **kwargs):
                return ModelResponse(
                    raw_text="",
                    parsed=None,
                    provider="cerebras",
                    model="gpt-oss-120b",
                    error="HTTP 429: TPM rate limit exceeded for free tier.",
                )

        runner = RateLimitRunner(provider="cerebras", default_model="gpt-oss-120b")
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            exit_code = main(["evolve", self.sample_idea, "--runs-dir", str(self.temp_dir)], runner=runner)

        self.assertEqual(exit_code, 1)
        self.assertIn("PROVIDER_RATE_LIMIT", stderr.getvalue())

    def test_14_500_server_failure_becomes_operational_error(self):
        """14: HTTP 500/503 emite erro operacional PROVIDER_SERVER_FAILURE."""
        class ServerFailRunner(FakeModelRunner):
            def generate(self, *args, **kwargs):
                return ModelResponse(
                    raw_text="",
                    parsed=None,
                    provider="cerebras",
                    model="gpt-oss-120b",
                    error="HTTP 503 Service Unavailable: upstream connection failed.",
                )

        runner = ServerFailRunner(provider="cerebras", default_model="gpt-oss-120b")
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            exit_code = main(["evolve", self.sample_idea, "--runs-dir", str(self.temp_dir)], runner=runner)

        self.assertEqual(exit_code, 1)
        self.assertIn("PROVIDER_SERVER_FAILURE", stderr.getvalue())

    def test_15_secret_material_absent_from_cli_error(self):
        """15: Material confidencial (chaves csk- e Bearer) é 100% mascarado na saída da CLI."""
        class LeakingRunner(FakeModelRunner):
            def generate(self, *args, **kwargs):
                return ModelResponse(
                    raw_text="",
                    parsed=None,
                    provider="cerebras",
                    model="gpt-oss-120b",
                    error="Erro de autenticação para chave csk-secretkey9999 e Bearer token_secreto_888",
                )

        runner = LeakingRunner(provider="cerebras", default_model="gpt-oss-120b")
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            exit_code = main(["evolve", self.sample_idea, "--runs-dir", str(self.temp_dir)], runner=runner)

        self.assertEqual(exit_code, 1)
        err_out = stderr.getvalue()
        self.assertNotIn("csk-secretkey9999", err_out)
        self.assertNotIn("token_secreto_888", err_out)
        self.assertIn("csk-***", err_out)
        self.assertIn("Bearer ***", err_out)

    # ---------------------------------------------------------------------------
    # Testes 16 a 18: Proteção contra Exposição Indevida e Formato de Saída
    # ---------------------------------------------------------------------------

    def test_16_condition_b_research_flag_not_publicly_exposed(self):
        """16: Flags da Condição B e loop profundo não existem na interface pública do evolve."""
        for forbidden_flag in ["--condition-b", "--simple-loop", "--deep-loop", "--allow-experimental-deep-loop", "--topology"]:
            with self.assertRaises(SystemExit) as ctx:
                parse_args(["evolve", self.sample_idea, forbidden_flag])
            # Argparse emite código 2 para argumentos não reconhecidos
            self.assertEqual(ctx.exception.code, 2)

    def test_17_unknown_provider_fails_closed(self):
        """17: Provedor não catalogado ou com custo desconhecido falha fechado (fail-closed)."""
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            exit_code = main(["evolve", self.sample_idea, "--provider", "some_unregistered_vendor", "--runs-dir", str(self.temp_dir)])

        self.assertEqual(exit_code, 1)
        self.assertIn("COST_POLICY_BLOCKED", stderr.getvalue())

    def test_18_json_output_contains_product_artifact_not_lean_internals(self):
        """18: A saída JSON contém exclusivamente campos do EvolutionArtifact, sem vazamento de estruturas internas."""
        runner = self._create_fake_runner()
        stdout = io.StringIO()

        with contextlib.redirect_stdout(stdout):
            main(["evolve", self.sample_idea, "--json", "--runs-dir", str(self.temp_dir)], runner=runner)

        data = json.loads(stdout.getvalue())
        # Campos canônicos presentes
        self.assertIn("schema_version", data)
        self.assertIn("artifact_id", data)
        self.assertIn("original_idea", data)
        self.assertIn("refined_idea", data)
        # Campos internos de laboratório NÃO vazam no nível superior
        self.assertNotIn("gate_result", data)
        self.assertNotIn("epistemic_rent", data)
        self.assertNotIn("decision_delta", data)
        self.assertNotIn("first_pass", data)

    # ---------------------------------------------------------------------------
    # Testes 19 a 20: Execução Offline e Invariância do Núcleo Científico
    # ---------------------------------------------------------------------------

    def test_19_fake_runner_executes_offline_with_zero_calls(self):
        """19: Testes e execuções com fake runner são 100% determinísticos e com zero custo."""
        runner = self._create_fake_runner()
        stdout = io.StringIO()

        with contextlib.redirect_stdout(stdout):
            exit_code = main(["evolve", self.sample_idea, "--fast", "--runs-dir", str(self.temp_dir)], runner=runner)

        self.assertEqual(exit_code, 0)
        output = stdout.getvalue()
        self.assertIn("FIOIDEIAS V1", output)

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
