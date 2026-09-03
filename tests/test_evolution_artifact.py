"""
tests/test_evolution_artifact.py
Testes determinísticos para o EvolutionArtifact e EvolutionArtifactMapper (M06 P2).

Zero chamadas de rede.
Zero consumo de tokens.
Valida conformidade com os 20 critérios de aceitação da Fase P2.
"""

import unittest
import shutil
import tempfile
import hashlib
import json
from pathlib import Path

from src.idea_evolution.artifacts.evolution_artifact import (
    EvolutionArtifact,
    CritiqueItem,
    CandidatePossibility,
    SCHEMA_VERSION_1_0,
    FROZEN_LEAN_CORE_HASH,
)
from src.idea_evolution.artifacts.mapper import EvolutionArtifactMapper
from src.idea_evolution.service.contracts import (
    EvolutionRequest,
    TreatmentMode,
    ServiceFailureType,
)
from src.idea_evolution.service.evolution_service import IdeaEvolutionService
from src.idea_evolution.domain.state import PromotionAuthorityBasis
from src.idea_evolution.domain.epistemic_contracts import SourceAnchor, SourceAnchorKind
from src.idea_evolution.providers.fake import FakeModelRunner


class TestEvolutionArtifactP2(unittest.TestCase):

    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp(prefix="test_artifact_p2_"))
        self.runs_dir = self.test_dir / "runs"
        self.runs_dir.mkdir(parents=True, exist_ok=True)

        self.sample_idea = "Criar um sistema de recomendação de livros baseado em micro-resenhas de leitores."

        self.default_first_pass = {
            "interpreted_problem": "Leitores perdem tempo escolhendo livros longos sem saber se combinam com seu momento.",
            "human_intent": "Encontrar rapidamente boas leituras a partir de sínteses curtas e autênticas.",
            "primary_mechanism": {
                "mechanism": "Feed de micro-resenhas com até 140 caracteres e tags temáticas",
                "is_explicit_in_source": False,
                "claimed_basis": "MODEL_HYPOTHESIS",
                "justification": "Mecanismo conciso de baixo esforço cognitivo.",
                "tradeoffs": ["Pode simplificar análises literárias profundas"],
            },
            "competing_alternatives": [
                {
                    "mechanism": "Algoritmo de grafo social de afinidade literária",
                    "is_explicit_in_source": False,
                    "claimed_basis": "MODEL_HYPOTHESIS",
                    "justification": "Explora rede de amizades.",
                    "tradeoffs": ["Problema de cold start"],
                }
            ],
            "key_assumptions": ["Leitores estão dispostos a escrever resenhas de 140 caracteres"],
            "material_ambiguities": ["Como evitar spam de resenhas promocionais?"],
            "material_vulnerabilities": [
                {
                    "vulnerability": "Risco de resenhas vazias ou piadas diminuírem a qualidade da recomendação.",
                    "why_it_matters": "Quebra a confiança na curadoria.",
                    "severity": "HIGH",
                    "affected_aspect": "Qualidade do Conteúdo",
                }
            ],
            "remaining_uncertainties": ["Qual a adesão mínima para relevância estatística?"],
            "requires_human_normative_choice": False,
            "proposed_next_action": "Validar interesse com 20 leitores ativos",
        }

    def tearDown(self):
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def test_01_direct_lean_completion_maps_to_valid_evolution_artifact(self):
        """1: Execução nominal de 1 passada Lean L1 gera EvolutionArtifact válido."""
        # Sem severidade HIGH e sem alternativas concorrentes para que complete em 1 passada
        one_pass_data = dict(self.default_first_pass)
        one_pass_data["material_vulnerabilities"] = []
        one_pass_data["competing_alternatives"] = []

        runner = FakeModelRunner(custom_responses={"LEAN_FIRST_PASS": one_pass_data})
        service = IdeaEvolutionService(runner=runner, runs_dir=self.runs_dir)

        resp = service.evolve_idea(self.sample_idea)

        self.assertTrue(resp.success)
        self.assertIsNotNone(resp.artifact)
        self.assertIsInstance(resp.artifact, EvolutionArtifact)
        self.assertEqual(resp.artifact.schema_version, SCHEMA_VERSION_1_0)
        self.assertEqual(resp.artifact.terminal_status, "COMPLETED_DIRECT_ONE_PASS")
        self.assertEqual(resp.artifact.treatment_mode, TreatmentMode.LEAN_L1)

    def test_02_focused_escalation_maps_correctly(self):
        """2: Escalação focada mapeia mutação e crítica aprofundada corretamente."""
        escalation_data = {
            "escalation_reason": "MATERIAL_VULNERABILITY",
            "target_hypothesis": "Risco de resenhas vazias ou piadas.",
            "focused_critique_or_analysis": "Sistema de reputação por votos úteis mitiga ruído inicial.",
            "resolved_tradeoffs": ["Adiciona barreira de entrada em prol de qualidade."],
            "discriminating_tests": ["Testar filtro de 3 upvotes mínimos antes de exibir na home."],
            "hypothesis_mutated": True,
            "mutated_hypothesis_description": "Feed de micro-resenhas curadas por reputação comunitária",
            "decision_progress_made": True,
            "updated_next_action": "Criar protótipo com regra de 3 upvotes",
        }

        runner = FakeModelRunner(
            custom_responses={
                "LEAN_FIRST_PASS": self.default_first_pass,
                "FOCUSED_ESCALATION": escalation_data,
            }
        )
        service = IdeaEvolutionService(runner=runner, runs_dir=self.runs_dir)

        resp = service.evolve_idea(self.sample_idea)

        self.assertTrue(resp.success)
        art = resp.artifact
        self.assertIsNotNone(art)
        self.assertEqual(art.terminal_status, "COMPLETED_WITH_FOCUSED_ESCALATION")
        self.assertEqual(art.refined_idea, "Feed de micro-resenhas curadas por reputação comunitária")
        self.assertEqual(art.recommended_next_action, "Criar protótipo com regra de 3 upvotes")
        self.assertTrue(any("reputação por votos" in c.vulnerability for c in art.critique))

    def test_03_human_decision_required_represented_as_valid_domain_outcome(self):
        """3: HUMAN_DECISION_REQUIRED é representado honestamente como desfecho de domínio (não erro)."""
        normative_data = dict(self.default_first_pass)
        normative_data["requires_human_normative_choice"] = True
        normative_data["human_choice_description"] = "Permitir ou proibir resenhas patrocinadas por editoras?"

        runner = FakeModelRunner(custom_responses={"LEAN_FIRST_PASS": normative_data})
        service = IdeaEvolutionService(runner=runner, runs_dir=self.runs_dir)

        resp = service.evolve_idea(self.sample_idea)

        self.assertTrue(resp.success)
        art = resp.artifact
        self.assertTrue(art.human_decision_required)
        self.assertEqual(art.terminal_status, "HUMAN_DECISION_REQUIRED")
        self.assertIn("editoras", art.recommended_next_action)
        self.assertIn("editoras", art.human_decision_description)

    def test_04_original_idea_preserved_lossless(self):
        """4: original_idea preservada exatamente, sem normalização destrutiva."""
        raw = "   Minha ideia com espaços e pontuação: Teste!   "
        runner = FakeModelRunner(custom_responses={"LEAN_FIRST_PASS": self.default_first_pass})
        service = IdeaEvolutionService(runner=runner, runs_dir=self.runs_dir)

        resp = service.evolve_idea(raw)

        self.assertEqual(resp.artifact.original_idea, raw)

    def test_05_refined_idea_preserved(self):
        """5: refined_idea presente e acessível diretamente no nível do artefato."""
        one_pass_data = dict(self.default_first_pass)
        one_pass_data["material_vulnerabilities"] = []

        runner = FakeModelRunner(custom_responses={"LEAN_FIRST_PASS": one_pass_data})
        service = IdeaEvolutionService(runner=runner, runs_dir=self.runs_dir)

        resp = service.evolve_idea(self.sample_idea)

        self.assertEqual(
            resp.artifact.refined_idea,
            "Feed de micro-resenhas com até 140 caracteres e tags temáticas",
        )

    def test_06_human_intent_provenance_not_upgraded_silently(self):
        """6: human_intent derivado do modelo NÃO é rotulado como USER_EXPLICIT."""
        runner = FakeModelRunner(custom_responses={"LEAN_FIRST_PASS": self.default_first_pass})
        service = IdeaEvolutionService(runner=runner, runs_dir=self.runs_dir)

        resp = service.evolve_idea(self.sample_idea)

        self.assertNotEqual(resp.artifact.intent_provenance, PromotionAuthorityBasis.USER_EXPLICIT)
        self.assertEqual(resp.artifact.intent_provenance, PromotionAuthorityBasis.VALID_USER_DERIVATION)

    def test_07_model_candidates_remain_non_authoritative(self):
        """7: Candidatos propostos pelo sistema permanecem rotulados como MODEL_HYPOTHESIS."""
        runner = FakeModelRunner(custom_responses={"LEAN_FIRST_PASS": self.default_first_pass})
        service = IdeaEvolutionService(runner=runner, runs_dir=self.runs_dir)

        resp = service.evolve_idea(self.sample_idea)

        for cand in resp.artifact.candidate_possibilities:
            self.assertEqual(cand.authority_basis, PromotionAuthorityBasis.MODEL_HYPOTHESIS)

    def test_08_uncertainty_survives_mapping(self):
        """8: Incertezas materiais sobrevivem intactas ao mapeamento."""
        runner = FakeModelRunner(custom_responses={"LEAN_FIRST_PASS": self.default_first_pass})
        service = IdeaEvolutionService(runner=runner, runs_dir=self.runs_dir)

        resp = service.evolve_idea(self.sample_idea)

        self.assertTrue(len(resp.artifact.uncertainties) >= 1)
        self.assertTrue(any("relevância estatística" in u for u in resp.artifact.uncertainties))

    def test_09_assumptions_survive_mapping(self):
        """9: Premissas não verificadas sobrevivem ao mapeamento."""
        runner = FakeModelRunner(custom_responses={"LEAN_FIRST_PASS": self.default_first_pass})
        service = IdeaEvolutionService(runner=runner, runs_dir=self.runs_dir)

        resp = service.evolve_idea(self.sample_idea)

        self.assertIn(
            "Leitores estão dispostos a escrever resenhas de 140 caracteres",
            resp.artifact.assumptions,
        )

    def test_10_next_action_survives_mapping(self):
        """10: Próximo passo acionável é mapeado diretamente."""
        one_pass_data = dict(self.default_first_pass)
        one_pass_data["material_vulnerabilities"] = []
        one_pass_data["competing_alternatives"] = []

        runner = FakeModelRunner(custom_responses={"LEAN_FIRST_PASS": one_pass_data})
        service = IdeaEvolutionService(runner=runner, runs_dir=self.runs_dir)

        resp = service.evolve_idea(self.sample_idea)

        self.assertEqual(resp.artifact.recommended_next_action, "Validar interesse com 20 leitores ativos")

    def test_11_source_anchor_and_provenance_survive(self):
        """11: SourceAnchor e hash de núcleo científico sobrevivem no artefato."""
        runner = FakeModelRunner(custom_responses={"LEAN_FIRST_PASS": self.default_first_pass})
        service = IdeaEvolutionService(runner=runner, runs_dir=self.runs_dir)

        resp = service.evolve_idea(self.sample_idea)

        art = resp.artifact
        self.assertIsNotNone(art.source_anchor)
        self.assertEqual(art.source_anchor.original_content, self.sample_idea)
        self.assertEqual(art.scientific_core_hash, FROZEN_LEAN_CORE_HASH)

    def test_12_artifact_serializes_deterministically(self):
        """12: Artefato serializa e desserializa em JSON sem perda de campos."""
        runner = FakeModelRunner(custom_responses={"LEAN_FIRST_PASS": self.default_first_pass})
        service = IdeaEvolutionService(runner=runner, runs_dir=self.runs_dir)

        resp = service.evolve_idea(self.sample_idea)
        art = resp.artifact

        json_str = art.model_dump_json(indent=2)
        reloaded = EvolutionArtifact.model_validate_json(json_str)

        self.assertEqual(art.artifact_id, reloaded.artifact_id)
        self.assertEqual(art.refined_idea, reloaded.refined_idea)
        self.assertEqual(len(art.critique), len(reloaded.critique))

    def test_13_artifact_schema_version_exists(self):
        """13: Versão canônica 1.0 declarada no artefato."""
        art = EvolutionArtifact(
            artifact_id="ART-TEST",
            run_id="RUN-TEST",
            treatment_mode=TreatmentMode.LEAN_L1,
            terminal_status="COMPLETED",
            original_idea="Ideia",
            human_intent="Intenção",
            refined_idea="Ideia refinada",
        )
        self.assertEqual(art.schema_version, "1.0")

    def test_14_no_model_call_occurs_during_mapping(self):
        """14: Mapper executa sem qualquer chamada de modelo (custo 0)."""
        runner = FakeModelRunner(custom_responses={"LEAN_FIRST_PASS": self.default_first_pass})
        service = IdeaEvolutionService(runner=runner, runs_dir=self.runs_dir)

        resp = service.evolve_idea(self.sample_idea)
        initial_calls = runner.call_counts.get("LEAN_FIRST_PASS", 0)

        # Invocação direta do mapper não altera call_counts
        art = EvolutionArtifactMapper.map_lean_result(resp.lean_result)
        after_calls = runner.call_counts.get("LEAN_FIRST_PASS", 0)

        self.assertEqual(initial_calls, after_calls)

    def test_15_condition_a_maps_without_fabricated_lean_fields(self):
        """15: Condição A mapeia sem fabricar premissas ou incertezas Lean inexistentes."""
        baseline_data = {
            "success": True,
            "parsed_output": {
                "summary": "Resumo baseline.",
                "refined_version": "Versão refinada baseline.",
                "tradeoffs": ["Tradeoff 1"],
                "next_step": "Passo 1",
            },
        }

        art = EvolutionArtifactMapper.map_baseline_result(
            baseline_data=baseline_data,
            original_idea=self.sample_idea,
            run_id="RUN-BASE-001",
        )

        self.assertEqual(art.treatment_mode, TreatmentMode.FAST_FALLBACK)
        self.assertEqual(art.refined_idea, "Versão refinada baseline.")
        self.assertEqual(art.assumptions, [])     # Não fabricado
        self.assertEqual(art.uncertainties, [])   # Não fabricado
        self.assertEqual(art.what_changed, [])    # Não fabricado
        self.assertEqual(art.candidate_possibilities, []) # Não fabricado
        self.assertIsNone(art.scientific_core_hash)

    def test_16_default_service_returns_evolution_artifact(self):
        """16: IdeaEvolutionService retorna EvolutionArtifact preenchido por padrão."""
        runner = FakeModelRunner(custom_responses={"LEAN_FIRST_PASS": self.default_first_pass})
        service = IdeaEvolutionService(runner=runner, runs_dir=self.runs_dir)

        resp = service.evolve_idea(self.sample_idea)

        self.assertIsNotNone(resp.artifact)
        self.assertIsInstance(resp.artifact, EvolutionArtifact)

    def test_17_condition_b_remains_non_default(self):
        """17: Condição B permanece estritamente não-padrão."""
        service = IdeaEvolutionService(runner=FakeModelRunner(), runs_dir=self.runs_dir)
        self.assertNotEqual(service.default_treatment, TreatmentMode.SUSPENDED_DEEP_LOOP)

    def test_18_invalid_artifact_invariants_fail_deterministically(self):
        """18: Invariantes do artefato falham deterministicamente quando violadas."""
        # 1. Ideia original vazia
        with self.assertRaises(ValueError):
            EvolutionArtifact(
                artifact_id="ART-FAIL-1",
                run_id="RUN-FAIL",
                treatment_mode=TreatmentMode.LEAN_L1,
                terminal_status="COMPLETED",
                original_idea="   ",
                human_intent="Intenção",
                refined_idea="Refinada",
            )

        # 2. Ideia refinada vazia em status COMPLETED
        with self.assertRaises(ValueError):
            EvolutionArtifact(
                artifact_id="ART-FAIL-2",
                run_id="RUN-FAIL",
                treatment_mode=TreatmentMode.LEAN_L1,
                terminal_status="COMPLETED_DIRECT_ONE_PASS",
                original_idea="Ideia válida",
                human_intent="Intenção",
                refined_idea="",
            )

        # 3. Spoofing de autoridade em CandidatePossibility
        with self.assertRaises(ValueError):
            CandidatePossibility(
                mechanism="Mecanismo inventado",
                authority_basis=PromotionAuthorityBasis.USER_EXPLICIT,
            )

    def test_19_secrets_and_api_keys_not_represented(self):
        """19: Chaves de API, senhas ou tokens secretos não aparecem no artefato."""
        runner = FakeModelRunner(custom_responses={"LEAN_FIRST_PASS": self.default_first_pass})
        service = IdeaEvolutionService(runner=runner, runs_dir=self.runs_dir)

        resp = service.evolve_idea(self.sample_idea)
        json_dump = resp.artifact.model_dump_json()

        self.assertNotIn("csk-", json_dump)
        self.assertNotIn("gsk_", json_dump)
        self.assertNotIn("sk-", json_dump)
        self.assertNotIn("api_key", json_dump)
        self.assertNotIn("authorization", json_dump.lower())

    def test_20_scientific_core_hash_remains_unchanged(self):
        """20: Hash SHA-256 do núcleo científico Lean L1 permanece 100% inalterado."""
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
