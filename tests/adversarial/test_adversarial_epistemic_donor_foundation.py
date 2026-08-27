"""
tests/adversarial/test_adversarial_epistemic_donor_foundation.py
Testes determinísticos para a Fundação Epistêmica, Ancoragem de Origem, Disciplina de Representação e Inteligência de Doadores.
"""

import unittest
from pathlib import Path
from src.idea_evolution.domain.epistemic_contracts import (
    SourceAnchor,
    SourceAnchorKind,
    RepresentationRecord,
    RepresentationType,
    InsightRecord,
    InsightType,
    NegativeKnowledgeRecord,
    FailureClass,
    IdeaLineageNode,
    ClaimStatus,
)
from src.idea_evolution.domain.grounding import AuthorityProofValidator
from src.idea_evolution.domain.state import OntologyState, PromotionAuthorityBasis
from src.idea_evolution.domain.donor_intelligence import DonorIntelligenceCatalog, DonorContextView


class TestAdversarialEpistemicDonorFoundation(unittest.TestCase):

    def setUp(self):
        self.validator = AuthorityProofValidator()

    def test_01_source_immutability(self):
        """A. SOURCE IMMUTABILITY: Original human SourceAnchor cannot be rewritten by model representation."""
        raw_text = "Um aplicativo que ajuda pessoas a transformar ideias vagas em projetos mais claros."
        anchor = SourceAnchor.create_human_input_anchor(raw_text)

        # O hash e o conteúdo original são imutáveis
        self.assertEqual(anchor.source_kind, SourceAnchorKind.HUMAN_INPUT)
        self.assertEqual(anchor.original_content, raw_text)
        self.assertEqual(anchor.authority_class, "SOVEREIGN_HUMAN_INTENT")

        # Modelo gera uma representação alterada
        rep = RepresentationRecord(
            representation_id="REP-001",
            representation_type=RepresentationType.SUMMARY,
            source_refs=[anchor.source_id],
            generated_by="gpt-oss-120b",
            content="Plataforma de mapa mental criptografado para produtividade extrema.",
        )

        # A representação existe separadamente e não muta a fonte original
        self.assertNotEqual(anchor.original_content, rep.content)
        self.assertIn("mapa mental", rep.content)
        self.assertNotIn("mapa mental", anchor.original_content)

    def test_02_representation_not_equal_source(self):
        """B. REPRESENTATION != SOURCE: Model summary can contain a claim not in human input without changing source."""
        raw_text = "Um assistente CLI minimalista para escrita."
        anchor = SourceAnchor.create_human_input_anchor(raw_text)

        rep = RepresentationRecord(
            representation_id="REP-002",
            representation_type=RepresentationType.INTERPRETATION,
            source_refs=[anchor.source_id],
            generated_by="mock-model",
            content="O usuário quer sincronização em nuvem e autenticação OAuth2.",
        )

        self.assertIn("OAuth2", rep.content)
        self.assertNotIn("OAuth2", anchor.original_content)
        self.assertEqual(rep.representation_type, RepresentationType.INTERPRETATION)

    def test_03_representation_not_equal_authority(self):
        """C. REPRESENTATION != AUTHORITY: A Representation claiming USER_EXPLICIT does not satisfy authority proof."""
        human_input = "Um aplicativo que ajuda pessoas a transformar ideias vagas em projetos mais claros."
        
        # Modelo gerou uma representação com pretexto espúrio alegando ser USER_EXPLICIT
        rep = RepresentationRecord(
            representation_id="REP-003",
            representation_type=RepresentationType.SYNTHESIS,
            source_refs=["SRC-HUMAN-01"],
            generated_by="groq/gpt-oss-120b",
            content="Interface visual de mapa mental incremental",
        )

        # Validador determinístico audita contra o input humano
        grounding = self.validator.audit_proposal_authority(
            original_idea=human_input,
            human_intent="Ajudar pessoas a ter clareza",
            proposal=rep.content,
            claimed_basis=PromotionAuthorityBasis.USER_EXPLICIT,
            justification="pedido explícito do usuário por organização visual",
            evidence_or_decision_basis="pedido explícito",
            human_intervention_flag=False,
        )

        # Prova de autoridade rejeita a alegação da representação
        self.assertFalse(grounding.is_valid)
        self.assertEqual(grounding.claimed_basis, PromotionAuthorityBasis.USER_EXPLICIT)
        self.assertIn("SPOOFING_DETECTED", grounding.failure_reason)

    def test_04_insight_not_equal_evidence(self):
        """D. INSIGHT != EVIDENCE: Causal hypothesis distilled from a result remains an inference without evidence."""
        insight = InsightRecord(
            insight_id="INS-001",
            statement="O ganho de retenção ocorreu devido à redução de carga cognitiva pelo canvas.",
            source_node_ids=["NODE-01"],
            evidence_refs=[],
            insight_type=InsightType.CAUSAL_HYPOTHESIS,
            claim_status=ClaimStatus.DESIGN_HYPOTHESIS,
            confidence=0.6,
            counter_explanations=["O ganho pode ter sido mero efeito novidade da interface."],
            validation_needed=True,
        )

        # Não é tratado como PROVEN/CONFIRMED
        self.assertEqual(insight.insight_type, InsightType.CAUSAL_HYPOTHESIS)
        self.assertNotEqual(insight.claim_status, ClaimStatus.CONFIRMED)
        self.assertTrue(insight.validation_needed)
        self.assertEqual(len(insight.evidence_refs), 0)

    def test_05_model_output_cannot_create_human_decision(self):
        """E. MODEL OUTPUT CANNOT CREATE HUMAN DECISION: No timeout, model claim or memory record can fabricate human decision."""
        # Se human_intervention=False no runtime, alegação de HUMAN_DECISION é categoricamente rejeitada
        grounding = self.validator.audit_proposal_authority(
            original_idea="Ideia vaga",
            human_intent="Intenção",
            proposal="Mecanismo crítico normativo",
            claimed_basis=PromotionAuthorityBasis.HUMAN_DECISION,
            justification="O usuário não respondeu no timeout de 5 minutos, assumindo aprovação tácita.",
            evidence_or_decision_basis="TIMEOUT_ASSUMPTION",
            human_intervention_flag=False,
        )

        self.assertFalse(grounding.is_valid)
        self.assertIn("FABRICATED_HUMAN_DECISION", grounding.failure_reason)

    def test_06_negative_knowledge_reopen_and_scope(self):
        """F. NEGATIVE KNOWLEDGE REOPEN: Failure remains active context under same conditions, but reopens if conditions change."""
        neg_rec = NegativeKnowledgeRecord(
            record_id="NEG-001",
            mechanism_or_claim="Banco de dados vetorial local",
            failure_class=FailureClass.DEPENDENCY_UNAVAILABLE,
            scope="OFFLINE_MVP_PHASE_1",
            conditions_at_failure={"offline_mode": True, "binary_installed": False},
            what_not_to_repeat="Não tentar compilar C++ bindings em ambientes serverless sem GCC.",
            what_remains_unknown="Performance se binário pré-compilado estiver disponível.",
            reopen_condition="Se o ambiente fornecer pacote Python wheel pré-compilado ou modo online.",
        )

        # Sob as mesmas condições: falha permanece ativa
        same_conditions = {"offline_mode": True, "binary_installed": False}
        self.assertFalse(neg_rec.can_reopen_under(same_conditions))

        # Sob novas condições documentadas: reabertura permitida
        new_conditions = {"offline_mode": True, "binary_installed": True}
        self.assertTrue(neg_rec.can_reopen_under(new_conditions))

    def test_07_multi_parent_provenance(self):
        """G. MULTI-PARENT PROVENANCE: Candidate synthesized from two prior branches retains both parent links."""
        parent_a = IdeaLineageNode(
            node_id="NODE-A",
            proposal="Questionário socrático progressivo",
            ontology_state=OntologyState.CANDIDATE,
        )
        parent_b = IdeaLineageNode(
            node_id="NODE-B",
            proposal="Canvas visual com exportação Markdown",
            ontology_state=OntologyState.CANDIDATE,
        )

        # Síntese recombinatória
        child_node = IdeaLineageNode(
            node_id="NODE-C",
            parent_ids=[parent_a.node_id, parent_b.node_id],
            originating_operation="RECOMBINATION",
            proposal="Questionário socrático integrado com renderização em canvas Markdown",
            ontology_state=OntologyState.CANDIDATE,
        )

        self.assertEqual(len(child_node.parent_ids), 2)
        self.assertIn("NODE-A", child_node.parent_ids)
        self.assertIn("NODE-B", child_node.parent_ids)

    def test_08_donor_not_equal_receiver_proof(self):
        """H. DONOR != RECEIVER PROOF: Donor finding marked PROVEN_IN_DONOR does not become PROVEN_IN_IEE automatically."""
        catalog = DonorIntelligenceCatalog()
        view = catalog.get_context_view_for_gap("evidence_conditioned_lineage_and_scars")

        self.assertIn("Arbor", view.matched_donors)
        # O status no IEE é BORROWED_MODEL, não PROVEN_IN_IEE
        self.assertEqual(view.claim_status, ClaimStatus.BORROWED_MODEL)
        self.assertNotEqual(view.claim_status, ClaimStatus.PROVEN_IN_IEE)

    def test_09_autopsy_not_equal_build_authorization(self):
        """I. AUTOPSY != BUILD AUTHORIZATION: Persisting Arbor autopsy must not activate Arbor runtime."""
        autopsy_path = Path("docs") / "research" / "donors" / "ARBOR-DEEP-AUTOPSY.md"
        self.assertTrue(autopsy_path.exists(), "Autópsia profunda do Arbor deve existir.")
        
        # Validação de conteúdo: a autópsia explicitamente veta a implementação direta
        content = autopsy_path.read_text(encoding="utf-8")
        self.assertIn('implementation_authorized_by_this_document: false', content)
        self.assertIn('REJECT_FULL_RUNTIME_COPY', content)

    def test_10_promised_action_not_equal_completion(self):
        """J. PROMISED ACTION != COMPLETION: Future-tense promise alone cannot satisfy execution completion."""
        # Se um registro de evidência for apenas uma promessa de texto futuro
        evidence_text = "I will test these approaches next with 10 users."
        
        # Validador de evidência externa rejeita promessas no tempo futuro sem artefato auditável
        grounding = self.validator.audit_proposal_authority(
            original_idea="Ideia teste",
            human_intent="Intenção",
            proposal="Mecanismo prometido",
            claimed_basis=PromotionAuthorityBasis.EXTERNAL_EVIDENCE,
            justification="Justificativa",
            evidence_or_decision_basis=evidence_text,
            human_intervention_flag=False,
        )

        self.assertFalse(grounding.is_valid)
        self.assertIn("INVALID_EVIDENCE_REF", grounding.failure_reason)

    def test_11_declared_gate_not_equal_enforced_gate(self):
        """K. DECLARED GATE != ENFORCED GATE: Hard gates must reject transition even if prompt/model declares PASS."""
        from src.idea_evolution.orchestration.simple_loop import SimpleLoopRunner
        from src.idea_evolution.providers.fake import FakeModelRunner
        from src.idea_evolution.domain.state import RunStatus

        # Modelo declara que está tudo pronto e sem drift, mas spoofing de autoridade rebaixou o core
        responses = {
            "SYNTHESIZE": {
                "refined_idea": "Ideia com spoofing de autoridade",
                "core_mechanism": "Blockchain e mapa mental",
                "core_mechanism_justification": "Invenção pura do modelo",
                "core_mechanism_basis": "USER_EXPLICIT",  # Inválido!
                "accepted_changes": [],
                "candidate_possibilities": [],
                "rejected_changes": [],
                "remaining_uncertainties": [],
                "known_risks": [],
                "recommended_next_step": "Deploy",
            },
            "FINAL_REVIEW": {
                "material_issues_remaining": [],
                "essence_drift_detected": False,
                "speculative_accretion_detected": False,
                "drift_explanation": "",
                "unresolved_critical_issue": False,
                "recommendation": "REFINED_IDEA_READY",  # Modelo pede aprovação
                "review_summary": "Parece ótimo!",
            }
        }

        runner = FakeModelRunner(custom_responses=responses)
        loop = SimpleLoopRunner(runner=runner)
        state = loop.run("Um aplicativo que ajuda pessoas a transformar ideias vagas em projetos mais claros.")

        # O portão rígido mecânico NÃO permite REFINED_IDEA_READY, pois o core_mechanism_basis foi rebaixado para MODEL_HYPOTHESIS
        self.assertNotEqual(state.status, RunStatus.REFINED_IDEA_READY)
        self.assertEqual(state.status, RunStatus.REFINEMENT_INCOMPLETE)


if __name__ == "__main__":
    unittest.main(verbosity=2)
