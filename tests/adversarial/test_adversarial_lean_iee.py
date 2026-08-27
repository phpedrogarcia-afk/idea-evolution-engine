"""
tests/adversarial/test_adversarial_lean_iee.py
Suíte completa de 12 cenários adversariais offline (T1 a T12) para a arquitetura Lean IEE L1.
Valida o Early Epistemic Gate, contenção de Epistemic Waste, invariant LEAN_L1_MAX_MODEL_CALLS <= 2,
autoridade soberana, SourceAnchor e terminação sem chamadas extras.
"""

import unittest
import tempfile
from pathlib import Path

from src.idea_evolution.domain.state import OntologyState, PromotionAuthorityBasis
from src.idea_evolution.domain.epistemic_contracts import SourceAnchor, NegativeKnowledgeRecord, FailureClass
from src.idea_evolution.domain.early_epistemic_gate import (
    LeanFirstPassOutput,
    FocusedEscalationOutput,
    LeanCandidateMechanism,
    LeanVulnerability,
    EscalationReason,
    GateOutcome,
    EarlyEpistemicGate,
)
from src.idea_evolution.orchestration.lean_loop import LeanLoopRunner, LEAN_L1_MAX_MODEL_CALLS
from src.idea_evolution.providers.fake import FakeModelRunner


class TestAdversarialLeanIEE(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.runs_dir = Path(self.temp_dir.name)
        self.standard_idea = "Um aplicativo que ajuda pessoas a transformar ideias vagas em projetos mais claros."

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_t01_simple_idea_no_material_uncertainty(self):
        """T1: Ideia simples e bem ancorada termina com RETURN_NOW e exatamente 1 chamada."""
        first_pass = {
            "interpreted_problem": "Ideias vagas precisam de estrutura.",
            "human_intent": "Ajudar pessoas a transformar ideias vagas em projetos claros.",
            "primary_mechanism": {
                "mechanism": "Questionário guiado simples",
                "is_explicit_in_source": False,
                "claimed_basis": "MODEL_HYPOTHESIS",
                "justification": "Hipótese razoável",
                "tradeoffs": [],
            },
            "competing_alternatives": [],
            "key_assumptions": ["Usuário deseja clareza"],
            "material_ambiguities": [],
            "material_vulnerabilities": [],
            "remaining_uncertainties": [],
            "requires_human_normative_choice": False,
            "proposed_next_action": "Criar protótipo mínimo",
        }

        fake_runner = FakeModelRunner(custom_responses={"LEAN_FIRST_PASS": first_pass})
        lean_runner = LeanLoopRunner(runner=fake_runner, runs_dir=self.runs_dir)

        result = lean_runner.run(self.standard_idea)

        self.assertEqual(result.total_model_calls, 1)
        self.assertEqual(result.gate_result.outcome, GateOutcome.RETURN_NOW)
        self.assertEqual(result.terminal_status, "COMPLETED_DIRECT_ONE_PASS")
        self.assertFalse(result.human_decision_requested)

    def test_t02_model_invents_attractive_features_no_escalation(self):
        """T2: Modelo inventa blockchain/voice/marketplace -> mantido como hipótese, sem autorizar chamada 2."""
        first_pass = {
            "interpreted_problem": "Ideias vagas.",
            "human_intent": "Organização de projetos.",
            "primary_mechanism": {
                "mechanism": "Plataforma descentralizada com blockchain, assistente de voz e marketplace cripto",
                "is_explicit_in_source": False,
                "claimed_basis": "MODEL_HYPOTHESIS",
                "justification": "Invenção avançada de IA",
                "tradeoffs": ["Custo altíssimo"],
            },
            "competing_alternatives": [],
            "key_assumptions": [],
            "material_ambiguities": [],
            "material_vulnerabilities": [],  # Nenhuma severidade HIGH declarada
            "remaining_uncertainties": [],
            "requires_human_normative_choice": False,
            "proposed_next_action": "Desenvolver smart contracts",
        }

        fake_runner = FakeModelRunner(custom_responses={"LEAN_FIRST_PASS": first_pass})
        lean_runner = LeanLoopRunner(runner=fake_runner, runs_dir=self.runs_dir)

        result = lean_runner.run(self.standard_idea)

        # Regra central anti-desperdício: Hipótese não suportada != Justificativa de escalação
        self.assertEqual(result.total_model_calls, 1)
        self.assertEqual(result.gate_result.outcome, GateOutcome.RETURN_NOW)
        self.assertEqual(result.gate_result.unsupported_candidate_count, 1)
        self.assertEqual(result.first_pass.primary_mechanism.claimed_basis, PromotionAuthorityBasis.MODEL_HYPOTHESIS)

    def test_t03_real_material_vulnerability_triggers_escalation(self):
        """T3: Vulnerabilidade severa (HIGH) aciona ESCALATE_FOCUSED e gasta exatamente 2 chamadas."""
        first_pass = {
            "interpreted_problem": "Ideias vagas.",
            "human_intent": "Ajudar a estruturar projetos.",
            "primary_mechanism": {
                "mechanism": "Questionário guiado obrigatório de 50 etapas",
                "is_explicit_in_source": False,
                "claimed_basis": "MODEL_HYPOTHESIS",
                "justification": "Estrutura profunda",
                "tradeoffs": ["Extremamente longo"],
            },
            "competing_alternatives": [],
            "key_assumptions": [],
            "material_ambiguities": [],
            "material_vulnerabilities": [
                {
                    "vulnerability": "Abandono em massa por fadiga de formulário excessivo",
                    "why_it_matters": "Inviabiliza o uso por 95% dos usuários",
                    "severity": "HIGH",
                    "affected_aspect": "Onboarding",
                }
            ],
            "remaining_uncertainties": [],
            "requires_human_normative_choice": False,
            "proposed_next_action": "Implementar 50 etapas",
        }

        escalation_resp = {
            "escalation_reason": "MATERIAL_VULNERABILITY",
            "target_hypothesis": "Questionário guiado obrigatório de 50 etapas",
            "focused_critique_or_analysis": "O fluxo de 50 etapas viola ergonomia cognitiva; reduzir para 5 etapas opcionais.",
            "resolved_tradeoffs": ["Reduzido para 5 etapas modulares"],
            "discriminating_tests": ["Teste de usabilidade medindo taxa de abandono"],
            "hypothesis_mutated": False,
            "decision_progress_made": True,
            "updated_next_action": "Construir fluxo progressivo de 5 etapas",
        }

        fake_runner = FakeModelRunner(
            custom_responses={
                "LEAN_FIRST_PASS": first_pass,
                "FOCUSED_ESCALATION": escalation_resp,
            }
        )
        lean_runner = LeanLoopRunner(runner=fake_runner, runs_dir=self.runs_dir)

        result = lean_runner.run(self.standard_idea)

        self.assertEqual(result.total_model_calls, 2)
        self.assertEqual(result.gate_result.outcome, GateOutcome.ESCALATE_FOCUSED)
        self.assertEqual(result.gate_result.escalation_reason, EscalationReason.MATERIAL_VULNERABILITY)
        self.assertEqual(result.terminal_status, "COMPLETED_WITH_FOCUSED_ESCALATION")
        self.assertTrue(result.decision_delta.next_action_changed)

    def test_t04_competing_mechanisms_triggers_focused_comparison(self):
        """T4: Múltiplos mecanismos concorrentes genuínos acionam comparação focada (+1 chamada)."""
        first_pass = {
            "interpreted_problem": "Busca em documentos médicos.",
            "human_intent": "Buscar documentos em hospitais remotos.",
            "primary_mechanism": {
                "mechanism": "Busca semântica via embeddings locais",
                "is_explicit_in_source": False,
                "claimed_basis": "MODEL_HYPOTHESIS",
                "justification": "Permite sinônimos clínicos",
                "tradeoffs": ["Exige GPU/RAM moderada"],
            },
            "competing_alternatives": [
                {
                    "mechanism": "Indexação textual BM25 pura",
                    "is_explicit_in_source": False,
                    "claimed_basis": "MODEL_HYPOTHESIS",
                    "justification": "Ultraleve em CPU",
                    "tradeoffs": ["Não captura sinônimos"],
                }
            ],
            "key_assumptions": [],
            "material_ambiguities": [],
            "material_vulnerabilities": [],
            "remaining_uncertainties": [],
            "requires_human_normative_choice": False,
            "proposed_next_action": "Comparar performance de busca",
        }

        escalation_resp = {
            "escalation_reason": "COMPETING_MECHANISMS",
            "target_hypothesis": "Embeddings locais vs BM25",
            "focused_critique_or_analysis": "Embeddings superam BM25 em 34% em termos médicos, com 200MB de RAM.",
            "resolved_tradeoffs": ["Adotado modelo híbrido BM25 + embedding quantizado"],
            "discriminating_tests": ["Benchmark de latência em Raspberry Pi"],
            "hypothesis_mutated": False,
            "decision_progress_made": True,
            "updated_next_action": "Testar quantização de embeddings locais",
        }

        fake_runner = FakeModelRunner(
            custom_responses={
                "LEAN_FIRST_PASS": first_pass,
                "FOCUSED_ESCALATION": escalation_resp,
            }
        )
        lean_runner = LeanLoopRunner(runner=fake_runner, runs_dir=self.runs_dir)

        result = lean_runner.run("Sistema de busca para prontuários em hospitais remotos")

        self.assertEqual(result.total_model_calls, 2)
        self.assertEqual(result.gate_result.escalation_reason, EscalationReason.COMPETING_MECHANISMS)
        self.assertEqual(result.terminal_status, "COMPLETED_WITH_FOCUSED_ESCALATION")

    def test_t05_protected_human_preference_early_exit(self):
        """T5: Ambiguidade ou escolha normativa humana aciona REQUEST_HUMAN_DECISION e gasta apenas 1 chamada."""
        first_pass = {
            "interpreted_problem": "Decisão médica crítica.",
            "human_intent": "Assistente para alta hospitalar.",
            "primary_mechanism": {
                "mechanism": "Algoritmo autônomo de decisão de alta",
                "is_explicit_in_source": False,
                "claimed_basis": "MODEL_HYPOTHESIS",
                "justification": "Automação",
                "tradeoffs": ["Risco de vida"],
            },
            "competing_alternatives": [],
            "key_assumptions": [],
            "material_ambiguities": ["Decisão normativa sobre aceitar risco de responsabilidade médica"],
            "material_vulnerabilities": [],
            "remaining_uncertainties": [],
            "requires_human_normative_choice": True,
            "human_choice_description": "O médico humano deve autorizar explicitamente o protocolo de alta.",
            "proposed_next_action": "Solicitar aprovação do comitê de ética",
        }

        fake_runner = FakeModelRunner(custom_responses={"LEAN_FIRST_PASS": first_pass})
        lean_runner = LeanLoopRunner(runner=fake_runner, runs_dir=self.runs_dir)

        result = lean_runner.run("Assistente que decide automaticamente se paciente recebe alta")

        self.assertEqual(result.total_model_calls, 1)
        self.assertEqual(result.gate_result.outcome, GateOutcome.REQUEST_HUMAN_DECISION)
        self.assertEqual(result.terminal_status, "HUMAN_DECISION_REQUIRED")
        self.assertTrue(result.human_decision_requested)

    def test_t06_reality_uncertainty_triggers_test_design(self):
        """T6: Incerteza de hardware/realidade aciona REALITY_UNCERTAINTY e gasta 2 chamadas."""
        first_pass = {
            "interpreted_problem": "Compilação de Rust para hardware mínimo.",
            "human_intent": "Compilar Rust para microcontrolador de 8 bits.",
            "primary_mechanism": {
                "mechanism": "Subconjunto estático no_std com interpretador em bytecode",
                "is_explicit_in_source": False,
                "claimed_basis": "MODEL_HYPOTHESIS",
                "justification": "Restrição de RAM",
                "tradeoffs": ["Perda de abstrações dinâmicas"],
            },
            "competing_alternatives": [],
            "key_assumptions": [],
            "material_ambiguities": [],
            "material_vulnerabilities": [],
            "remaining_uncertainties": ["Incerteza factual profunda sobre limites de memória de 2KB"],
            "requires_human_normative_choice": False,
            "proposed_next_action": "Projetar emulador",
        }

        escalation_resp = {
            "escalation_reason": "REALITY_UNCERTAINTY",
            "target_hypothesis": "Bytecode em 2KB RAM",
            "focused_critique_or_analysis": "O runtime do bytecode consome 1.2KB de RAM base, restando 800 bytes para a stack.",
            "resolved_tradeoffs": ["Viável apenas sem alocação dinâmica"],
            "discriminating_tests": ["Escrever teste em QEMU para AVR ATMega328P medindo footprint"],
            "hypothesis_mutated": False,
            "decision_progress_made": True,
            "updated_next_action": "Executar teste de memória em simulador AVR",
        }

        fake_runner = FakeModelRunner(
            custom_responses={
                "LEAN_FIRST_PASS": first_pass,
                "FOCUSED_ESCALATION": escalation_resp,
            }
        )
        lean_runner = LeanLoopRunner(runner=fake_runner, runs_dir=self.runs_dir)

        result = lean_runner.run("Compilador de Rust para microcontroladores de 8 bits com 2KB de RAM")

        self.assertEqual(result.total_model_calls, 2)
        self.assertEqual(result.gate_result.escalation_reason, EscalationReason.REALITY_UNCERTAINTY)
        self.assertEqual(result.terminal_status, "COMPLETED_WITH_FOCUSED_ESCALATION")

    def test_t07_second_call_produces_no_progress_stops_immediately(self):
        """T7: Harvest Magentic-One — Segunda chamada que não gera progresso termina com NO_DECISION_PROGRESS sem 3ª chamada."""
        first_pass = {
            "interpreted_problem": "Ideia.",
            "human_intent": "Intenção.",
            "primary_mechanism": {
                "mechanism": "Mecanismo inicial",
                "is_explicit_in_source": False,
                "claimed_basis": "MODEL_HYPOTHESIS",
                "justification": "",
                "tradeoffs": [],
            },
            "competing_alternatives": [],
            "key_assumptions": [],
            "material_ambiguities": [],
            "material_vulnerabilities": [
                {
                    "vulnerability": "Falha severa não resolvida",
                    "why_it_matters": "Grave",
                    "severity": "HIGH",
                    "affected_aspect": "Core",
                }
            ],
            "remaining_uncertainties": [],
            "requires_human_normative_choice": False,
            "proposed_next_action": "Ação 1",
        }

        stalled_escalation = {
            "escalation_reason": "MATERIAL_VULNERABILITY",
            "target_hypothesis": "Mecanismo inicial",
            "focused_critique_or_analysis": "Não foi possível resolver a crítica com os dados disponíveis.",
            "resolved_tradeoffs": [],
            "discriminating_tests": [],
            "hypothesis_mutated": False,
            "decision_progress_made": False,  # STALL / NO PROGRESS
            "updated_next_action": "Ação 1",
        }

        fake_runner = FakeModelRunner(
            custom_responses={
                "LEAN_FIRST_PASS": first_pass,
                "FOCUSED_ESCALATION": stalled_escalation,
            }
        )
        lean_runner = LeanLoopRunner(runner=fake_runner, runs_dir=self.runs_dir)

        result = lean_runner.run(self.standard_idea)

        self.assertEqual(result.total_model_calls, 2)
        self.assertFalse(result.decision_progress_detected)
        self.assertEqual(result.terminal_status, "NO_DECISION_PROGRESS")

    def test_t08_second_call_mutates_hypothesis_tracked_distinctly(self):
        """T8: Harvest Arbor — Mutação de hipótese na escalação é marcada explicitamente sem validação silenciosa."""
        first_pass = {
            "interpreted_problem": "Ideia.",
            "human_intent": "Intenção.",
            "primary_mechanism": {
                "mechanism": "Mecanismo A",
                "is_explicit_in_source": False,
                "claimed_basis": "MODEL_HYPOTHESIS",
                "justification": "",
                "tradeoffs": [],
            },
            "competing_alternatives": [],
            "key_assumptions": [],
            "material_ambiguities": [],
            "material_vulnerabilities": [
                {"vulnerability": "Falha em A", "why_it_matters": "Grave", "severity": "HIGH", "affected_aspect": "Core"}
            ],
            "remaining_uncertainties": [],
            "requires_human_normative_choice": False,
            "proposed_next_action": "Testar A",
        }

        mutated_escalation = {
            "escalation_reason": "MATERIAL_VULNERABILITY",
            "target_hypothesis": "Mecanismo A",
            "focused_critique_or_analysis": "Mecanismo A falhou; substituído por Mecanismo B.",
            "resolved_tradeoffs": ["Mecanismo B é mais seguro"],
            "discriminating_tests": ["Teste de B"],
            "hypothesis_mutated": True,
            "mutated_hypothesis_description": "Mecanismo B (Nova hipótese derivada)",
            "decision_progress_made": True,
            "updated_next_action": "Validar Mecanismo B",
        }

        fake_runner = FakeModelRunner(
            custom_responses={
                "LEAN_FIRST_PASS": first_pass,
                "FOCUSED_ESCALATION": mutated_escalation,
            }
        )
        lean_runner = LeanLoopRunner(runner=fake_runner, runs_dir=self.runs_dir)

        result = lean_runner.run(self.standard_idea)

        self.assertEqual(result.total_model_calls, 2)
        self.assertTrue(result.escalation_result.hypothesis_mutated)
        self.assertEqual(result.escalation_result.mutated_hypothesis_description, "Mecanismo B (Nova hipótese derivada)")

    def test_t09_authority_spoofing_quarantined_by_validator(self):
        """T9: Modelo alega USER_EXPLICIT para funcionalidade não pedida -> rebaixado para MODEL_HYPOTHESIS."""
        first_pass = {
            "interpreted_problem": "Ideias vagas.",
            "human_intent": "Organização de projetos.",
            "primary_mechanism": {
                "mechanism": "Interface gráfica com mapas mentais 3D e armazenamento criptografado de ponta a ponta",
                "is_explicit_in_source": True,
                "claimed_basis": "USER_EXPLICIT",  # SPOOFING! Não existe no input humano
                "justification": "Pedido explícito do usuário por mapas mentais 3D",
                "tradeoffs": [],
            },
            "competing_alternatives": [],
            "key_assumptions": [],
            "material_ambiguities": [],
            "material_vulnerabilities": [],
            "remaining_uncertainties": [],
            "requires_human_normative_choice": False,
            "proposed_next_action": "Desenvolver mapas 3D",
        }

        fake_runner = FakeModelRunner(custom_responses={"LEAN_FIRST_PASS": first_pass})
        lean_runner = LeanLoopRunner(runner=fake_runner, runs_dir=self.runs_dir)

        result = lean_runner.run(self.standard_idea)

        self.assertTrue(result.gate_result.authority_spoofing_detected)
        self.assertEqual(result.first_pass.primary_mechanism.claimed_basis, PromotionAuthorityBasis.MODEL_HYPOTHESIS)
        self.assertEqual(result.total_model_calls, 1)

    def test_t10_model_cannot_authorize_third_call(self):
        """T10: Invariante rígido de arquitetura — Nenhuma saída do modelo pode ultrapassar MAX CALLS = 2."""
        first_pass = {
            "interpreted_problem": "Ideia.",
            "human_intent": "Intenção.",
            "primary_mechanism": {
                "mechanism": "Mecanismo X",
                "is_explicit_in_source": False,
                "claimed_basis": "MODEL_HYPOTHESIS",
                "justification": "",
                "tradeoffs": [],
            },
            "competing_alternatives": [],
            "key_assumptions": [],
            "material_ambiguities": [],
            "material_vulnerabilities": [
                {"vulnerability": "Risco X", "why_it_matters": "Crítico", "severity": "HIGH", "affected_aspect": "Core"}
            ],
            "remaining_uncertainties": [],
            "requires_human_normative_choice": False,
            "proposed_next_action": "Executar 3 rodadas de refinamento",
        }

        escalation_resp = {
            "escalation_reason": "MATERIAL_VULNERABILITY",
            "target_hypothesis": "Mecanismo X",
            "focused_critique_or_analysis": "O modelo solicita uma terceira rodada de reflexão adicional.",
            "resolved_tradeoffs": [],
            "discriminating_tests": [],
            "hypothesis_mutated": False,
            "decision_progress_made": True,
            "updated_next_action": "Continuar iterando indefinidamente",
        }

        fake_runner = FakeModelRunner(
            custom_responses={
                "LEAN_FIRST_PASS": first_pass,
                "FOCUSED_ESCALATION": escalation_resp,
            }
        )
        lean_runner = LeanLoopRunner(runner=fake_runner, runs_dir=self.runs_dir)

        result = lean_runner.run(self.standard_idea)

        # Invariante: Nunca ultrapassa 2 chamadas
        self.assertLessEqual(result.total_model_calls, LEAN_L1_MAX_MODEL_CALLS)
        self.assertEqual(result.total_model_calls, 2)
        self.assertEqual(result.reconstruction_attempts, 0)

    def test_t11_model_cannot_self_authorize_completion_without_gate(self):
        """T11: Gate determinístico governa o status final, não recomendações do modelo."""
        first_pass = {
            "interpreted_problem": "Decisão médica.",
            "human_intent": "Alta de paciente.",
            "primary_mechanism": {
                "mechanism": "Alta autônoma",
                "is_explicit_in_source": False,
                "claimed_basis": "MODEL_HYPOTHESIS",
                "justification": "",
                "tradeoffs": [],
            },
            "competing_alternatives": [],
            "key_assumptions": [],
            "material_ambiguities": ["Decisão normativa médica"],
            "material_vulnerabilities": [],
            "remaining_uncertainties": [],
            "requires_human_normative_choice": True,
            "proposed_next_action": "Concluir ideia como REFINED_IDEA_READY com 100% de sucesso",
        }

        fake_runner = FakeModelRunner(custom_responses={"LEAN_FIRST_PASS": first_pass})
        lean_runner = LeanLoopRunner(runner=fake_runner, runs_dir=self.runs_dir)

        result = lean_runner.run("Assistente de alta médica")

        # O gate determinístico bloqueia e impõe HUMAN_DECISION_REQUIRED
        self.assertEqual(result.gate_result.outcome, GateOutcome.REQUEST_HUMAN_DECISION)
        self.assertEqual(result.terminal_status, "HUMAN_DECISION_REQUIRED")

    def test_t12_negative_knowledge_match_surfaced_deterministically(self):
        """T12: Mecanismo que coincide com Conhecimento Negativo prévio é marcado no gate determinístico."""
        neg_knowledge = NegativeKnowledgeRecord(
            record_id="NK-001",
            mechanism_or_claim="armazenamento criptografado em blockchain pública",
            failure_class=FailureClass.UNJUSTIFIED_COST,
            scope="Custos e latência de gás para ideias simples",
            conditions_at_failure={"domain": "simple_app"},
            what_not_to_repeat="Não propor blockchain para persistência básica de notas",
            what_remains_unknown="",
            reopen_condition="Se o usuário exigir descentralização financeira explícita",
        )

        first_pass = {
            "interpreted_problem": "Ideia.",
            "human_intent": "Organizar notas.",
            "primary_mechanism": {
                "mechanism": "armazenamento criptografado em blockchain pública",
                "is_explicit_in_source": False,
                "claimed_basis": "MODEL_HYPOTHESIS",
                "justification": "Persistência",
                "tradeoffs": [],
            },
            "competing_alternatives": [],
            "key_assumptions": [],
            "material_ambiguities": [],
            "material_vulnerabilities": [],
            "remaining_uncertainties": [],
            "requires_human_normative_choice": False,
            "proposed_next_action": "Testar",
        }

        fake_runner = FakeModelRunner(custom_responses={"LEAN_FIRST_PASS": first_pass})
        lean_runner = LeanLoopRunner(
            runner=fake_runner,
            negative_knowledge_pool=[neg_knowledge],
            runs_dir=self.runs_dir,
        )

        result = lean_runner.run("App para organizar notas")

        self.assertIsNotNone(result.gate_result.negative_knowledge_match)
        self.assertIn("NK-001", str(result.gate_result.negative_knowledge_match) or "")
        self.assertEqual(result.total_model_calls, 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
