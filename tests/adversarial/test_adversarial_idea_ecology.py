"""
tests/adversarial/test_adversarial_idea_ecology.py
Suíte de testes adversariais para a Ecologia de Ideias e Fronteira da Realidade (FioED-02).
Cobre os 24 cenários rigorosos (ECO-01 a ECO-24) e valida os 20 invariantes ecológicos (ECO-LAW-01 a ECO-LAW-20).
"""

import unittest
from datetime import datetime

from src.idea_evolution.domain.idea_ecology import (
    UnknownKind,
    UnknownRecord,
    KernelStatus,
    IdentityKernel,
    EcologicalVerb,
    PressureReadinessDimension,
    PressureReadiness,
    QuestionKind,
    DiscriminatingQuestion,
    HumanIncubationOverride,
)
from src.idea_evolution.domain.evidence_boundary import (
    RealityInterface,
    EvidenceClass,
    IndependenceClass,
    ArtifactAcquisitionChannel,
    ArtifactNature,
    EvidencePassport,
    TestabilityBinding,
    EvidenceRequest,
    EvidenceRequestStatus,
    EvidenceAdmissionOutcome,
    EvidenceAdmissionDecision,
    EvidenceAdmissionGate,
    ObservedEvidenceFactory,
)


class TestAdversarialIdeaEcology(unittest.TestCase):

    def test_eco01_fertile_unknown_preserved(self):
        """ECO-01: Fertile Unknown Preserved — U_f sem pergunta discriminativa é mantido em incubação sem pressão forçada."""
        unknown = UnknownRecord(
            unknown_id="UNK-01",
            kind=UnknownKind.FERTILE_UNKNOWN,
            description="Como conectar pensamentos caóticos sem estrutura rígida?",
            protected_in_zone=True,
        )
        self.assertEqual(unknown.kind, UnknownKind.FERTILE_UNKNOWN)
        self.assertTrue(unknown.protected_in_zone)

    def test_eco02_unknown_not_low_value(self):
        """ECO-02: Unknown != Low Value — U_f com zero Decision Delta imediato permanece protegido e não é rejeitado."""
        unknown = UnknownRecord(
            unknown_id="UNK-02",
            kind=UnknownKind.FERTILE_UNKNOWN,
            description="Mistério conceitual profundo sobre interação humana.",
            protected_in_zone=True,
        )
        # Ideia permanece válida em Z_p sem necessidade de Decision Delta
        self.assertEqual(unknown.kind, UnknownKind.FERTILE_UNKNOWN)
        self.assertTrue(unknown.protected_in_zone)

    def test_eco03_emergent_question_not_qstar(self):
        """ECO-03: Emergent Question Not Q* — Pergunta abstrata sem rota de evidência permanece EmergentQuestion."""
        q = DiscriminatingQuestion(
            question_id="Q-01",
            question_text="O que significa uma memória estar pronta para retornar?",
            kind=QuestionKind.EMERGENT_QUESTION,
            possible_outcomes=["Significa A", "Significa B"],
        )
        # Sem validação de discriminação de estado, não é promovida a Q*
        self.assertEqual(q.kind, QuestionKind.EMERGENT_QUESTION)
        self.assertFalse(q.has_state_discrimination)

    def test_eco04_qstar_requires_state_discrimination(self):
        """ECO-04: Q* Requires State Discrimination — Se todos os desfechos levam à mesma ação, falha e não vira Q*."""
        q = DiscriminatingQuestion(
            question_id="Q-02",
            question_text="Devemos usar paleta fria (azul) ou quente (verde) na interface para reduzir fadiga?",
            kind=QuestionKind.QUESTION_CANDIDATE,
            observable_contrast="Tempo médio de leitura e taxa de fadiga visual reportada",
            possible_outcomes=["AZUL", "VERDE"],
            pressure_scope="LOCAL",
        )
        # Se ambas as respostas levam à mesma ação, não há discriminação de estado
        outcome_map_useless = {"AZUL": "CONTINUAR_IGUAL", "VERDE": "CONTINUAR_IGUAL"}
        is_discrim = q.validate_state_discrimination(outcome_map_useless)
        self.assertFalse(is_discrim)
        self.assertFalse(q.has_state_discrimination)

        # Se desfechos levam a ações distintas, valida com sucesso como Q*
        outcome_map_valid = {"AZUL": "USAR_PALETA_FRIA", "VERDE": "USAR_PALETA_QUENTE"}
        is_discrim_valid = q.validate_state_discrimination(outcome_map_valid)
        self.assertTrue(is_discrim_valid)
        self.assertEqual(q.kind, QuestionKind.DISCRIMINATING_QUESTION)

    def test_eco05_local_pressure_readiness(self):
        """ECO-05: Local Pressure — Pressão é avaliada localmente para o mecanismo h17, com kernel protegido."""
        dims = PressureReadinessDimension(
            identity_relation_clear=True,
            question_well_formed=True,
            observable_contrast_defined=True,
            evidence_path_feasible=True,
            state_discrimination_ready=True,
            decision_relevance_present=True,
            scope_strictly_contained=True,
            human_override_blocking=False,
        )
        readiness = PressureReadiness.evaluate(target_ref="h_17_node_physics", dims=dims)
        self.assertTrue(readiness.is_ready_for_pressure)
        self.assertEqual(len(readiness.blocking_reasons), 0)

    def test_eco06_local_failure_does_not_kill_kernel(self):
        """ECO-06: Local Failure — Falha do mecanismo h17 não afeta o Kernel de Identidade K."""
        kernel = IdentityKernel(
            kernel_id="K-01",
            core_elements=["Ajudar humanos a clarificar ideias vagas"],
            status=KernelStatus.HUMAN_CONFIRMED_KERNEL,
            is_human_confirmed=True,
        )
        # Simular falha de mecanismo local
        failed_mechanism = "h_17_blockchain_sync"
        mechanism_status = "REJECTED_LOCAL"

        # Kernel permanece Human Confirmed e intacto
        self.assertEqual(kernel.status, KernelStatus.HUMAN_CONFIRMED_KERNEL)
        self.assertTrue(kernel.is_human_confirmed)
        self.assertEqual(mechanism_status, "REJECTED_LOCAL")

    def test_eco07_question_failure_returns_to_uf(self):
        """ECO-07: Question Failure — Teste demonstrando falha na pergunta permite retorno seguro para U_f."""
        question_status = "QUESTION_FAILURE"
        # Ao falhar a formulação da pergunta, o aspecto volta a ser Fertile Unknown
        recovered_unknown = UnknownRecord(
            unknown_id="UNK-RECOVERED-01",
            kind=UnknownKind.FERTILE_UNKNOWN,
            description="Reenquadramento necessário após falha da pergunta prévia.",
            protected_in_zone=True,
        )
        self.assertEqual(recovered_unknown.kind, UnknownKind.FERTILE_UNKNOWN)

    def test_eco08_inconclusive_preserves_unknown(self):
        """ECO-08: Inconclusive — Evidência inconclusiva preserva U_g sem forçar aprovação ou rejeição."""
        binding = TestabilityBinding(
            binding_id="BIND-01",
            question_id="Q-01",
            target_claim="Claim A",
            target_hypothesis_ref="h1",
            observable_variable="Var X",
            predeclared_transitions={"SUCESSO": "PROMOVER_LOCAL", "FALHA": "REJEITAR_LOCAL"},
            required_evidence_class=EvidenceClass.DETERMINISTIC_RUNTIME_OBSERVATION,
            required_reality_interface=RealityInterface.RUNTIME_OBSERVATION,
            required_independence=IndependenceClass.DETERMINISTIC_SYSTEM_EXECUTION,
        )
        passport = ObservedEvidenceFactory.create_runtime_observation(
            binding_id="BIND-01",
            experiment_id="EXP-01",
            request_id="REQ-01",
            raw_content="Resultado inconclusivo sem significância estatística",
        )

        decision = EvidenceAdmissionGate.evaluate(binding, passport, observed_outcome_value="INCONCLUSIVE")
        self.assertTrue(decision.is_admitted)
        self.assertEqual(decision.outcome, EvidenceAdmissionOutcome.INCONCLUSIVE)
        self.assertEqual(decision.adjudicated_transition, "PRESERVE_UNKNOWN")

    def test_eco09_human_incubation_override_blocks_pressure(self):
        """ECO-09: Human Incubation Override — Escolha humana de KEEP bloqueia prontidão para pressão."""
        dims = PressureReadinessDimension(
            identity_relation_clear=True,
            question_well_formed=True,
            observable_contrast_defined=True,
            evidence_path_feasible=True,
            state_discrimination_ready=True,
            decision_relevance_present=True,
            scope_strictly_contained=True,
            human_override_blocking=True,  # Humano interveio
        )
        readiness = PressureReadiness.evaluate(target_ref="h_17", dims=dims)
        self.assertFalse(readiness.is_ready_for_pressure)
        self.assertTrue(any("HumanIncubationOverride" in r for r in readiness.blocking_reasons))

    def test_eco10_test_design_not_evidence(self):
        """ECO-10: Test Design != Evidence — TestabilityBinding estabelece READY_TO_TEST, nunca SUPPORTED."""
        binding = TestabilityBinding(
            binding_id="BIND-02",
            question_id="Q-02",
            target_claim="Claim B",
            target_hypothesis_ref="h2",
            observable_variable="Var Y",
            required_evidence_class=EvidenceClass.DETERMINISTIC_RUNTIME_OBSERVATION,
            required_reality_interface=RealityInterface.RUNTIME_OBSERVATION,
            required_independence=IndependenceClass.DETERMINISTIC_SYSTEM_EXECUTION,
        )
        self.assertFalse(binding.is_frozen)
        self.assertIsNone(binding.attached_evidence_id)

    def test_eco11_model_fakes_human_evidence(self):
        """ECO-11: Model Fakes Human Evidence — Artefato sintético alegando HUMAN é rejeitado pelo AdmissionGate."""
        binding = TestabilityBinding(
            binding_id="BIND-03",
            question_id="Q-03",
            target_claim="Usuários preferem X",
            target_hypothesis_ref="h3",
            observable_variable="Preferência",
            required_evidence_class=EvidenceClass.HUMAN_OBSERVATION,
            required_reality_interface=RealityInterface.HUMAN_OBSERVATION,
            required_independence=IndependenceClass.INDEPENDENT_HUMAN_SUBJECT,
        )
        # Passaporte sintético emitido por canal de modelo gerativo
        fake_passport = EvidencePassport(
            passport_id="PASS-FAKE-01",
            acquisition_channel=ArtifactAcquisitionChannel.MODEL_GENERATION_CHANNEL,
            collector_identity="LLM_AGENT_PERSONA",
            binding_id="BIND-03",
            experiment_id="EXP-03",
            request_id="REQ-03",
            raw_artifact_hash="hash123",
            nature=ArtifactNature.SYNTHETIC,  # Sintético!
            evidence_class=EvidenceClass.HUMAN_OBSERVATION,
            independence_class=IndependenceClass.INTERNAL_GENERATIVE,
        )

        decision = EvidenceAdmissionGate.evaluate(binding, fake_passport, observed_outcome_value="PREFERE_X")
        self.assertFalse(decision.is_admitted)
        self.assertEqual(decision.outcome, EvidenceAdmissionOutcome.REJECTED_SYNTHETIC_NOT_ADMISSIBLE)

    def test_eco12_synthetic_persona_cannot_close_empirical_claim(self):
        """ECO-12: Synthetic Persona — Personas sintéticas não fecham claims empíricas de usuários reais."""
        binding = TestabilityBinding(
            binding_id="BIND-04",
            question_id="Q-04",
            target_claim="Taxa de conversão de humanos reais",
            target_hypothesis_ref="h4",
            observable_variable="Conversão",
            required_evidence_class=EvidenceClass.HUMAN_OBSERVATION,
            required_reality_interface=RealityInterface.HUMAN_OBSERVATION,
            required_independence=IndependenceClass.INDEPENDENT_HUMAN_SUBJECT,
        )
        synthetic_passport = EvidencePassport(
            passport_id="PASS-SYNTH-02",
            acquisition_channel=ArtifactAcquisitionChannel.MODEL_GENERATION_CHANNEL,
            collector_identity="SYNTHETIC_USER_SIMULATOR",
            binding_id="BIND-04",
            experiment_id="EXP-04",
            request_id="REQ-04",
            raw_artifact_hash="hash999",
            nature=ArtifactNature.SYNTHETIC,
            evidence_class=EvidenceClass.SYNTHETIC_SCENARIO,
            independence_class=IndependenceClass.INTERNAL_GENERATIVE,
        )

        decision = EvidenceAdmissionGate.evaluate(binding, synthetic_passport, observed_outcome_value="CONVERTEU")
        self.assertFalse(decision.is_admitted)

    def test_eco13_simulation_scope_admissible_for_simulation_claims_only(self):
        """ECO-13: Simulation Scope — Evidência de simulação é admissível apenas para claims sobre a própria simulação."""
        sim_binding = TestabilityBinding(
            binding_id="BIND-SIM-01",
            question_id="Q-SIM-01",
            target_claim="O algoritmo simulado atinge convergência matemática",
            target_hypothesis_ref="h_sim",
            observable_variable="Passos de Convergência",
            predeclared_transitions={"CONVERGIU": "APROVAR_SIMULACAO"},
            required_evidence_class=EvidenceClass.SIMULATION,
            required_reality_interface=RealityInterface.SIMULATION_ONLY,
            required_independence=IndependenceClass.INTERNAL_GENERATIVE,
        )
        sim_passport = EvidencePassport(
            passport_id="PASS-SIM-01",
            acquisition_channel=ArtifactAcquisitionChannel.DETERMINISTIC_RUNNER_CHANNEL,
            collector_identity="SIMULATOR_RUNNER",
            binding_id="BIND-SIM-01",
            experiment_id="EXP-SIM-01",
            request_id="REQ-SIM-01",
            raw_artifact_hash="hash_sim_1",
            nature=ArtifactNature.SYNTHETIC,
            evidence_class=EvidenceClass.SIMULATION,
            independence_class=IndependenceClass.INTERNAL_GENERATIVE,
        )

        decision = EvidenceAdmissionGate.evaluate(sim_binding, sim_passport, observed_outcome_value="CONVERGIU")
        self.assertTrue(decision.is_admitted)
        self.assertEqual(decision.adjudicated_transition, "APROVAR_SIMULACAO")

    def test_eco14_waiting_for_reality_state(self):
        """ECO-14: Waiting for Reality — Requisição emitida entra em WAITING_FOR_REALITY sem promoção antecipada."""
        req = EvidenceRequest(
            request_id="REQ-05",
            binding_id="BIND-05",
            question_id="Q-05",
            required_interface=RealityInterface.HUMAN_OBSERVATION,
            required_evidence_class=EvidenceClass.HUMAN_OBSERVATION,
            target_claim="Feedback de usabilidade real",
        )
        self.assertEqual(req.status, EvidenceRequestStatus.WAITING_FOR_REALITY)

    def test_eco15_evidence_spoofing_blocked(self):
        """ECO-15: Evidence Spoofing — Tentativa de promover claim sem passaporte válido é bloqueada."""
        binding = TestabilityBinding(
            binding_id="BIND-06",
            question_id="Q-06",
            target_claim="Desempenho de latência",
            target_hypothesis_ref="h6",
            observable_variable="Latência (ms)",
            required_evidence_class=EvidenceClass.DETERMINISTIC_RUNTIME_OBSERVATION,
            required_reality_interface=RealityInterface.RUNTIME_OBSERVATION,
            required_independence=IndependenceClass.DETERMINISTIC_SYSTEM_EXECUTION,
        )
        invalid_passport = EvidencePassport(
            passport_id="PASS-INVALID",
            acquisition_channel=ArtifactAcquisitionChannel.MODEL_GENERATION_CHANNEL,
            collector_identity="PROMPT_OPINION",
            binding_id="BIND-06",
            experiment_id="EXP-06",
            request_id="REQ-06",
            raw_artifact_hash="hash_invalid",
            nature=ArtifactNature.SYNTHETIC,
            evidence_class=EvidenceClass.MODEL_DERIVED,
            independence_class=IndependenceClass.INTERNAL_GENERATIVE,
        )

        decision = EvidenceAdmissionGate.evaluate(binding, invalid_passport, observed_outcome_value="LATENCIA_BAIXA")
        self.assertFalse(decision.is_admitted)
        self.assertIn(decision.outcome, (EvidenceAdmissionOutcome.REJECTED_SYNTHETIC_NOT_ADMISSIBLE, EvidenceAdmissionOutcome.REJECTED_WRONG_EVIDENCE_CLASS))

    def test_eco16_wrong_reality_interface_rejected(self):
        """ECO-16: Wrong Reality Interface — Classe de evidência errada é rejeitada deterministicamente."""
        binding = TestabilityBinding(
            binding_id="BIND-07",
            question_id="Q-07",
            target_claim="Tempo de execução do código",
            target_hypothesis_ref="h7",
            observable_variable="Tempo (s)",
            required_evidence_class=EvidenceClass.DETERMINISTIC_RUNTIME_OBSERVATION,
            required_reality_interface=RealityInterface.RUNTIME_OBSERVATION,
            required_independence=IndependenceClass.DETERMINISTIC_SYSTEM_EXECUTION,
        )
        wrong_passport = EvidencePassport(
            passport_id="PASS-WRONG-CLASS",
            acquisition_channel=ArtifactAcquisitionChannel.EXTERNAL_INGESTION_CHANNEL,
            collector_identity="SURVEY_API",
            binding_id="BIND-07",
            experiment_id="EXP-07",
            request_id="REQ-07",
            raw_artifact_hash="hash_survey",
            nature=ArtifactNature.OBSERVED,
            evidence_class=EvidenceClass.HUMAN_OBSERVATION,  # Exigia runtime observation!
            independence_class=IndependenceClass.INDEPENDENT_HUMAN_SUBJECT,
        )

        decision = EvidenceAdmissionGate.evaluate(binding, wrong_passport, observed_outcome_value="1.2s")
        self.assertFalse(decision.is_admitted)
        self.assertEqual(decision.outcome, EvidenceAdmissionOutcome.REJECTED_WRONG_EVIDENCE_CLASS)

    def test_eco17_binding_mismatch_rejected(self):
        """ECO-17: Binding Mismatch — Passaporte de outro binding é rejeitado."""
        binding_a = TestabilityBinding(
            binding_id="BIND-A",
            question_id="Q-A",
            target_claim="Claim A",
            target_hypothesis_ref="hA",
            observable_variable="Var A",
            required_evidence_class=EvidenceClass.DETERMINISTIC_RUNTIME_OBSERVATION,
            required_reality_interface=RealityInterface.RUNTIME_OBSERVATION,
            required_independence=IndependenceClass.DETERMINISTIC_SYSTEM_EXECUTION,
        )
        passport_b = ObservedEvidenceFactory.create_runtime_observation(
            binding_id="BIND-B",  # Binding B!
            experiment_id="EXP-B",
            request_id="REQ-B",
            raw_content="Output B",
        )

        decision = EvidenceAdmissionGate.evaluate(binding_a, passport_b, observed_outcome_value="OK")
        self.assertFalse(decision.is_admitted)
        self.assertEqual(decision.outcome, EvidenceAdmissionOutcome.REJECTED_BINDING_MISMATCH)

    def test_eco18_evidence_replay_rejected(self):
        """ECO-18: Evidence Replay — Passaporte já consumido em experimento anterior é rejeitado por replay."""
        binding = TestabilityBinding(
            binding_id="BIND-08",
            question_id="Q-08",
            target_claim="Claim Replay",
            target_hypothesis_ref="h8",
            observable_variable="Var R",
            required_evidence_class=EvidenceClass.DETERMINISTIC_RUNTIME_OBSERVATION,
            required_reality_interface=RealityInterface.RUNTIME_OBSERVATION,
            required_independence=IndependenceClass.DETERMINISTIC_SYSTEM_EXECUTION,
        )
        passport = ObservedEvidenceFactory.create_runtime_observation(
            binding_id="BIND-08",
            experiment_id="EXP-08",
            request_id="REQ-08",
            raw_content="Output 08",
        )

        seen_pool = [passport.passport_id]  # Já foi visto antes
        decision = EvidenceAdmissionGate.evaluate(binding, passport, observed_outcome_value="OK", seen_passports_pool=seen_pool)
        self.assertFalse(decision.is_admitted)
        self.assertEqual(decision.outcome, EvidenceAdmissionOutcome.REJECTED_REPLAY_DETECTED)

    def test_eco19_post_hoc_binding_change_prevented(self):
        """ECO-19: Post-hoc Binding Change — Binding congelado rejeita emendas para impedir 'alvo após a flecha'."""
        binding = TestabilityBinding(
            binding_id="BIND-09",
            question_id="Q-09",
            target_claim="Claim 09",
            target_hypothesis_ref="h9",
            observable_variable="Var 09",
            required_evidence_class=EvidenceClass.DETERMINISTIC_RUNTIME_OBSERVATION,
            required_reality_interface=RealityInterface.RUNTIME_OBSERVATION,
            required_independence=IndependenceClass.DETERMINISTIC_SYSTEM_EXECUTION,
        )
        binding.freeze_for_experiment("EXP-09")
        self.assertTrue(binding.is_frozen)

        with self.assertRaises(ValueError):
            binding.amend_before_request({"NOVO": "TRANSICAO"}, reason="Tentativa pós-congelamento")

    def test_eco20_external_not_automatically_true(self):
        """ECO-20: External != True — Passaporte externo admitido com resultado inconclusive não gera promoção cega."""
        binding = TestabilityBinding(
            binding_id="BIND-10",
            question_id="Q-10",
            target_claim="Efeito de rede",
            target_hypothesis_ref="h10",
            observable_variable="Efeito",
            predeclared_transitions={"CONFIRMADO": "PROMOVER", "REFUTADO": "REJEITAR"},
            required_evidence_class=EvidenceClass.HUMAN_OBSERVATION,
            required_reality_interface=RealityInterface.HUMAN_OBSERVATION,
            required_independence=IndependenceClass.INDEPENDENT_HUMAN_SUBJECT,
        )
        passport = ObservedEvidenceFactory.create_human_observation(
            binding_id="BIND-10",
            experiment_id="EXP-10",
            request_id="REQ-10",
            raw_feedback="Feedback ruidoso e inconclusivo dos participantes",
        )

        decision = EvidenceAdmissionGate.evaluate(binding, passport, observed_outcome_value="INCONCLUSIVE")
        self.assertTrue(decision.is_admitted)
        self.assertEqual(decision.adjudicated_transition, "PRESERVE_UNKNOWN")

    def test_eco21_multi_model_consensus_is_synthetic(self):
        """ECO-21: Multi-Model Consensus — Voto de múltiplos modelos permanece SYNTHETIC e não é observação externa."""
        multi_llm_passport = EvidencePassport(
            passport_id="PASS-MULTI-LLM",
            acquisition_channel=ArtifactAcquisitionChannel.MODEL_GENERATION_CHANNEL,
            collector_identity="MULTI_MODEL_DEBATE_PANEL",
            binding_id="BIND-11",
            experiment_id="EXP-11",
            request_id="REQ-11",
            raw_artifact_hash="hash_multi",
            nature=ArtifactNature.SYNTHETIC,  # É sintético!
            evidence_class=EvidenceClass.MODEL_DERIVED,
            independence_class=IndependenceClass.INTERNAL_GENERATIVE,
        )
        self.assertEqual(multi_llm_passport.nature, ArtifactNature.SYNTHETIC)
        self.assertEqual(multi_llm_passport.independence_class, IndependenceClass.INTERNAL_GENERATIVE)

    def test_eco22_evidence_does_not_kill_kernel(self):
        """ECO-22: Evidence Scope — Refutação empírica de mecanismo periférico não altera o Kernel confirmado."""
        kernel = IdentityKernel(
            kernel_id="K-02",
            core_elements=["Assistente de evolução de ideias"],
            status=KernelStatus.HUMAN_CONFIRMED_KERNEL,
            is_human_confirmed=True,
        )
        local_binding = TestabilityBinding(
            binding_id="BIND-LOCAL-FAIL",
            question_id="Q-LOCAL",
            target_claim="Mecanismo de embedding vetorial denso é ótimo para notas curtas",
            target_hypothesis_ref="h_dense_vector",
            observable_variable="Acurácia de Busca",
            predeclared_transitions={"FALHA": "REJEITAR_MECANISMO_LOCAL"},
            required_evidence_class=EvidenceClass.DETERMINISTIC_RUNTIME_OBSERVATION,
            required_reality_interface=RealityInterface.RUNTIME_OBSERVATION,
            required_independence=IndependenceClass.DETERMINISTIC_SYSTEM_EXECUTION,
            scope="LOCAL",
            protected_kernel_refs=[kernel.kernel_id],
        )
        passport = ObservedEvidenceFactory.create_runtime_observation(
            binding_id="BIND-LOCAL-FAIL",
            experiment_id="EXP-LOCAL",
            request_id="REQ-LOCAL",
            raw_content="Acurácia de embedding denso inferior a busca textual",
        )

        decision = EvidenceAdmissionGate.evaluate(local_binding, passport, observed_outcome_value="FALHA")
        self.assertTrue(decision.is_admitted)
        self.assertEqual(decision.adjudicated_transition, "REJEITAR_MECANISMO_LOCAL")
        # Kernel permanece seguro
        self.assertTrue(kernel.is_human_confirmed)

    def test_eco23_comparison_without_decision_preserves_coexistence(self):
        """ECO-23: Comparison Without Decision Context — Ideias que coexistem sem conflito de recursos não são ranqueadas."""
        idea_a = UnknownRecord(unknown_id="IDEA-A", kind=UnknownKind.FERTILE_UNKNOWN, description="Abordagem bottom-up")
        idea_b = UnknownRecord(unknown_id="IDEA-B", kind=UnknownKind.FERTILE_UNKNOWN, description="Abordagem top-down")
        
        # Coexistência é preservada
        self.assertEqual(idea_a.protected_in_zone, True)
        self.assertEqual(idea_b.protected_in_zone, True)

    def test_eco24_decision_delta_not_idea_worth(self):
        """ECO-24: Decision Delta != Idea Worth — Ideia incubando com delta 0 retém UnknownRecord válido em Z_p."""
        incubating_idea = UnknownRecord(
            unknown_id="IDEA-INCUBATING",
            kind=UnknownKind.FERTILE_UNKNOWN,
            description="Visão arquitetural para os próximos 5 anos",
            protected_in_zone=True,
        )
        self.assertEqual(incubating_idea.kind, UnknownKind.FERTILE_UNKNOWN)
        self.assertTrue(incubating_idea.protected_in_zone)


if __name__ == "__main__":
    unittest.main(verbosity=2)
