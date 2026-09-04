"""
tests/test_fioideias_v1_provenance_guard.py
Testes adversariais e de salvaguardas ontológicas para a Fase P3 (M06).

Valida deterministicamente que:
1. MODEL_CANDIDATE -> USER_EXPLICIT falha categoricamente.
2. MODEL_CANDIDATE -> VALID_USER_DERIVATION sem prova de autoridade falha.
3. Intenção humana derivada preserva status não-explícito após serialização/recarga.
4. refined_idea oriunda de proposta do modelo não é rotulada como USER_EXPLICIT.
5. Repetição de candidato em múltiplos estágios não gera upgrade de autoridade.
6. Seleção de candidato como próximo passo acionável não gera autoridade do usuário.
7. Itens de incerteza (unknown) preservam status após serialização/recarga.
8. Incertezas não desaparecem silenciosamente no mapeamento.
9. Textos gerados na Condição A não assumem proveniência USER_EXPLICIT.
10. Tentativas de spoofing na Condição B são contidas na fronteira de produto.
11. Violações e adulterações (tampering) no SourceAnchor são detectadas deterministicamente.
12. Round-trip completo JSON preserva 100% das etiquetas de autoridade e ontologia.
13. Entrada crua original é preservada sem distorções de normalização.
14. Resposta do IdeaEvolutionService preserva a proveniência tipada do artefato.
15. Chaves e segredos não vazam nos campos de proveniência e auditoria.
16. Zero chamadas de modelo (custo 0, 100% determinístico).
17. ProvenanceReceipt audita completude com unlabeled_semantic_item_count == 0.
18. Hash do núcleo científico Lean L1 permanece estritamente idêntico.
"""

import unittest
import hashlib
import json
import tempfile
import shutil
from pathlib import Path

from src.idea_evolution.artifacts.evolution_artifact import (
    EvolutionArtifact,
    CritiqueItem,
    CandidatePossibility,
    TreatmentMode,
    SCHEMA_VERSION_1_0,
    FROZEN_LEAN_CORE_HASH,
)
from src.idea_evolution.artifacts.mapper import EvolutionArtifactMapper
from src.idea_evolution.artifacts.provenance import (
    ProvenanceReceipt,
    audit_artifact_provenance,
)
from src.idea_evolution.domain.state import (
    PromotionAuthorityBasis,
    OntologyState,
    SimpleIdeaState,
    ProposalRecord,
    CriticalIssue,
    AlternativeMechanism,
)
from src.idea_evolution.domain.epistemic_contracts import SourceAnchor, SourceAnchorKind
from src.idea_evolution.domain.grounding import AuthorityProofValidator
from src.idea_evolution.service.evolution_service import IdeaEvolutionService
from src.idea_evolution.providers.fake import FakeModelRunner


class TestProvenanceAndOntologyEnforcementP3(unittest.TestCase):

    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp(prefix="test_provenance_p3_"))
        self.runs_dir = self.test_dir / "runs"
        self.runs_dir.mkdir(parents=True, exist_ok=True)

        self.sample_idea = "Criar um gestor de tarefas para estudantes universitários."
        self.valid_anchor = SourceAnchor.create_human_input_anchor(self.sample_idea)

        self.default_first_pass = {
            "interpreted_problem": "Estudantes têm prazos concorrentes e procrastinam.",
            "human_intent": "Organizar entregas acadêmicas para evitar atrasos.",
            "primary_mechanism": {
                "mechanism": "Quadro Kanban automático integrado ao calendário de provas",
                "is_explicit_in_source": False,
                "claimed_basis": "MODEL_HYPOTHESIS",
                "justification": "Estrutura visual de tarefas com datas críticas.",
                "tradeoffs": ["Exige sincronização de calendário"],
            },
            "competing_alternatives": [
                {
                    "mechanism": "Notificações diárias com lista de prioridades simples",
                    "is_explicit_in_source": False,
                    "claimed_basis": "MODEL_HYPOTHESIS",
                    "justification": "Menor esforço de manutenção.",
                    "tradeoffs": ["Menos visão panorâmica"],
                }
            ],
            "key_assumptions": ["Estudantes mantêm as datas do calendário atualizadas"],
            "material_ambiguities": ["Como importar grades semestrais automaticamente?"],
            "material_vulnerabilities": [
                {
                    "vulnerability": "Usuário pode abandonar o preenchimento manual de prazos.",
                    "why_it_matters": "O Kanban desatualizado perde utilidade.",
                    "severity": "HIGH",
                    "affected_aspect": "Engajamento",
                }
            ],
            "remaining_uncertainties": ["Qual a taxa de adesão sem integração direta com o AVA?"],
            "requires_human_normative_choice": False,
            "proposed_next_action": "Entrevistar 10 estudantes sobre o uso de calendário",
        }

    def tearDown(self):
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def test_01_model_candidate_to_user_explicit_fails(self):
        """1: MODEL_CANDIDATE -> USER_EXPLICIT deve falhar categoricamente."""
        with self.assertRaises(ValueError) as ctx:
            CandidatePossibility(
                mechanism="Algoritmo avançado de IA para priorização",
                authority_basis=PromotionAuthorityBasis.USER_EXPLICIT,
            )
        self.assertIn("CandidatePossibility não pode assumir base de autoridade", str(ctx.exception))

    def test_02_model_candidate_to_valid_derivation_without_proof_fails(self):
        """2: MODEL_CANDIDATE -> VALID_USER_DERIVATION sem prova de autoridade deve falhar."""
        # 2a. Candidato direto não pode alegar VALID_USER_DERIVATION
        with self.assertRaises(ValueError) as ctx:
            CandidatePossibility(
                mechanism="Mecanismo sugerido",
                authority_basis=PromotionAuthorityBasis.VALID_USER_DERIVATION,
            )
        self.assertIn("CandidatePossibility não pode assumir base de autoridade", str(ctx.exception))

        # 2b. AuthorityProofValidator rejeita deduções baseadas em mera conveniência/utilidade
        is_valid, _, reason = AuthorityProofValidator.validate_user_derivation(
            original_idea=self.sample_idea,
            human_intent="Organizar entregas acadêmicas",
            proposition="Sistema de IA generativa com blockchain",
            derivation_proof="Seria muito útil e moderno integrar IA para os estudantes.",
        )
        self.assertFalse(is_valid)
        self.assertIn("INVALID_DERIVATION", reason)

    def test_03_derived_intent_serialization_roundtrip_remains_derived(self):
        """3: Intenção humana derivada serializada e recarregada DEVE permanecer derivada."""
        art = EvolutionArtifact(
            artifact_id="ART-TEST-03",
            run_id="RUN-03",
            treatment_mode=TreatmentMode.LEAN_L1,
            terminal_status="COMPLETED_DIRECT_ONE_PASS",
            original_idea=self.sample_idea,
            human_intent="Intenção inferida pelo sistema",
            intent_provenance=PromotionAuthorityBasis.VALID_USER_DERIVATION,
            refined_idea="Quadro Kanban",
            source_anchor=self.valid_anchor,
        )

        serialized = art.model_dump_json()
        reloaded = EvolutionArtifact.model_validate_json(serialized)

        self.assertEqual(reloaded.intent_provenance, PromotionAuthorityBasis.VALID_USER_DERIVATION)
        self.assertNotEqual(reloaded.intent_provenance, PromotionAuthorityBasis.USER_EXPLICIT)

    def test_04_refined_idea_from_model_cannot_claim_user_explicit(self):
        """4: refined_idea gerada pelo modelo não pode receber autoridade USER_EXPLICIT."""
        with self.assertRaises(ValueError) as ctx:
            EvolutionArtifact(
                artifact_id="ART-TEST-04",
                run_id="RUN-04",
                treatment_mode=TreatmentMode.LEAN_L1,
                terminal_status="COMPLETED_DIRECT_ONE_PASS",
                original_idea=self.sample_idea,
                human_intent="Organizar prazos",
                intent_provenance=PromotionAuthorityBasis.VALID_USER_DERIVATION,
                refined_idea="Quadro Kanban com IA e algoritmo preditivo",
                refined_idea_authority=PromotionAuthorityBasis.USER_EXPLICIT,  # SPOOFING!
                source_anchor=self.valid_anchor,
            )
        self.assertIn("Authority Spoofing", str(ctx.exception))

    def test_05_repetition_does_not_create_authority(self):
        """5: Repetição de candidato em múltiplos estágios NÃO altera autoridade."""
        runner = FakeModelRunner(
            custom_responses={
                "LEAN_FIRST_PASS": self.default_first_pass,
                "FOCUSED_ESCALATION": {
                    "escalation_reason": "MATERIAL_VULNERABILITY",
                    "target_hypothesis": "Kanban automático integrado ao calendário",
                    "focused_critique_or_analysis": "Análise aprofundada repetindo o Kanban.",
                    "resolved_tradeoffs": ["Tradeoff resolvido"],
                    "discriminating_tests": ["Teste 1"],
                    "hypothesis_mutated": False,
                    "mutated_hypothesis_description": "",
                    "decision_progress_made": True,
                    "updated_next_action": "Validar o Kanban",
                },
            }
        )
        service = IdeaEvolutionService(runner=runner, runs_dir=self.runs_dir)
        resp = service.evolve_idea(self.sample_idea)

        self.assertTrue(resp.success)
        art = resp.artifact
        # Mesmo repetido na escalação, refined_idea permanece MODEL_HYPOTHESIS
        self.assertEqual(art.refined_idea_authority, PromotionAuthorityBasis.MODEL_HYPOTHESIS)
        self.assertNotEqual(art.refined_idea_authority, PromotionAuthorityBasis.USER_EXPLICIT)

    def test_06_selection_as_recommended_path_does_not_create_authority(self):
        """6: Seleção de candidato como recommended_next_action não gera autoridade do usuário."""
        runner = FakeModelRunner(custom_responses={"LEAN_FIRST_PASS": self.default_first_pass})
        service = IdeaEvolutionService(runner=runner, runs_dir=self.runs_dir)
        resp = service.evolve_idea(self.sample_idea)

        art = resp.artifact
        self.assertTrue(len(art.recommended_next_action) > 0)
        # Candidatos continuam MODEL_HYPOTHESIS mesmo que um deles seja promovido a próximo passo
        for cand in art.candidate_possibilities:
            self.assertEqual(cand.authority_basis, PromotionAuthorityBasis.MODEL_HYPOTHESIS)
            self.assertNotEqual(cand.authority_basis, PromotionAuthorityBasis.USER_EXPLICIT)

    def test_07_unknown_serialized_reloaded_remains_unknown(self):
        """7: Itens de incerteza (unknown) serializados/recarregados preservam status."""
        runner = FakeModelRunner(custom_responses={"LEAN_FIRST_PASS": self.default_first_pass})
        service = IdeaEvolutionService(runner=runner, runs_dir=self.runs_dir)
        resp = service.evolve_idea(self.sample_idea)

        art = resp.artifact
        self.assertTrue(len(art.uncertainties) > 0)
        original_uncertainties = list(art.uncertainties)

        reloaded = EvolutionArtifact.model_validate_json(art.model_dump_json())
        self.assertEqual(reloaded.uncertainties, original_uncertainties)

        receipt = reloaded.audit_provenance()
        self.assertEqual(receipt.unknown_count, len(original_uncertainties))

    def test_08_uncertainty_cannot_silently_disappear_in_mapper(self):
        """8: Incertezas não podem sumir silenciosamente durante o mapeamento."""
        runner = FakeModelRunner(custom_responses={"LEAN_FIRST_PASS": self.default_first_pass})
        service = IdeaEvolutionService(runner=runner, runs_dir=self.runs_dir)
        resp = service.evolve_idea(self.sample_idea)

        art = resp.artifact
        # Both remaining_uncertainties and material_ambiguities must be preserved
        self.assertTrue(any("taxa de adesão" in u for u in art.uncertainties))
        self.assertTrue(any("importar grades" in u for u in art.uncertainties))

    def test_09_condition_a_model_text_cannot_claim_user_explicit(self):
        """9: Texto gerado na Condição A não assume proveniência USER_EXPLICIT."""
        base_data = {
            "success": True,
            "parsed_output": {
                "summary": "Resumo baseline gerado pelo modelo.",
                "refined_version": "Versão refinada baseline gerada pelo modelo.",
                "tradeoffs": ["Tradeoff 1"],
                "next_step": "Ação 1",
            },
        }
        art = EvolutionArtifactMapper.map_baseline_result(
            baseline_data=base_data,
            original_idea=self.sample_idea,
            run_id="RUN-BASE-P3",
        )
        self.assertEqual(art.refined_idea_authority, PromotionAuthorityBasis.MODEL_HYPOTHESIS)
        self.assertEqual(art.original_idea_authority, PromotionAuthorityBasis.USER_EXPLICIT)
        self.assertIsNone(art.source_anchor)  # Não fabrica SourceAnchor

    def test_10_condition_b_spoofing_contained_at_product_boundary(self):
        """10: Tentativas de spoofing na Condição B são contidas na fronteira de produto."""
        state = SimpleIdeaState(
            run_id="RUN-B-P3",
            original_idea=self.sample_idea,
            proposal_records=[
                ProposalRecord(
                    proposal="Funcionalidade inventada não presente no input",
                    promotion_basis=PromotionAuthorityBasis.USER_EXPLICIT,  # Spoofing interno
                )
            ],
            alternatives=[
                AlternativeMechanism(
                    mechanism="Alternativa profunda B",
                    tradeoffs=["Pró", "Contra"],
                    novelty_or_difference="Testar isolamento",
                )
            ],
        )

        art = EvolutionArtifactMapper.map_simple_state(state=state, run_id="RUN-B-P3")

        # Verifica que o candidato permanece estritamente MODEL_HYPOTHESIS
        self.assertEqual(len(art.candidate_possibilities), 1)
        self.assertEqual(art.candidate_possibilities[0].authority_basis, PromotionAuthorityBasis.MODEL_HYPOTHESIS)
        self.assertEqual(art.refined_idea_authority, PromotionAuthorityBasis.MODEL_HYPOTHESIS)

    def test_11_source_anchor_tamper_detection(self):
        """11: Adulteração no SourceAnchor (hash ou conteúdo) é detectada deterministicamente."""
        # 11a. Hash adulterado (não bate com SHA-256 do conteúdo)
        bad_hash_anchor = SourceAnchor(
            source_id="SRC-BAD-1",
            original_content=self.sample_idea,
            content_hash="0000000000000000000000000000000000000000000000000000000000000000",
            source_kind=SourceAnchorKind.HUMAN_INPUT,
        )
        with self.assertRaises(ValueError) as ctx1:
            EvolutionArtifact(
                artifact_id="ART-TAMPER-1",
                run_id="RUN-T1",
                treatment_mode=TreatmentMode.LEAN_L1,
                terminal_status="COMPLETED_DIRECT_ONE_PASS",
                original_idea=self.sample_idea,
                human_intent="Intenção",
                refined_idea="Ideia refinada",
                source_anchor=bad_hash_anchor,
            )
        self.assertIn("Tamper detected", str(ctx1.exception))

        # 11b. original_idea difere do original_content do SourceAnchor
        diff_anchor = SourceAnchor.create_human_input_anchor("Outro texto completamente diferente")
        with self.assertRaises(ValueError) as ctx2:
            EvolutionArtifact(
                artifact_id="ART-TAMPER-2",
                run_id="RUN-T2",
                treatment_mode=TreatmentMode.LEAN_L1,
                terminal_status="COMPLETED_DIRECT_ONE_PASS",
                original_idea=self.sample_idea,
                human_intent="Intenção",
                refined_idea="Ideia refinada",
                source_anchor=diff_anchor,
            )
        self.assertIn("Tamper detected", str(ctx2.exception))

    def test_12_artifact_roundtrip_preserves_epistemic_labels(self):
        """12: Round-trip serialização/recarga preserva todas as classes epistêmicas."""
        runner = FakeModelRunner(custom_responses={"LEAN_FIRST_PASS": self.default_first_pass})
        service = IdeaEvolutionService(runner=runner, runs_dir=self.runs_dir)
        resp = service.evolve_idea(self.sample_idea)

        original = resp.artifact
        json_data = original.model_dump_json(indent=2)
        reloaded = EvolutionArtifact.model_validate_json(json_data)

        self.assertEqual(original.original_idea_authority, reloaded.original_idea_authority)
        self.assertEqual(original.intent_provenance, reloaded.intent_provenance)
        self.assertEqual(original.refined_idea_authority, reloaded.refined_idea_authority)
        self.assertEqual(original.assumptions_authority, reloaded.assumptions_authority)
        self.assertEqual(
            original.candidate_possibilities[0].authority_basis,
            reloaded.candidate_possibilities[0].authority_basis,
        )
        self.assertEqual(
            original.candidate_possibilities[0].ontology_state,
            reloaded.candidate_possibilities[0].ontology_state,
        )

    def test_13_original_input_preserved_exactly(self):
        """13: Entrada original crua preservada sem modificações."""
        raw_text = "   Espaços no início e pontuação exótica: !!!   "
        runner = FakeModelRunner(custom_responses={"LEAN_FIRST_PASS": self.default_first_pass})
        service = IdeaEvolutionService(runner=runner, runs_dir=self.runs_dir)
        resp = service.evolve_idea(raw_text)

        self.assertEqual(resp.artifact.original_idea, raw_text)

    def test_14_service_response_preserves_artifact_provenance(self):
        """14: Resposta do IdeaEvolutionService preserva o artefato e proveniência intactos."""
        runner = FakeModelRunner(custom_responses={"LEAN_FIRST_PASS": self.default_first_pass})
        service = IdeaEvolutionService(runner=runner, runs_dir=self.runs_dir)
        resp = service.evolve_idea(self.sample_idea)

        self.assertIsNotNone(resp.artifact)
        self.assertEqual(resp.artifact.original_idea_authority, PromotionAuthorityBasis.USER_EXPLICIT)
        self.assertEqual(resp.artifact.intent_provenance, PromotionAuthorityBasis.VALID_USER_DERIVATION)
        self.assertEqual(resp.artifact.refined_idea_authority, PromotionAuthorityBasis.MODEL_HYPOTHESIS)

    def test_15_no_secret_material_in_provenance(self):
        """15: Nenhum dado confidencial ou chave de API está presente no artefato ou recibo."""
        runner = FakeModelRunner(custom_responses={"LEAN_FIRST_PASS": self.default_first_pass})
        service = IdeaEvolutionService(runner=runner, runs_dir=self.runs_dir)
        resp = service.evolve_idea(self.sample_idea)

        art_json = resp.artifact.model_dump_json()
        receipt_json = resp.artifact.audit_provenance().model_dump_json()

        for forbidden in ["csk-", "gsk_", "sk-", "password", "bearer ", "api_key"]:
            self.assertNotIn(forbidden, art_json.lower())
            self.assertNotIn(forbidden, receipt_json.lower())

    def test_16_zero_model_calls_for_provenance_audit(self):
        """16: Auditoria de proveniência não realiza nenhuma chamada de IA (custo 0)."""
        runner = FakeModelRunner(custom_responses={"LEAN_FIRST_PASS": self.default_first_pass})
        service = IdeaEvolutionService(runner=runner, runs_dir=self.runs_dir)
        resp = service.evolve_idea(self.sample_idea)

        calls_before = sum(runner.call_counts.values())

        # Auditoria determinística de proveniência
        receipt = resp.artifact.audit_provenance()

        calls_after = sum(runner.call_counts.values())
        self.assertEqual(calls_before, calls_after)
        self.assertTrue(receipt.is_epistemically_safe)

    def test_17_provenance_completeness_receipt_unlabeled_count_is_zero(self):
        """17: ProvenanceReceipt relata unlabeled_semantic_item_count == 0 para artefatos canônicos."""
        runner = FakeModelRunner(custom_responses={"LEAN_FIRST_PASS": self.default_first_pass})
        service = IdeaEvolutionService(runner=runner, runs_dir=self.runs_dir)
        resp = service.evolve_idea(self.sample_idea)

        receipt = resp.artifact.audit_provenance()

        self.assertEqual(receipt.unlabeled_semantic_item_count, 0)
        self.assertTrue(receipt.user_explicit_count >= 1)     # original_idea
        self.assertTrue(receipt.valid_derivation_count >= 1)  # human_intent
        self.assertTrue(receipt.model_candidate_count >= 2)   # refined_idea + assumptions + alternatives
        self.assertTrue(receipt.unknown_count >= 1)           # uncertainties
        self.assertTrue(receipt.is_epistemically_safe)

    def test_18_candidate_core_spoofing_fails(self):
        """18: Tentativa de candidato alegar estado ontológico CORE falha."""
        with self.assertRaises(ValueError) as ctx:
            CandidatePossibility(
                mechanism="Candidato que tenta usurpar estado ontológico central",
                ontology_state=OntologyState.CORE,
            )
        self.assertIn("CandidatePossibility não pode assumir estado ontológico CORE", str(ctx.exception))

    def test_19_assumptions_cannot_be_user_explicit(self):
        """19: Premissas do sistema não podem ser rotuladas como USER_EXPLICIT."""
        with self.assertRaises(ValueError) as ctx:
            EvolutionArtifact(
                artifact_id="ART-ASSUMP-FAIL",
                run_id="RUN-FAIL",
                treatment_mode=TreatmentMode.LEAN_L1,
                terminal_status="COMPLETED_DIRECT_ONE_PASS",
                original_idea=self.sample_idea,
                human_intent="Intenção",
                refined_idea="Refinada",
                assumptions=["Premissa inventada"],
                assumptions_authority=PromotionAuthorityBasis.USER_EXPLICIT,  # Proibido!
                source_anchor=self.valid_anchor,
            )
        self.assertIn("premissas (assumptions) não podem ter autoridade USER_EXPLICIT", str(ctx.exception))

    def test_20_scientific_core_hash_remains_strictly_unchanged(self):
        """20: Integridade inegociável do hash SHA-256 do núcleo científico Lean L1."""
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

        self.assertEqual(combined.hexdigest(), FROZEN_LEAN_CORE_HASH)


if __name__ == "__main__":
    unittest.main(verbosity=2)
