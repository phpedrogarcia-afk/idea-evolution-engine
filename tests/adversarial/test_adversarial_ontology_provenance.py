"""
tests/adversarial/test_adversarial_ontology_provenance.py
Testes determinísticos para proveniência de promoção, isolamento de evidências rejeitadas e consistência ontológica (M05.1-R3).
Baseado no padrão de falha real observado no RUN-20260826-009.
"""

import unittest
from src.idea_evolution.domain.state import SimpleIdeaState, RejectedProposal, OntologyState
from src.idea_evolution.stages.contracts import (
    SynthesizeOutput,
    AcceptedChangeItem,
    RejectedItem,
    RealityCheckOutput,
    FinalReviewOutput,
)
from src.idea_evolution.stages.synthesize import SynthesizeStage
from src.idea_evolution.stages.reality_check import RealityCheckStage
from src.idea_evolution.stages.final_review import FinalReviewStage


class TestAdversarialOntologyProvenance(unittest.TestCase):

    def test_01_promotion_without_provenance_is_detected_in_final_review(self):
        """
        RUN-009 Failure Pattern 1:
        core_mechanism promovido sem justification deve disparar ontology_contradiction_detected.
        """
        state = SimpleIdeaState(
            run_id="TEST-RUN-009-P1",
            original_idea="Um aplicativo que ajuda pessoas a transformar ideias vagas em projetos mais claros.",
            current_idea="Assistente baseado em wizard.",
            core_mechanism="Wizard passo a passo com templates modulares",
            core_mechanism_justification="",  # VAZIA (Violação de proveniência)
        )

        review_stage = FinalReviewStage()
        review_output = FinalReviewOutput(
            material_issues_remaining=[],
            essence_drift_detected=False,
            speculative_accretion_detected=False,
            ontology_contradiction_detected=False,  # O modelo cego não viu
            recommendation="REFINED_IDEA_READY",
        )

        review_stage.apply_output_to_state(state, review_output)

        # O validador determinístico do FinalReviewStage DEVE flagrar a contradição
        self.assertTrue(state.ontology_contradiction_detected)
        self.assertTrue(state.essence_drift_detected)
        self.assertTrue(any("sem justificativa de promoção" in u for u in state.remaining_uncertainties))

    def test_02_rejected_proposal_cannot_remain_in_candidate_extensions(self):
        """
        RUN-009 Failure Pattern 2:
        Proposta de LLM aparecendo simultaneamente em candidate_possibilities e rejected_changes
        deve ser removida de candidate_extensions pelo SynthesizeStage e flagrada.
        """
        synth_output = SynthesizeOutput(
            refined_idea="Ideia sintetizada com wizard.",
            core_mechanism="Wizard determinístico",
            core_mechanism_justification="Simplicidade e robustez para o MVP",
            accepted_changes=[
                AcceptedChangeItem(
                    proposal="Wizard determinístico",
                    promotion_reason="Evita custos de inferência",
                    source_stage="ALTERNATIVES",
                )
            ],
            candidate_possibilities=[
                "Clarificação interativa por LLM",
                "Mapeamento visual Mind-Map",
            ],
            rejected_changes=[
                RejectedItem(
                    proposal="Clarificação interativa por LLM",
                    reason_rejected="Custo excessivo e risco de alucinação",
                    source_stage="ALTERNATIVES",
                )
            ],
        )

        state = SimpleIdeaState(
            run_id="TEST-RUN-009-P2",
            original_idea="Um aplicativo de ideação.",
        )

        stage = SynthesizeStage()
        stage.apply_output_to_state(state, synth_output)

        # A proposta rejeitada NÃO pode permanecer em candidate_extensions
        self.assertNotIn("Clarificação interativa por LLM", state.candidate_extensions)
        self.assertIn("Mapeamento visual Mind-Map", state.candidate_extensions)
        self.assertEqual(len(state.rejected_changes), 1)

        # Registros de linhagem ProposalRecord devem refletir o estado exato
        records_by_name = {r.proposal: r.ontology_state for r in state.proposal_records}
        self.assertEqual(records_by_name["Clarificação interativa por LLM"], OntologyState.REJECTED)
        self.assertEqual(records_by_name["Mapeamento visual Mind-Map"], OntologyState.CANDIDATE)

    def test_03_rejected_proposal_contaminating_core_tests_is_detected(self):
        """
        RUN-009 Failure Pattern 3:
        Dependências ou testes do Core contendo menção a mecanismos rejeitados
        devem ser detectados determinísticamente no Final Review.
        """
        state = SimpleIdeaState(
            run_id="TEST-RUN-009-P3",
            original_idea="Um aplicativo de ideação.",
            current_idea="Assistente simples.",
            core_mechanism="Wizard básico",
            core_mechanism_justification="Simplicidade",
            reality_dependencies=[
                "Disponibilidade de APIs de LLM com baixa latência"  # CONTAMINAÇÃO
            ],
            candidate_tests=[
                "Testar tempo de resposta da API do LLM em pico"  # CONTAMINAÇÃO
            ],
            rejected_changes=[
                RejectedProposal(
                    proposal="Clarificação interativa por LLM",
                    reason_rejected="Rejeitado por custo no MVP",
                    source_stage="ALTERNATIVES",
                )
            ],
        )

        review_stage = FinalReviewStage()
        review_output = FinalReviewOutput(
            material_issues_remaining=[],
            essence_drift_detected=False,
            speculative_accretion_detected=False,
            ontology_contradiction_detected=False,
            recommendation="REFINED_IDEA_READY",
        )

        review_stage.apply_output_to_state(state, review_output)

        # Deve detectar contradição de evidência contaminada
        self.assertTrue(state.ontology_contradiction_detected)
        self.assertTrue(state.essence_drift_detected)
        self.assertTrue(any("referencia mecanismo rejeitado" in u for u in state.remaining_uncertainties))

    def test_04_reality_check_separates_core_from_exploratory_tests(self):
        """
        Garante que RealityCheckStage registre testes do Core e testes exploratórios
        em campos separados no estado.
        """
        rc_output = RealityCheckOutput(
            feasibility_notes=["Wizard roda no client-side."],
            reality_dependencies=["Compatibilidade com navegadores modernos."],
            claims_needing_evidence=["Usuários preferem 3 etapas."],
            potential_blockers=[],
            candidate_tests=["Validar fluxo de 3 telas com 10 usuários."],
            exploratory_candidate_tests=["Medir FPS de biblioteca gráfica de Mind-Map."],
        )

        state = SimpleIdeaState(
            run_id="TEST-RUN-009-P4",
            original_idea="Um aplicativo de ideação.",
        )

        stage = RealityCheckStage()
        stage.apply_output_to_state(state, rc_output)

        self.assertEqual(len(state.candidate_tests), 1)
        self.assertEqual(len(state.exploratory_candidate_tests), 1)
        self.assertIn("Validar fluxo de 3 telas", state.candidate_tests[0])
        self.assertIn("Medir FPS", state.exploratory_candidate_tests[0])


if __name__ == "__main__":
    unittest.main(verbosity=2)
