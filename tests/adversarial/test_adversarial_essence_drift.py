"""
tests/adversarial/test_adversarial_essence_drift.py
Testes adversariais para detecção de Speculative Feature Accretion e Preservação de Essência (M05.1).
"""

import unittest
import tempfile
from pathlib import Path
from src.idea_evolution.orchestration.simple_loop import SimpleLoopRunner
from src.idea_evolution.providers.fake import FakeModelRunner
from src.idea_evolution.domain.state import RunStatus


class TestAdversarialEssenceDrift(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.runs_path = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_01_speculative_features_isolated_from_core(self):
        """
        Garante que alternativas especulativas (IA federada, gamificação, blockchain)
        sejam mantidas como 'candidate_extensions' e não inchem o 'current_idea' essencial.
        """
        responses = {
            "UNDERSTAND": {
                "interpreted_problem": "Pessoas têm ideias difusas e precisam de perguntas guiadas para estruturá-las.",
                "human_intent": "Transformar ideias vagas em projetos mais claros.",
                "proposed_mechanism": "Questionário socrático guiado e geração de canvas estruturado.",
                "actors_or_users": ["Criadores", "Empreendedores"],
                "assumptions": ["Estruturação lógica reduz abandono."],
                "ambiguities": [],
                "strengths": ["Foco direto em clareza."],
                "structured_idea": "App de perguntas socráticas para maturar ideias.",
            },
            "ALTERNATIVES": {
                "alternatives": [
                    {
                        "mechanism": "Questionário socrático interativo com exportação em Markdown.",
                        "addresses_issues": ["Clareza"],
                        "preserves_intent": True,
                        "tradeoffs": ["Simples, sem rede social."],
                        "novelty_or_difference": "Abordagem minimalista.",
                    },
                    {
                        "mechanism": "Rede social gamificada com backend federado e tokens para validação comunitária.",
                        "addresses_issues": ["Engajamento"],
                        "preserves_intent": False,
                        "tradeoffs": ["Altíssima complexidade e perda de foco."],
                        "novelty_or_difference": "Speculative accretion.",
                    },
                ]
            },
            "SYNTHESIZE": {
                "refined_idea": "Aplicativo de ideação socrática que guia o usuário através de perguntas progressivas de esclarecimento e gera um plano estruturado de projeto.",
                "core_mechanism": "Motor de perguntas socráticas e sumarização em canvas.",
                "core_mechanism_justification": "Atende diretamente à necessidade humana de estruturação progressiva.",
                "accepted_changes": [
                    {
                        "proposal": "Suporte a exportação em Markdown.",
                        "promotion_reason": "Facilita a portabilidade sem adicionar complexidade técnica.",
                        "source_stage": "ALTERNATIVES",
                        "evidence_or_decision_basis": "Formato aberto padrão",
                    }
                ],
                "candidate_possibilities": [
                    "Validação comunitária opcional e rede de mentoria peer-to-peer (CANDIDATE).",
                    "Armazenamento local criptografado para privacidade reforçada (CANDIDATE).",
                ],
                "rejected_changes": [
                    {
                        "proposal": "Backend federado com gamificação e tokens.",
                        "reason_rejected": "Inchaço especulativo (Speculative Feature Accretion) não solicitado pelo usuário humano.",
                        "source_stage": "ALTERNATIVES",
                    }
                ],
                "remaining_uncertainties": [],
                "known_risks": [],
                "recommended_next_step": "Testar questionário com 5 usuários reais.",
            },
            "REALITY_CHECK": {
                "target_core_mechanism": "Motor de perguntas socráticas e sumarização em canvas.",
                "feasibility_notes": ["Questionários socráticos rodam diretamente no cliente com latência zero."],
                "reality_dependencies": ["Exportador de Markdown"],
                "claims_needing_evidence": [],
                "potential_blockers": [],
                "candidate_tests": ["Testar fluidez do questionário com 5 usuários"],
                "exploratory_candidate_tests": [],
            },
            "FINAL_REVIEW": {
                "material_issues_remaining": [],
                "essence_drift_detected": False,
                "speculative_accretion_detected": False,
                "drift_explanation": "",
                "unresolved_critical_issue": False,
                "recommendation": "REFINED_IDEA_READY",
                "review_summary": "Núcleo perfeitamente preservado; extensões especulativas isoladas.",
            },
        }

        runner = FakeModelRunner(custom_responses=responses)
        loop = SimpleLoopRunner(runner=runner, runs_dir=self.runs_path)
        state = loop.run("Um aplicativo que ajuda pessoas a transformar ideias vagas em projetos mais claros.")

        self.assertEqual(state.status, RunStatus.REFINED_IDEA_READY)
        self.assertIn("ideação socrática", state.current_idea)
        self.assertNotIn("blockchain", state.current_idea.lower())
        self.assertNotIn("federado", state.current_idea.lower())
        self.assertEqual(len(state.candidate_extensions), 2)
        self.assertEqual(len(state.rejected_changes), 1)

    def test_02_forced_speculative_accretion_triggers_drift_reconstruction(self):
        """
        Se o modelo tentar forçar inchaço especulativo para dentro do core,
        o FINAL_REVIEW deve acusar speculative_accretion_detected=True e forçar RECONSTRUCT.
        """
        responses = {
            "SYNTHESIZE": {
                "refined_idea": "Plataforma de blockchain com IA federada, gamificação de ideias e rede social de validação descentralizada.",
                "core_mechanism": "Blockchain federado com microserviços.",
                "core_mechanism_justification": "Mecanismo descentralizado",
                "accepted_changes": [
                    {
                        "proposal": "Transformado em plataforma Web3.",
                        "promotion_reason": "Descentralização forçada",
                        "source_stage": "ALTERNATIVES",
                        "evidence_or_decision_basis": "Hype tecnológico",
                    }
                ],
                "candidate_possibilities": [],
                "rejected_changes": [],
                "remaining_uncertainties": [],
                "known_risks": [],
                "recommended_next_step": "Deploy de smart contracts.",
            },
            "FINAL_REVIEW": {
                "material_issues_remaining": ["Inchaço especulativo extremo."],
                "essence_drift_detected": True,
                "speculative_accretion_detected": True,
                "drift_explanation": "A ideia original pedia apenas clareza para ideias vagas, mas o sistema adicionou blockchain e rede social sem justificativa.",
                "unresolved_critical_issue": True,
                "recommendation": "RECONSTRUCT",
                "review_summary": "Reconstrução exigida por inchaço especulativo.",
            },
        }

        runner = FakeModelRunner(custom_responses=responses)
        loop = SimpleLoopRunner(runner=runner, runs_dir=self.runs_path)
        state = loop.run("Um aplicativo que ajuda pessoas a transformar ideias vagas em projetos mais claros.")

        # O estado deve registrar reconstrução e detecção de drift
        self.assertTrue(state.essence_drift_detected)
        self.assertTrue(state.speculative_accretion_detected)
        self.assertEqual(state.reconstruction_count, 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
