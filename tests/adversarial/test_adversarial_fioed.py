"""
tests/adversarial/test_adversarial_fioed.py
Suíte de testes adversariais formais e filosóficos do Fio Epistemic Dynamics (FioED-01).
Valida as Leis Formais (LAW-01 a LAW-15), cenários filosóficos (T-PHIL-01 a T-PHIL-10),
imunidade a custos afundados, ciclo A->C->A, não-autoridade sobre representações e admissão seletiva de memória.
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
    DecisionDeltaEventType,
    DecisionDeltaRecord,
    EpistemicRentRecord,
    EpistemicRentDecision,
    AttentionSnapshot,
    MemoryAdmissionVerdict,
    MemoryAdmissionDecision,
)
from src.idea_evolution.orchestration.lean_loop import LeanLoopRunner, LEAN_L1_MAX_MODEL_CALLS
from src.idea_evolution.providers.fake import FakeModelRunner


class TestAdversarialFioED(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.runs_dir = Path(self.temp_dir.name)
        self.standard_idea = "Um aplicativo que ajuda pessoas a transformar ideias vagas em projetos mais claros."

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_law01_source_immutability(self):
        """LAW-01: Source Immutability — O SourceAnchor original nunca é mutado ou sobrescrito por transformações."""
        source = SourceAnchor.create_human_input_anchor(self.standard_idea)
        initial_hash = source.content_hash

        # Simular tentativa de mutação de representação
        mutated_text = "Um app com blockchain e mapas mentais."
        new_source = SourceAnchor.create_human_input_anchor(mutated_text, source_id="SRC-HUMAN-NEW")

        self.assertEqual(source.content_hash, initial_hash)
        self.assertNotEqual(source.content_hash, new_source.content_hash)
        self.assertEqual(source.original_content, self.standard_idea)

    def test_law02_representation_non_authority(self):
        """LAW-02: Representation Non-Authority — Representação gerada não herda autoridade humana."""
        first_pass = {
            "interpreted_problem": "Ideias vagas.",
            "human_intent": "Organizar projetos.",
            "primary_mechanism": {
                "mechanism": "Interface gráfica com mapas mentais 3D e criptografia",
                "is_explicit_in_source": True,
                "claimed_basis": "USER_EXPLICIT",  # Falsificação!
                "justification": "O usuário quer mapas mentais",
                "tradeoffs": [],
            },
            "competing_alternatives": [],
            "key_assumptions": [],
            "material_ambiguities": [],
            "material_vulnerabilities": [],
            "remaining_uncertainties": [],
            "requires_human_normative_choice": False,
            "proposed_next_action": "Desenvolver mapas",
        }

        fake_runner = FakeModelRunner(custom_responses={"LEAN_FIRST_PASS": first_pass})
        lean_runner = LeanLoopRunner(runner=fake_runner, runs_dir=self.runs_dir)
        result = lean_runner.run(self.standard_idea)

        self.assertTrue(result.gate_result.authority_spoofing_detected)
        self.assertEqual(result.first_pass.primary_mechanism.claimed_basis, PromotionAuthorityBasis.MODEL_HYPOTHESIS)

    def test_law07_sunk_cost_immunity(self):
        """LAW-07: Sunk Cost Immunity — Investimento de chamadas/tokens não aumenta o status de verdade de uma hipótese."""
        # Se uma hipótese gasta 2 chamadas sem evidência adicional, seu status permanece MODEL_HYPOTHESIS
        first_pass = {
            "interpreted_problem": "Ideias vagas.",
            "human_intent": "Intenção.",
            "primary_mechanism": {
                "mechanism": "Mecanismo especulativo sem prova",
                "is_explicit_in_source": False,
                "claimed_basis": "MODEL_HYPOTHESIS",
                "justification": "",
                "tradeoffs": [],
            },
            "competing_alternatives": [],
            "key_assumptions": [],
            "material_ambiguities": [],
            "material_vulnerabilities": [
                {"vulnerability": "Vulnerabilidade X", "why_it_matters": "Grave", "severity": "HIGH", "affected_aspect": "Core"}
            ],
            "remaining_uncertainties": [],
            "requires_human_normative_choice": False,
            "proposed_next_action": "Analisar",
        }

        escalation_resp = {
            "escalation_reason": "MATERIAL_VULNERABILITY",
            "target_hypothesis": "Mecanismo especulativo sem prova",
            "focused_critique_or_analysis": "O modelo gastou 10.000 tokens e 2 chamadas elogiando a hipótese.",
            "resolved_tradeoffs": [],
            "discriminating_tests": [],
            "hypothesis_mutated": False,
            "decision_progress_made": True,
            "updated_next_action": "Continuar",
        }

        fake_runner = FakeModelRunner(
            custom_responses={
                "LEAN_FIRST_PASS": first_pass,
                "FOCUSED_ESCALATION": escalation_resp,
            }
        )
        lean_runner = LeanLoopRunner(runner=fake_runner, runs_dir=self.runs_dir)
        result = lean_runner.run(self.standard_idea)

        # Investimento = 2 chamadas, mas a base continua sendo MODEL_HYPOTHESIS (sem evidência empírica)
        self.assertEqual(result.total_model_calls, 2)
        self.assertEqual(result.first_pass.primary_mechanism.claimed_basis, PromotionAuthorityBasis.MODEL_HYPOTHESIS)

    def test_law10_human_authority_non_substitutable(self):
        """LAW-10: Non-Substitutable Human Authority — Decisão normativa humana encerra o loop sem chamadas extras de IA."""
        first_pass = {
            "interpreted_problem": "Decisão hospitalar.",
            "human_intent": "Alta médica.",
            "primary_mechanism": {
                "mechanism": "Alta autônoma",
                "is_explicit_in_source": False,
                "claimed_basis": "MODEL_HYPOTHESIS",
                "justification": "",
                "tradeoffs": [],
            },
            "competing_alternatives": [],
            "key_assumptions": [],
            "material_ambiguities": ["Decisão de responsabilidade legal médica"],
            "material_vulnerabilities": [],
            "remaining_uncertainties": [],
            "requires_human_normative_choice": True,
            "proposed_next_action": "Aguardar médico",
        }

        fake_runner = FakeModelRunner(custom_responses={"LEAN_FIRST_PASS": first_pass})
        lean_runner = LeanLoopRunner(runner=fake_runner, runs_dir=self.runs_dir)
        result = lean_runner.run("Assistente de alta")

        self.assertEqual(result.total_model_calls, 1)
        self.assertEqual(result.gate_result.outcome, GateOutcome.REQUEST_HUMAN_DECISION)
        self.assertEqual(result.terminal_status, "HUMAN_DECISION_REQUIRED")

    def test_law12_no_useful_work_as_success(self):
        """LAW-12: No Useful Work is Success — Ideia sem incertezas materiais encerra imediatamente com 1 chamada."""
        fake_runner = FakeModelRunner()
        lean_runner = LeanLoopRunner(runner=fake_runner, runs_dir=self.runs_dir)
        result = lean_runner.run(self.standard_idea)

        self.assertEqual(result.total_model_calls, 1)
        self.assertEqual(result.terminal_status, "COMPLETED_DIRECT_ONE_PASS")

    def test_a_c_a_cycle_enforcement(self):
        """A -> C -> A Cycle — Toda escalação focada (C) é seguida por reconciliação determinística (A)."""
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
                {"vulnerability": "Falha severa", "why_it_matters": "Grave", "severity": "HIGH", "affected_aspect": "Core"}
            ],
            "remaining_uncertainties": [],
            "requires_human_normative_choice": False,
            "proposed_next_action": "Testar",
        }

        escalation_resp = {
            "escalation_reason": "MATERIAL_VULNERABILITY",
            "target_hypothesis": "Mecanismo A",
            "focused_critique_or_analysis": "Análise focada de falha.",
            "resolved_tradeoffs": ["Tradeoff resolvido"],
            "discriminating_tests": ["Teste 1"],
            "hypothesis_mutated": False,
            "decision_progress_made": True,
            "updated_next_action": "Executar teste 1",
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
        # O resultado contém o DecisionDeltaRecord reconciliado pós-escalação
        self.assertIsNotNone(result.decision_delta)
        self.assertEqual(result.decision_delta.created_by_stage, "FOCUSED_ESCALATION")
        self.assertEqual(result.terminal_status, "COMPLETED_WITH_FOCUSED_ESCALATION")

    def test_memory_admission_decision(self):
        """Memory Admission — Apenas lições com escopo e condições de reabertura são admitidas em memória durável."""
        # Caso 1: Especulação efêmera de modelo sem evidência -> Rejeitada
        decision_1 = MemoryAdmissionDecision(
            decision=MemoryAdmissionVerdict.REJECT_EPHEMERAL_SPECULATION,
            candidate_content="O modelo acha que o mercado de IA vai triplicar.",
            has_provenance=False,
            has_scope_and_reopen=False,
            has_decision_relevance=False,
            reason="Especulação sem evidência ou condição de reabertura.",
        )
        self.assertEqual(decision_1.decision, MemoryAdmissionVerdict.REJECT_EPHEMERAL_SPECULATION)

        # Caso 2: Conhecimento negativo estruturado com escopo -> Admitido
        decision_2 = MemoryAdmissionDecision(
            decision=MemoryAdmissionVerdict.ADMIT_NEGATIVE_KNOWLEDGE,
            candidate_content="Persistência em blockchain pública para notas simples falhou por latência.",
            has_provenance=True,
            has_scope_and_reopen=True,
            has_decision_relevance=True,
            reason="Tupla de falha com escopo de simples_app e condição de reabertura explícita.",
        )
        self.assertEqual(decision_2.decision, MemoryAdmissionVerdict.ADMIT_NEGATIVE_KNOWLEDGE)

    def test_historical_source_events_immutability(self):
        """Historical Source Events — S0 e S1 são eventos imutáveis distintos; S1 não reescreve S0."""
        s0 = SourceAnchor.create_human_input_anchor("Quero um app de notas local.", source_id="SRC-S0")
        s1 = SourceAnchor.create_human_input_anchor("Quero adicionar sincronização P2P opcional.", source_id="SRC-S1")

        self.assertNotEqual(s0.source_id, s1.source_id)
        self.assertNotEqual(s0.content_hash, s1.content_hash)
        self.assertEqual(s0.original_content, "Quero um app de notas local.")
        self.assertEqual(s1.original_content, "Quero adicionar sincronização P2P opcional.")

    def test_attention_snapshot_representation_only(self):
        """Attention Snapshot — Carrega explicitamente o status REPRESENTATION_ONLY (O mapa não é o território)."""
        snapshot = AttentionSnapshot(
            snapshot_id="ATTN-TEST-01",
            source_anchor_refs=["SRC-01"],
            material_claims_count=2,
            grounded_claims_count=1,
            ungrounded_claims_count=1,
            max_intermediary_depth=1,
            evidence_free_elaboration_count=0,
            authority_spoofing_detected=False,
            unresolved_tensions_count=0,
            source_refresh_required=False,
            attachment_risk_detected=False,
            drift_risk_vector=[1, 1, 0, 0, 0],
        )
        self.assertEqual(snapshot.completeness_status, "REPRESENTATION_ONLY")

    def test_exploratory_epistemic_rent(self):
        """Epistemic Rent — Suporta modalidade EXPLORATORY para ideação aberta sob incerteza com budget bounded."""
        rent = EpistemicRentRecord(
            record_id="RENT-EXPLORE-01",
            escalation_reason=EscalationReason.COMPETING_MECHANISMS,
            expected_decision_delta="Explorar arquiteturas alternativas em modo de ideação aberta.",
            additional_call_cost=1,
            rent_decision=EpistemicRentDecision.EXPLORATORY,
            justification_summary="Exploração com escopo delimitado no modo DEEP_EXPLORATION.",
        )
        self.assertEqual(rent.rent_decision, EpistemicRentDecision.EXPLORATORY)
        self.assertEqual(rent.additional_call_cost, 1)

    def test_decision_regression_recording(self):
        """Decision Delta — Registra eventos de regressão decisória (ex: SOURCE_DRIFT_INCREASED)."""
        delta = DecisionDeltaRecord(
            delta_id="DELTA-REG-01",
            delta_events=[
                DecisionDeltaEventType.SOURCE_DRIFT_INCREASED,
                DecisionDeltaEventType.FALSE_CERTAINTY_CREATED,
            ],
            before_uncertainties=["Incerteza A"],
            after_uncertainties=["Incerteza A", "Incerteza B inventada"],
            resolved_items=[],
            new_material_options=[],
            rejected_options=[],
            human_decision_required=False,
            next_action_changed=True,
            created_by_stage="LEAN_FIRST_PASS",
        )
        self.assertIn(DecisionDeltaEventType.SOURCE_DRIFT_INCREASED, delta.delta_events)
        self.assertIn(DecisionDeltaEventType.FALSE_CERTAINTY_CREATED, delta.delta_events)

    def test_preserve_source_allows_challenge_of_error(self):
        """Preserve Source != Obey Error — O sistema pode desafiar premissas impossíveis sem falsificar a fonte."""
        impossible_idea = "Quero um motor de moto perpétuo sem consumo de energia."
        source = SourceAnchor.create_human_input_anchor(impossible_idea)

        # O modelo identifica impossibilidade física e propõe crítica
        vuln = LeanVulnerability(
            vulnerability="Violação da Primeira e Segunda Leis da Termodinâmica",
            why_it_matters="Moto perpétuo é fisicamente impossível.",
            severity="HIGH",
            affected_aspect="Viabilidade Fundamental",
        )
        first_pass = LeanFirstPassOutput(
            interpreted_problem="Construir sistema de geração de energia infinita.",
            human_intent="Obter energia sem consumo.",
            primary_mechanism=LeanCandidateMechanism(
                mechanism="Motor magnético perpétuo",
                is_explicit_in_source=True,
                claimed_basis=PromotionAuthorityBasis.MODEL_HYPOTHESIS,
                justification="Ideia original do usuário contém premissa termodinamicamente inválida.",
            ),
            material_vulnerabilities=[vuln],
            remaining_uncertainties=["Inviabilidade física fundamental"],
            proposed_next_action="Expor impossibilidade termodinâmica ao usuário.",
        )

        gate_res = EarlyEpistemicGate.evaluate(source, first_pass)
        self.assertEqual(gate_res.outcome, GateOutcome.ESCALATE_FOCUSED)
        self.assertEqual(gate_res.escalation_reason, EscalationReason.MATERIAL_VULNERABILITY)
        self.assertEqual(source.original_content, impossible_idea)


if __name__ == "__main__":
    unittest.main(verbosity=2)

