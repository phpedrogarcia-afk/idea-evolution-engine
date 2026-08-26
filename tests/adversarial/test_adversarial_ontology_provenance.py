"""
tests/adversarial/test_adversarial_ontology_provenance.py
Testes determinísticos para proveniência de promoção, autoridade não circular, alinhamento pós-síntese de realidade, identidade imutável de Run ID e validação estrita de autoridade / gates finais (M05.1-R3 / M05.1-R4 / M05.1-R5).
Baseado nos padrões de falha reais observados nas execuções em Cloud Shell (RUN-009 e RUN-20260826_202600-6639861f).
"""

import unittest
import tempfile
import time
from pathlib import Path
from src.idea_evolution.domain.state import (
    SimpleIdeaState,
    RejectedProposal,
    OntologyState,
    PromotionAuthorityBasis,
    RunStatus,
)
from src.idea_evolution.domain.grounding import AuthorityProofValidator, GroundingRecord
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
from src.idea_evolution.orchestration.simple_loop import SimpleLoopRunner
from src.idea_evolution.providers.fake import FakeModelRunner
from src.idea_evolution.tracing.tracer import RunTracer


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
            core_mechanism_basis=PromotionAuthorityBasis.VALID_USER_DERIVATION,
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

        self.assertTrue(state.ontology_contradiction_detected)
        self.assertTrue(state.essence_drift_detected)
        self.assertTrue(any("sem justificativa registrada" in u for u in state.remaining_uncertainties))

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
            core_mechanism_basis="VALID_USER_DERIVATION",
            accepted_changes=[
                AcceptedChangeItem(
                    proposal="Wizard determinístico",
                    promotion_reason="Evita custos de inferência",
                    promotion_basis="VALID_USER_DERIVATION",
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

        self.assertNotIn("Clarificação interativa por LLM", state.candidate_extensions)
        self.assertIn("Mapeamento visual Mind-Map", state.candidate_extensions)
        self.assertEqual(len(state.rejected_changes), 1)

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
            core_mechanism_basis=PromotionAuthorityBasis.VALID_USER_DERIVATION,
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

        self.assertTrue(state.ontology_contradiction_detected)
        self.assertTrue(state.essence_drift_detected)
        self.assertTrue(any("referencia mecanismo rejeitado" in u for u in state.remaining_uncertainties))

    def test_04_reality_check_tested_core_must_match_accepted_core(self):
        """
        M05.1-R4 Failure A:
        O RealityCheck deve testar o Core aceito na Síntese. Se houver descompasso (mismatch),
        o FinalReview deve detectar determinísticamente.
        """
        synth_stage = SynthesizeStage()
        reality_stage = RealityCheckStage()
        review_stage = FinalReviewStage()

        state = SimpleIdeaState(
            run_id="TEST-RUN-009-R4-A",
            original_idea="Um aplicativo de ideação.",
        )

        # Síntese promove Local LLM
        synth_out = SynthesizeOutput(
            refined_idea="Ideia com LLM local",
            core_mechanism="Local Small Language Model com Knowledge Packs",
            core_mechanism_justification="Operação offline",
            core_mechanism_basis="VALID_USER_DERIVATION",
            accepted_changes=[],
            candidate_possibilities=[],
            rejected_changes=[],
        )
        synth_stage.apply_output_to_state(state, synth_out)

        # RealityCheck testa Wizard (Mismatch intencional)
        rc_out = RealityCheckOutput(
            target_core_mechanism="Wizard determinístico básico",  # MISMATCH
            feasibility_notes=[],
            reality_dependencies=["Suporte a HTML5"],
            claims_needing_evidence=[],
            potential_blockers=[],
            candidate_tests=["Testar fluxo de formulário"],
            exploratory_candidate_tests=[],
        )
        reality_stage.apply_output_to_state(state, rc_out)

        review_out = FinalReviewOutput(
            material_issues_remaining=[],
            essence_drift_detected=False,
            speculative_accretion_detected=False,
            ontology_contradiction_detected=False,
            recommendation="REFINED_IDEA_READY",
        )
        review_stage.apply_output_to_state(state, review_out)

        self.assertTrue(state.ontology_contradiction_detected)
        self.assertTrue(state.essence_drift_detected)
        self.assertTrue(any("CORE_MISMATCH" in u for u in state.remaining_uncertainties))

    def test_05_model_hypothesis_alone_cannot_authorize_core_promotion(self):
        """
        M05.1-R4 Failure B:
        Se core_mechanism_basis for MODEL_HYPOTHESIS (preocupação inventada pelo modelo),
        o FinalReview deve vetar determinísticamente.
        """
        state = SimpleIdeaState(
            run_id="TEST-RUN-009-R4-B",
            original_idea="Um aplicativo de ideação.",
            core_mechanism="Arquitetura offline local com criptografia P2P",
            core_mechanism_justification="Evita dependência de conexão à internet inventada pelo modelo",
            core_mechanism_basis=PromotionAuthorityBasis.MODEL_HYPOTHESIS,  # INVÁLIDO
        )

        review_stage = FinalReviewStage()
        review_out = FinalReviewOutput(
            material_issues_remaining=[],
            essence_drift_detected=False,
            speculative_accretion_detected=False,
            ontology_contradiction_detected=False,
            recommendation="REFINED_IDEA_READY",
        )
        review_stage.apply_output_to_state(state, review_out)

        self.assertTrue(state.ontology_contradiction_detected)
        self.assertTrue(state.essence_drift_detected)
        self.assertTrue(any("CIRCULAR_PROMOTION" in u for u in state.remaining_uncertainties))

    def test_06_core_mechanism_cannot_appear_in_exploratory_tests(self):
        """
        M05.1-R4 Failure C:
        Mecanismo do Core não pode constar na lista de testes exploratórios/não-core.
        """
        state = SimpleIdeaState(
            run_id="TEST-RUN-009-R4-C",
            original_idea="Um aplicativo de ideação.",
            core_mechanism="Local Small Language Model com Knowledge Packs",
            core_mechanism_justification="Derivação válida",
            core_mechanism_basis=PromotionAuthorityBasis.VALID_USER_DERIVATION,
            exploratory_candidate_tests=[
                "Medir uso de memória de Local Small Language Model em dispositivos móveis"  # ERRO: Core nos exploratórios
            ],
        )

        review_stage = FinalReviewStage()
        review_out = FinalReviewOutput(
            material_issues_remaining=[],
            essence_drift_detected=False,
            speculative_accretion_detected=False,
            ontology_contradiction_detected=False,
            recommendation="REFINED_IDEA_READY",
        )
        review_stage.apply_output_to_state(state, review_out)

        self.assertTrue(state.ontology_contradiction_detected)
        self.assertTrue(state.essence_drift_detected)
        self.assertTrue(any("CORE_IN_EXPLORATORY" in u for u in state.remaining_uncertainties))

    def test_07_rejected_proposal_cannot_become_recommended_next_step(self):
        """
        M05.1-R4 Failure C:
        O recommended_next_step não pode propor desenvolver um mecanismo rejeitado.
        """
        state = SimpleIdeaState(
            run_id="TEST-RUN-009-R4-D",
            original_idea="Um aplicativo de ideação.",
            core_mechanism="Wizard simples",
            core_mechanism_justification="Derivação válida",
            core_mechanism_basis=PromotionAuthorityBasis.VALID_USER_DERIVATION,
            recommended_next_step="Construir arquitetura de plugins e knowledge packs para modelo local",  # REJEITADO
            rejected_changes=[
                RejectedProposal(
                    proposal="Knowledge packs e plugins locais",
                    reason_rejected="Complexidade prematura para MVP",
                    source_stage="ALTERNATIVES",
                )
            ],
        )

        review_stage = FinalReviewStage()
        review_out = FinalReviewOutput(
            material_issues_remaining=[],
            essence_drift_detected=False,
            speculative_accretion_detected=False,
            ontology_contradiction_detected=False,
            recommendation="REFINED_IDEA_READY",
        )
        review_stage.apply_output_to_state(state, review_out)

        self.assertTrue(state.ontology_contradiction_detected)
        self.assertTrue(state.essence_drift_detected)
        self.assertTrue(any("REJECTED_AS_NEXT_STEP" in u for u in state.remaining_uncertainties))

    def test_08_immutable_run_id_generation_and_no_reuse(self):
        """
        M05.1-R4 Failure D:
        Garante que gerar múltiplos Run IDs nunca gere colisão e não dependa de listagem do disco.
        """
        id1 = RunTracer.generate_immutable_run_id()
        id2 = RunTracer.generate_immutable_run_id()
        self.assertNotEqual(id1, id2)
        self.assertTrue(id1.startswith("RUN-"))
        self.assertTrue(id2.startswith("RUN-"))

    def test_09_moving_artifact_dir_does_not_allow_id_reuse(self):
        """
        M05.1-R4 Failure D:
        Mesmo se o diretório runs/ for apagado ou movido, novos runs geram IDs únicos com timestamp e uuid.
        """
        with tempfile.TemporaryDirectory() as tmp1:
            dir1 = Path(tmp1)
            t1 = RunTracer(runs_dir=dir1)
            first_id = t1.run_id

        # Novo diretório vazio
        with tempfile.TemporaryDirectory() as tmp2:
            dir2 = Path(tmp2)
            t2 = RunTracer(runs_dir=dir2)
            second_id = t2.run_id

        self.assertNotEqual(first_id, second_id)

    # =========================================================================
    # M05.1-R5: AUTHORITY PROOF & FINAL GATE ENFORCEMENT ADVERSARIAL TESTS (1-12)
    # =========================================================================

    def test_10_organize_vague_ideas_cannot_ground_mindmap_as_user_explicit(self):
        """
        R5-Test 1: 'organize vague ideas' cannot ground 'mind-map' as USER_EXPLICIT.
        """
        orig = "Um aplicativo que ajuda pessoas a transformar ideias vagas em projetos mais claros."
        prop = "Interface visual de mapa mental incremental e drag-and-drop"
        valid, span, reason = AuthorityProofValidator.validate_user_explicit(orig, prop)
        self.assertFalse(valid)
        self.assertIn("SPOOFING_DETECTED", reason)

    def test_11_organize_vague_ideas_cannot_ground_encryption_as_user_explicit(self):
        """
        R5-Test 2: 'organize vague ideas' cannot ground 'encryption' as USER_EXPLICIT.
        """
        orig = "Um aplicativo que ajuda pessoas a transformar ideias vagas em projetos mais claros."
        prop = "Armazenamento local criptografado de ponta a ponta com chave assimétrica"
        valid, span, reason = AuthorityProofValidator.validate_user_explicit(orig, prop)
        self.assertFalse(valid)
        self.assertIn("SPOOFING_DETECTED", reason)

    def test_12_model_generated_privacy_concern_cannot_become_user_explicit(self):
        """
        R5-Test 3: model-generated privacy concern cannot become USER_EXPLICIT.
        """
        orig = "Plataforma web para conectar tutores e alunos de matemática."
        prop = "Sistema de privacidade e anonimização de dados biométricos"
        valid, span, reason = AuthorityProofValidator.validate_user_explicit(orig, prop)
        self.assertFalse(valid)
        self.assertIn("SPOOFING_DETECTED", reason)

    def test_13_model_cannot_fabricate_human_decision(self):
        """
        R5-Test 4: model cannot fabricate HUMAN_DECISION without registered human intervention.
        """
        valid, span, reason = AuthorityProofValidator.validate_human_decision(
            decision_ref="O operador humano decidiu adotar mapa mental",
            human_intervention_flag=False,  # Nenhuma intervenção real
        )
        self.assertFalse(valid)
        self.assertIn("FABRICATED_HUMAN_DECISION", reason)

    def test_14_external_evidence_requires_real_evidence_reference(self):
        """
        R5-Test 5: EXTERNAL_EVIDENCE requires real evidence reference (ID/URL/DOI), not model prose.
        """
        # Prosa de modelo sem ID formal -> REJEITADO
        valid, span, reason = AuthorityProofValidator.validate_external_evidence(
            "Pesquisas recentes de mercado indicam que usuários preferem mapas mentais"
        )
        self.assertFalse(valid)
        self.assertIn("INVALID_EVIDENCE_REF", reason)

        # Referência a ID auditável -> ACEITO
        valid_ok, span_ok, reason_ok = AuthorityProofValidator.validate_external_evidence("EXP-20260826-BENCH-001")
        self.assertTrue(valid_ok)

    def test_15_valid_user_derivation_cannot_be_assigned_solely_for_useful_mechanism(self):
        """
        R5-Test 6: VALID_USER_DERIVATION cannot be assigned solely because a mechanism is useful/plausible.
        """
        orig = "Um aplicativo que ajuda pessoas a transformar ideias vagas em projetos mais claros."
        intent = "Ajudar na clarificação de projetos"
        prop = "Interface visual de mapa mental"
        justification = "É uma interface moderna, útil, elegante e recomendada para ideação."
        valid, span, reason = AuthorityProofValidator.validate_user_derivation(orig, intent, prop, justification)
        self.assertFalse(valid)
        self.assertIn("INVALID_DERIVATION", reason)

    def test_16_invalid_authority_keeps_proposal_candidate(self):
        """
        R5-Test 7: invalid authority proof downgrades basis to MODEL_HYPOTHESIS and keeps proposal CANDIDATE.
        """
        synth_stage = SynthesizeStage()
        state = SimpleIdeaState(
            run_id="TEST-R5-P7",
            original_idea="Um aplicativo que ajuda pessoas a transformar ideias vagas em projetos mais claros.",
        )
        synth_out = SynthesizeOutput(
            refined_idea="Ideia refinada com mapa mental criptografado",
            core_mechanism="Interface visual de mapa mental incremental com armazenamento criptografado",
            core_mechanism_justification="pedido explícito do usuário por organização visual e proteção",
            core_mechanism_basis="USER_EXPLICIT",  # SPOOFING
            accepted_changes=[],
            candidate_possibilities=[],
            rejected_changes=[],
        )
        synth_stage.apply_output_to_state(state, synth_out)

        # Validador deve ter rebaixado a base e o registro ontológico deve ser CANDIDATE
        self.assertEqual(state.core_mechanism_basis, PromotionAuthorityBasis.MODEL_HYPOTHESIS)
        self.assertTrue(any("AUTHORITY_SPOOFING_BLOCKED" in u for u in state.remaining_uncertainties))
        self.assertEqual(state.proposal_records[0].ontology_state, OntologyState.CANDIDATE)

    def test_17_essence_drift_detected_makes_ready_impossible(self):
        """
        R5-Test 8: essence_drift_detected=true makes REFINED_IDEA_READY impossible in SimpleLoopRunner.
        """
        runner = SimpleLoopRunner()
        state = SimpleIdeaState(
            run_id="TEST-R5-P8",
            original_idea="Ideia original",
            essence_drift_detected=True,
            max_reconstructions=0,  # Sem budget
        )
        review_out = FinalReviewOutput(
            material_issues_remaining=[],
            essence_drift_detected=True,
            recommendation="REFINED_IDEA_READY",  # Modelo alucina READY
        )
        passes = runner._evaluate_hard_gates(state, review_out)
        self.assertFalse(passes)

    def test_18_ontology_contradiction_detected_makes_ready_impossible(self):
        """
        R5-Test 9: ontology_contradiction_detected=true makes REFINED_IDEA_READY impossible.
        """
        runner = SimpleLoopRunner()
        state = SimpleIdeaState(
            run_id="TEST-R5-P9",
            original_idea="Ideia original",
            ontology_contradiction_detected=True,
            max_reconstructions=0,
        )
        review_out = FinalReviewOutput(
            material_issues_remaining=[],
            recommendation="REFINED_IDEA_READY",
        )
        passes = runner._evaluate_hard_gates(state, review_out)
        self.assertFalse(passes)

    def test_19_hard_deterministic_gate_overrides_llm_recommendation_of_ready(self):
        """
        R5-Test 10: hard deterministic gate overrides an LLM recommendation of READY when core is MODEL_HYPOTHESIS.
        """
        runner = SimpleLoopRunner()
        state = SimpleIdeaState(
            run_id="TEST-R5-P10",
            original_idea="Ideia original",
            core_mechanism="Mapa mental",
            core_mechanism_basis=PromotionAuthorityBasis.MODEL_HYPOTHESIS,
            max_reconstructions=0,
        )
        review_out = FinalReviewOutput(
            material_issues_remaining=[],
            essence_drift_detected=False,
            ontology_contradiction_detected=False,
            recommendation="REFINED_IDEA_READY",  # LLM aprova
        )
        passes = runner._evaluate_hard_gates(state, review_out)
        self.assertFalse(passes)

    def test_20_reconstruction_occurs_when_budget_remains(self):
        """
        R5-Test 11: reconstruction occurs (reconstruction_count increments) when hard gates fail and budget remains.
        """
        spoofed_synth = {
            "SYNTHESIZE": {
                "refined_idea": "Refinada com mapa mental criptografado",
                "core_mechanism": "Mapa mental criptografado",
                "core_mechanism_justification": "Pedido do usuário",
                "core_mechanism_basis": "USER_EXPLICIT",  # Será rebaixado pelo validador determinístico
                "accepted_changes": [],
                "candidate_possibilities": [],
                "rejected_changes": [],
                "remaining_uncertainties": [],
                "known_risks": [],
                "recommended_next_step": "Testar",
            },
            "FINAL_REVIEW": {
                "material_issues_remaining": [],
                "essence_drift_detected": False,
                "speculative_accretion_detected": False,
                "ontology_contradiction_detected": False,
                "recommendation": "REFINED_IDEA_READY",
                "review_summary": "Tudo ok",
            }
        }
        runner = FakeModelRunner(custom_responses=spoofed_synth)
        loop = SimpleLoopRunner(runner=runner)

        state = loop.run("Um aplicativo que ajuda pessoas a transformar ideias vagas em projetos mais claros.")
        # Como o spoofing foi rebaixado e a base do core virou MODEL_HYPOTHESIS, o gate falhou e acionou reconstrução (attempt=2)
        self.assertEqual(state.reconstruction_count, 1)
        self.assertEqual(state.status, RunStatus.REFINEMENT_INCOMPLETE)

    def test_21_exhausted_reconstruction_cannot_emit_ready(self):
        """
        R5-Test 12: exhausted reconstruction cannot emit READY when hard gates fail; emits REFINEMENT_INCOMPLETE.
        """
        spoofed_synth = {
            "SYNTHESIZE": {
                "refined_idea": "Refinada com mapa mental criptografado",
                "core_mechanism": "Mapa mental criptografado",
                "core_mechanism_justification": "Pedido do usuário",
                "core_mechanism_basis": "USER_EXPLICIT",
                "accepted_changes": [],
                "candidate_possibilities": [],
                "rejected_changes": [],
                "remaining_uncertainties": [],
                "known_risks": [],
                "recommended_next_step": "Testar",
            },
            "FINAL_REVIEW": {
                "material_issues_remaining": [],
                "essence_drift_detected": False,
                "speculative_accretion_detected": False,
                "ontology_contradiction_detected": False,
                "recommendation": "REFINED_IDEA_READY",
                "review_summary": "Tudo ok",
            }
        }
        runner = FakeModelRunner(custom_responses=spoofed_synth)
        loop = SimpleLoopRunner(runner=runner)

        state = loop.run("Um aplicativo que ajuda pessoas a transformar ideias vagas em projetos mais claros.")
        self.assertNotEqual(state.status, RunStatus.REFINED_IDEA_READY)
        self.assertEqual(state.status, RunStatus.REFINEMENT_INCOMPLETE)


if __name__ == "__main__":
    unittest.main(verbosity=2)
