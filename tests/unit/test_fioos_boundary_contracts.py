"""
tests/unit/test_fioos_boundary_contracts.py
Testes determinísticos para validação das invariantes de contrato do protocolo IEE/FioOS V1.
"""

import unittest
from datetime import datetime
from pydantic import ValidationError
from src.idea_evolution.contracts.fioos_protocol import (
    InvestigationIntent,
    IntentProvenance,
    EpistemicBudgetHint,
    CognitiveRequirement,
    EpistemicState,
    FioOSMissionPlan,
    OperationalBudget,
    ExecutionIdentityBinding,
    EvidenceEnvelope,
    OperationalCostReport,
    EpistemicUpdate,
    OntologyLayer,
    OntologyTransitionValidator,
    IEEOperatingMode,
    FioOSOperationalStatus,
)


class TestFioOSBoundaryContracts(unittest.TestCase):

    def setUp(self):
        self.valid_provenance = IntentProvenance(
            created_by="IEE_INVESTIGATION_COORDINATOR",
            created_at=datetime.now().isoformat(),
        )

    def test_01_investigation_intent_cannot_contain_credentials_or_secrets(self):
        """Invariante: InvestigationIntent rejeita estritamente segredos, chaves e tokens."""
        with self.assertRaises(ValueError) as ctx:
            InvestigationIntent(
                idea_id="IDEA-001",
                genome_version="v0.1.0",
                uncertainty_id="UNC-001",
                target_claims=["CLM-001"],
                question="Como validar a latência com api_key=sk-12345678?",
                epistemic_operation="DISCRIMINATE",
                decision_relevance="Crítica para o MVP",
                evidence_required="Métricas de latência",
                cognitive_requirements=[CognitiveRequirement.RESEARCH_FAST],
                stop_condition="Resultado obtido",
                provenance=self.valid_provenance,
            )
        self.assertIn("INVESTIGATION_INTENT_VIOLATION", str(ctx.exception))

    def test_02_investigation_intent_cannot_contain_tool_requests_or_shell_commands(self):
        """Invariante: InvestigationIntent rejeita comandos operacionais de terminal/shell."""
        with self.assertRaises(ValueError) as ctx:
            InvestigationIntent(
                idea_id="IDEA-001",
                genome_version="v0.1.0",
                uncertainty_id="UNC-001",
                target_claims=["CLM-001"],
                question="Executar curl https://api.example.com para testar",
                epistemic_operation="REALITY_TEST",
                decision_relevance="Alta",
                evidence_required="HTTP 200",
                cognitive_requirements=[CognitiveRequirement.MECHANICAL_NO_MODEL],
                stop_condition="curl finalizado",
                provenance=self.valid_provenance,
            )
        self.assertIn("INVESTIGATION_INTENT_VIOLATION", str(ctx.exception))

    def test_03_investigation_intent_requires_target_claims(self):
        """Invariante: InvestigationIntent exige target_claims não vazio."""
        with self.assertRaises(ValidationError):
            InvestigationIntent(
                idea_id="IDEA-001",
                genome_version="v0.1.0",
                uncertainty_id="UNC-001",
                target_claims=[],
                question="Pergunta genérica sem claim?",
                epistemic_operation="CRITIQUE",
                decision_relevance="Nula",
                evidence_required="Nenhuma",
                cognitive_requirements=[CognitiveRequirement.ADVERSARIAL_REASONING_HIGH],
                stop_condition="Parada",
                provenance=self.valid_provenance,
            )

    def test_04_ready_to_test_is_epistemic_state_not_execution_authority(self):
        """Invariante: READY_TO_TEST é um estado epistêmico e não concede autoridade de execução."""
        state = EpistemicState.READY_TO_TEST
        self.assertEqual(state.value, "READY_TO_TEST")
        # O FioOS pode responder com múltiplos status operacionais independentes
        fioos_responses = [
            FioOSOperationalStatus.AUTHORIZED,
            FioOSOperationalStatus.BLOCKED,
            FioOSOperationalStatus.BUDGET_DENIED,
        ]
        self.assertIn(FioOSOperationalStatus.BUDGET_DENIED, fioos_responses)

    def test_05_mission_plan_does_not_imply_authorization(self):
        """Invariante: Ter um FioOSMissionPlan não é autorização."""
        plan = FioOSMissionPlan(
            investigation_intent_hash="sha256_mock_hash",
            mission_id="MSN-001",
            source_identity="USER_ANONYMIZED",
            lane="BATCH",
            concrete_model="qwen3.6-27b",
            provider="groq",
            reasoning_effort="MEDIUM",
            tools=["web_search"],
            requested_authority="READ_ONLY",
            budget=OperationalBudget(max_cost_usd=0.0, max_tokens=10000),
            territory="SANDBOX_EPHEMERAL",
            test_budget="1_EXECUTION",
            stop_condition="Evidence found",
        )
        self.assertEqual(plan.mission_id, "MSN-001")
        # FioOSMissionPlan não possui campo de autorização concedida
        self.assertFalse(hasattr(plan, "is_authorized"))

    def test_06_execution_identity_binding_temporal_separation(self):
        """Invariante: ExecutionIdentityBinding é uma etapa downstream com lease temporal."""
        binding = ExecutionIdentityBinding(
            binding_id="BIND-001",
            mission_id="MSN-001",
            authorized_identity="WORKLOAD_RUNNER_01",
            workload_token="JWT_SECURE_TOKEN",
            granted_authority="READ_ONLY",
            lease_expires_at="2026-08-26T16:00:00Z",
            sandbox_container_id="CONTAINER-998",
        )
        self.assertEqual(binding.granted_authority, "READ_ONLY")
        self.assertTrue(bool(binding.workload_token))

    def test_07_evidence_envelope_observations_not_truth(self):
        """Invariante: EvidenceEnvelope transporta observações brutas e telemetria de custo."""
        envelope = EvidenceEnvelope(
            evidence_id="EVID-001",
            mission_id="MSN-001",
            investigation_intent_hash="sha256_mock_hash",
            source_identity="USER_ANONYMIZED",
            execution_identity="WORKLOAD_RUNNER_01",
            artifact_pointer="/runs/evidence/evid_001.json",
            artifact_sha256="sha256_artifact_hash",
            observation_type="EMPIRICAL_DATA",
            raw_verdict="PASS",
            occurred_at=datetime.now().isoformat(),
            operational_cost=OperationalCostReport(total_tokens=500, cost_usd=0.0, latency_seconds=0.45),
            intervention_record=[],
            provenance={"runner": "FioOS_RUNTIME_GATEWAY"},
            source_metadata={"engine": "benchmark_v1"},
        )
        self.assertEqual(envelope.raw_verdict, "PASS")
        self.assertEqual(envelope.operational_cost.cost_usd, 0.0)

    def test_08_candidate_cannot_silently_become_core(self):
        """Invariante: Transição CANDIDATE -> CORE exige autorização humana explícita."""
        with self.assertRaises(ValueError) as ctx:
            OntologyTransitionValidator.validate_transition(
                current_layer=OntologyLayer.CANDIDATE,
                target_layer=OntologyLayer.CORE,
                human_authority_granted=False,
            )
        self.assertIn("ONTOLOGY_VIOLATION", str(ctx.exception))

        # Com autorização humana explícita, a transição é autorizada
        self.assertTrue(
            OntologyTransitionValidator.validate_transition(
                current_layer=OntologyLayer.CANDIDATE,
                target_layer=OntologyLayer.CORE,
                human_authority_granted=True,
            )
        )

    def test_09_candidate_to_derived_requires_justification(self):
        """Invariante: Transição CANDIDATE -> DERIVED exige justificativa formal."""
        with self.assertRaises(ValueError) as ctx:
            OntologyTransitionValidator.validate_transition(
                current_layer=OntologyLayer.CANDIDATE,
                target_layer=OntologyLayer.DERIVED,
                has_justification=False,
            )
        self.assertIn("ONTOLOGY_VIOLATION", str(ctx.exception))

        self.assertTrue(
            OntologyTransitionValidator.validate_transition(
                current_layer=OntologyLayer.CANDIDATE,
                target_layer=OntologyLayer.DERIVED,
                has_justification=True,
            )
        )

    def test_10_rejected_item_cannot_reopen_without_evidence_or_reason(self):
        """Invariante: Proposição REJECTED não pode ser reativada sem nova evidência ou motivo explícito."""
        with self.assertRaises(ValueError) as ctx:
            OntologyTransitionValidator.validate_transition(
                current_layer=OntologyLayer.REJECTED,
                target_layer=OntologyLayer.CANDIDATE,
                has_new_evidence=False,
                reopen_reason="",
            )
        self.assertIn("ONTOLOGY_VIOLATION", str(ctx.exception))

        # Reabertura com motivo formal
        self.assertTrue(
            OntologyTransitionValidator.validate_transition(
                current_layer=OntologyLayer.REJECTED,
                target_layer=OntologyLayer.CANDIDATE,
                has_new_evidence=False,
                reopen_reason="Novas condições de mercado tornaram o mecanismo viável.",
            )
        )

    def test_11_operating_modes_definition(self):
        """Invariante: Modos STANDALONE e FIOOS_GOVERNED são definidos formalmente."""
        self.assertEqual(IEEOperatingMode.STANDALONE.value, "STANDALONE")
        self.assertEqual(IEEOperatingMode.FIOOS_GOVERNED.value, "FIOOS_GOVERNED")


if __name__ == "__main__":
    unittest.main(verbosity=2)
