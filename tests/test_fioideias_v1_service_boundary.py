"""
tests/test_fioideias_v1_service_boundary.py
Testes determinísticos para o FioIdeias V1 Service Boundary (M06 P1).

Zero chamadas de rede.
Zero consumo de tokens.
Valida isolamento da camada de aplicação e fidelidade do núcleo científico Lean L1.
"""

import unittest
import shutil
import tempfile
import hashlib
from pathlib import Path

from src.idea_evolution.service.contracts import (
    EvolutionRequest,
    EvolutionResponse,
    TreatmentMode,
    ServiceFailureType,
)
from src.idea_evolution.service.evolution_service import IdeaEvolutionService
from src.idea_evolution.providers.fake import FakeModelRunner
from src.idea_evolution.domain.early_epistemic_gate import GateOutcome, EscalationReason


class TestFioIdeiasV1ServiceBoundary(unittest.TestCase):

    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp(prefix="test_fioideias_v1_"))
        self.runs_dir = self.test_dir / "runs"
        self.runs_dir.mkdir(parents=True, exist_ok=True)

        self.sample_idea = "Criar um sistema simples de rodízio de tarefas diárias em uma cafeteria de 3 pessoas."

        self.default_first_pass = {
            "interpreted_problem": "Cafeteria com 3 funcionários precisa de escala justa e sem atrito.",
            "human_intent": "Distribuir tarefas diárias de cafeteria de forma equitativa e sem software pesado.",
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
            "remaining_uncertainties": [],
            "requires_human_normative_choice": False,
            "proposed_next_action": "Testar com cartões de papel durante 1 semana",
        }

    def tearDown(self):
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def test_01_service_accepts_valid_raw_idea_and_delegates_to_lean_l1_by_default(self):
        """1 & 2: Service aceita ideia válida e delega para Lean L1 por padrão."""
        runner = FakeModelRunner(custom_responses={"LEAN_FIRST_PASS": self.default_first_pass})
        service = IdeaEvolutionService(runner=runner, runs_dir=self.runs_dir)

        response = service.evolve_idea(self.sample_idea)

        self.assertTrue(response.success)
        self.assertEqual(response.treatment_used, TreatmentMode.LEAN_L1)
        self.assertEqual(response.total_model_calls, 1)
        self.assertEqual(response.terminal_status, "COMPLETED_DIRECT_ONE_PASS")
        self.assertFalse(response.human_decision_requested)
        self.assertTrue(response.decision_progress_detected)
        self.assertIsNone(response.failure_type)

    def test_02_service_does_not_invoke_condition_b_by_default(self):
        """3: Service não invoca Condição B por padrão e bloqueia uso acidental."""
        runner = FakeModelRunner(custom_responses={"LEAN_FIRST_PASS": self.default_first_pass})
        service = IdeaEvolutionService(runner=runner, runs_dir=self.runs_dir)

        # Default nunca é Condição B
        self.assertEqual(service.default_treatment, TreatmentMode.LEAN_L1)

        # Tentativa de chamar Condição B sem flag explícita é bloqueada
        req = EvolutionRequest(
            raw_idea=self.sample_idea,
            treatment_mode=TreatmentMode.SUSPENDED_DEEP_LOOP,
            allow_experimental_deep_loop=False,
        )
        resp = service.evolve(req)

        self.assertFalse(resp.success)
        self.assertEqual(resp.treatment_used, TreatmentMode.SUSPENDED_DEEP_LOOP)
        self.assertEqual(resp.terminal_status, "SUSPENDED_TREATMENT_BLOCKED")
        self.assertEqual(resp.failure_type, ServiceFailureType.INVALID_INPUT)
        self.assertIn("suspensa", resp.error_message.lower())

    def test_03_lean_result_preserved_through_boundary(self):
        """4: Resultado detalhado do Lean L1 é preservado integralmente na resposta."""
        runner = FakeModelRunner(custom_responses={"LEAN_FIRST_PASS": self.default_first_pass})
        service = IdeaEvolutionService(runner=runner, runs_dir=self.runs_dir)

        resp = service.evolve_idea(self.sample_idea)

        self.assertIsNotNone(resp.lean_result)
        self.assertEqual(resp.lean_result.source_anchor.original_content, self.sample_idea)
        self.assertEqual(
            resp.lean_result.first_pass.primary_mechanism.mechanism,
            "Quadro físico com cartões magnéticos rotativos",
        )
        self.assertEqual(resp.lean_result.gate_result.outcome, GateOutcome.RETURN_NOW)

    def test_04_human_intent_and_original_idea_not_silently_changed(self):
        """5: Intenção humana e ideia original não são alteradas ou corrompidas na fronteira."""
        runner = FakeModelRunner(custom_responses={"LEAN_FIRST_PASS": self.default_first_pass})
        service = IdeaEvolutionService(runner=runner, runs_dir=self.runs_dir)

        resp = service.evolve_idea(self.sample_idea)

        self.assertEqual(resp.raw_idea, self.sample_idea)
        self.assertEqual(resp.lean_result.source_anchor.original_content, self.sample_idea)
        self.assertEqual(
            resp.lean_result.first_pass.human_intent,
            "Distribuir tarefas diárias de cafeteria de forma equitativa e sem software pesado.",
        )

    def test_05_focused_escalation_result_survives_boundary(self):
        """6: Escalação focada dispara sob incerteza material e sobrevive à fronteira de serviço."""
        escalated_first_pass = dict(self.default_first_pass)
        escalated_first_pass["material_vulnerabilities"] = [
            {
                "vulnerability": "Equipe pode rejeitar rodízio se as tarefas tiverem cargas horárias desiguais.",
                "why_it_matters": "Gera conflitos internos graves.",
                "severity": "HIGH",
                "affected_aspect": "Adesão",
            }
        ]

        escalation_response = {
            "escalation_reason": "MATERIAL_VULNERABILITY",
            "target_hypothesis": "Equipe pode rejeitar rodízio se tarefas forem desiguais.",
            "focused_critique_or_analysis": "Pesagem prévia de tarefas em pontos resolve a assimetria percebida.",
            "resolved_tradeoffs": ["Adiciona complexidade de pontuação em troca de percepção de justiça."],
            "discriminating_tests": ["Listar as 5 tarefas mais pesadas e atribuir pesos acordados."],
            "hypothesis_mutated": True,
            "mutated_hypothesis_description": "Quadro com pesos ponderados de tarefas.",
            "decision_progress_made": True,
            "updated_next_action": "Realizar votação de pesos das tarefas com a equipe.",
        }

        runner = FakeModelRunner(
            custom_responses={
                "LEAN_FIRST_PASS": escalated_first_pass,
                "FOCUSED_ESCALATION": escalation_response,
            }
        )
        service = IdeaEvolutionService(runner=runner, runs_dir=self.runs_dir)

        resp = service.evolve_idea(self.sample_idea)

        self.assertTrue(resp.success)
        self.assertEqual(resp.total_model_calls, 2)
        self.assertEqual(resp.terminal_status, "COMPLETED_WITH_FOCUSED_ESCALATION")
        self.assertIsNotNone(resp.lean_result.escalation_result)
        self.assertEqual(
            resp.lean_result.escalation_result.escalation_reason,
            EscalationReason.MATERIAL_VULNERABILITY,
        )
        self.assertTrue(resp.lean_result.decision_progress_detected)

    def test_06_human_decision_required_survives_correctly_as_domain_outcome(self):
        """7: HUMAN_DECISION_REQUIRED sobrevive como desfecho de domínio válido (não é erro)."""
        normative_first_pass = dict(self.default_first_pass)
        normative_first_pass["requires_human_normative_choice"] = True
        normative_first_pass["human_choice_description"] = "Decidir se penalidades por falta de cumprimento de tarefa devem existir."

        runner = FakeModelRunner(custom_responses={"LEAN_FIRST_PASS": normative_first_pass})
        service = IdeaEvolutionService(runner=runner, runs_dir=self.runs_dir)

        resp = service.evolve_idea(self.sample_idea)

        self.assertTrue(resp.success)
        self.assertTrue(resp.human_decision_requested)
        self.assertEqual(resp.terminal_status, "HUMAN_DECISION_REQUIRED")
        self.assertEqual(resp.total_model_calls, 1)
        self.assertIsNone(resp.failure_type)

    def test_07_provider_or_structured_failure_distinguishable(self):
        """8: Falhas de modelo/provider são distinguidas com clareza de desfechos de domínio."""
        class FailingModelRunner(FakeModelRunner):
            def generate(self, prompt_text, output_schema, stage_name, model_name=None, max_repairs=1):
                return FakeModelRunner.generate(
                    self, prompt_text, output_schema, stage_name, model_name, max_repairs=0
                )

        runner = FailingModelRunner(should_fail_schema_stages={"LEAN_FIRST_PASS": 1})
        service = IdeaEvolutionService(runner=runner, runs_dir=self.runs_dir)

        resp = service.evolve_idea(self.sample_idea)

        self.assertFalse(resp.success)
        self.assertEqual(resp.terminal_status, "FIRST_PASS_FAILED")
        self.assertEqual(resp.failure_type, ServiceFailureType.STRUCTURED_OUTPUT_FAILURE)
        self.assertIn("Falha na análise inicial", resp.error_message)


    def test_08_invalid_input_fails_deterministically(self):
        """9: Entradas inválidas (vazias, espaços, muito curtas) falham sem chamadas de modelo."""
        runner = FakeModelRunner(custom_responses={"LEAN_FIRST_PASS": self.default_first_pass})
        service = IdeaEvolutionService(runner=runner, runs_dir=self.runs_dir)

        for bad_input in ["", "   ", "ab", None]:
            req = EvolutionRequest(raw_idea=bad_input or "")
            resp = service.evolve(req)

            self.assertFalse(resp.success)
            self.assertEqual(resp.total_model_calls, 0)
            self.assertEqual(resp.failure_type, ServiceFailureType.INVALID_INPUT)
            self.assertEqual(resp.terminal_status, "INVALID_INPUT")

    def test_09_fast_fallback_condition_a_available_explicitly(self):
        """10: Condição A (Baseline) pode ser selecionada explicitamente como FAST_FALLBACK."""
        baseline_response = {
            "summary": "Ideia de rodízio para cafeteria.",
            "refined_version": "Criar quadro magnético semanal.",
            "tradeoffs": ["Manutenção manual"],
            "next_step": "Testar 1 semana",
        }
        runner = FakeModelRunner(custom_responses={"BASELINE_REFINE": baseline_response})
        service = IdeaEvolutionService(runner=runner, runs_dir=self.runs_dir)

        req = EvolutionRequest(
            raw_idea=self.sample_idea,
            treatment_mode=TreatmentMode.FAST_FALLBACK,
        )
        resp = service.evolve(req)

        self.assertTrue(resp.success)
        self.assertEqual(resp.treatment_used, TreatmentMode.FAST_FALLBACK)
        self.assertEqual(resp.total_model_calls, 1)
        self.assertIsNotNone(resp.baseline_result)
        self.assertTrue(resp.baseline_result["success"])

    def test_10_scientific_core_hashes_remain_unchanged(self):
        """11: Invariante do Núcleo Científico: Os 7 arquivos congelados mantêm o hash exato."""
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
        expected_hash = "e6785bcaf5af291f438ab467386db640d4c0790e0f7012c40773dd25782e5600"

        self.assertEqual(
            computed_core_hash,
            expected_hash,
            "VIOLAÇÃO DO NÚCLEO CIENTÍFICO: Os arquivos congelados foram modificados!",
        )

    def test_11_no_paid_fallback_or_hardcoded_keys(self):
        """12: Não há injeção de provedores pagos ou chaves hardcoded no serviço."""
        service_file = Path("src/idea_evolution/service/evolution_service.py")
        content = service_file.read_text(encoding="utf-8")

        self.assertNotIn("csk-", content)
        self.assertNotIn("gsk_", content)
        self.assertNotIn("sk-", content)
        self.assertNotIn("paid", content.lower())
        self.assertNotIn("fallback_to_paid", content.lower())


if __name__ == "__main__":
    unittest.main(verbosity=2)
