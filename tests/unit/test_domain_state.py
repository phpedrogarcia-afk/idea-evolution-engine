"""
tests/unit/test_domain_state.py
Testes unitários para o estado compartilhado do IEE (SimpleIdeaState).
"""

import unittest
import json
from src.idea_evolution.domain.state import SimpleIdeaState, RunStatus, CriticalIssue, AlternativeMechanism


class TestDomainState(unittest.TestCase):

    def test_01_state_initialization(self):
        state = SimpleIdeaState(
            run_id="RUN-TEST-001",
            original_idea="Uma nova ideia de teste.",
            status=RunStatus.INITIALIZED,
        )
        self.assertEqual(state.run_id, "RUN-TEST-001")
        self.assertEqual(state.original_idea, "Uma nova ideia de teste.")
        self.assertEqual(state.status, RunStatus.INITIALIZED)
        self.assertEqual(state.reconstruction_count, 0)
        self.assertEqual(state.max_reconstructions, 1)

    def test_02_original_idea_immutability_and_evolution(self):
        state = SimpleIdeaState(
            run_id="RUN-TEST-002",
            original_idea="Texto imutável original.",
        )
        # Evolução ocorre em current_idea, original_idea permanece intacta
        state.current_idea = "Texto evoluído após UNDERSTAND e ATTACK."
        self.assertEqual(state.original_idea, "Texto imutável original.")
        self.assertEqual(state.current_idea, "Texto evoluído após UNDERSTAND e ATTACK.")

    def test_03_stage_history_recording(self):
        state = SimpleIdeaState(
            run_id="RUN-TEST-003",
            original_idea="Ideia para teste de histórico.",
        )
        state.record_stage_execution(
            stage_id="UNDERSTAND",
            stage_version="0.1.0",
            provider="fake",
            model="fake-model",
            success=True,
            retry_count=0,
            delta_summary="Intenção extraída com sucesso.",
        )
        self.assertEqual(len(state.stage_history), 1)
        self.assertEqual(state.stage_history[0].stage_id, "UNDERSTAND")
        self.assertTrue(state.stage_history[0].success)

    def test_04_human_markdown_generation(self):
        state = SimpleIdeaState(
            run_id="RUN-TEST-004",
            original_idea="Ideia de teste para Markdown.",
            human_intent="Intenção clara do usuário.",
            problem_statement="Problema formulado.",
            current_idea="Versão refinada e robusta.",
            status=RunStatus.REFINED_IDEA_READY,
        )
        state.critical_issues.append(
            CriticalIssue(issue="Falha potencial", why_it_matters="Pode quebrar", severity="HIGH")
        )
        md = state.to_human_markdown()
        self.assertIn("# Pacote de Maturação da Ideia", md)
        self.assertIn("Ideia Original (Imutável)", md)
        self.assertIn("Falha potencial", md)
        self.assertIn("REFINED_IDEA_READY", md)


if __name__ == "__main__":
    unittest.main(verbosity=2)
