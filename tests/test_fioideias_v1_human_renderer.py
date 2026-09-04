"""
tests/test_fioideias_v1_human_renderer.py
Suíte de Testes Determinísticos para o HumanResultRenderer (M06 P6).

Valida apresentação humana limpa, preservação ontológica, supressão de termos
internos de laboratório, formato Markdown compatível, integração com a CLI e
invariância criptográfica estrita do núcleo científico congelado.
"""

from __future__ import annotations

import io
import json
import hashlib
import tempfile
import unittest
import contextlib
from pathlib import Path

from src.idea_evolution.artifacts.evolution_artifact import (
    EvolutionArtifact,
    TreatmentMode,
    CritiqueItem,
    CandidatePossibility,
    FROZEN_LEAN_CORE_HASH,
)
from src.idea_evolution.domain.state import PromotionAuthorityBasis, OntologyState
from src.idea_evolution.rendering.human_result import (
    HumanResultRenderer,
    render_human_result,
)
from src.idea_evolution.cli.main import main
from src.idea_evolution.providers.fake import FakeModelRunner


import shutil

class TestFioIdeiasV1HumanRendererP6(unittest.TestCase):
    """Testes determinísticos do HumanResultRenderer sob a missão M06 P6."""

    def setUp(self):
        self.sample_idea = "Criar um sistema simples de rodízio de tarefas diárias em uma cafeteria de 3 pessoas."
        self.temp_dir = Path(tempfile.mkdtemp(prefix="iee_renderer_p6_"))
        self.default_first_pass = {
            "interpreted_problem": "Cafeteria com 3 funcionários precisa de escala justa e sem atrito.",
            "human_intent": "Distribuir tarefas diárias de cafeteria de forma equitativa.",
            "primary_mechanism": {
                "mechanism": "Quadro físico com cartões magnéticos rotativos",
                "is_explicit_in_source": False,
                "claimed_basis": "MODEL_HYPOTHESIS",
                "justification": "Solução prática de baixo atrito físico.",
                "tradeoffs": ["Exige disciplina presencial diária"],
            },
            "competing_alternatives": [],
            "key_assumptions": ["Funcionários comparecem nos horários estabelecidos"],
            "material_ambiguities": [],
            "material_vulnerabilities": [],
            "remaining_uncertainties": ["Adesão dos funcionários ao quadro"],
            "requires_human_normative_choice": False,
            "proposed_next_action": "Testar com cartões de papel durante 1 semana",
        }

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _create_fake_runner(self, custom_responses=None):
        resp = {"LEAN_FIRST_PASS": self.default_first_pass}
        if custom_responses:
            resp.update(custom_responses)
        return FakeModelRunner(custom_responses=resp)

    def _create_direct_completion_artifact(self) -> EvolutionArtifact:
        return EvolutionArtifact(
            artifact_id="ART-DIRECT-001",
            run_id="RUN-DIRECT-001",
            treatment_mode=TreatmentMode.LEAN_L1,
            terminal_status="COMPLETED_DIRECT_ONE_PASS",
            original_idea=self.sample_idea,
            original_idea_authority=PromotionAuthorityBasis.USER_EXPLICIT,
            human_intent="Distribuir tarefas diárias de cafeteria de forma equitativa.",
            intent_provenance=PromotionAuthorityBasis.VALID_USER_DERIVATION,
            refined_idea="Quadro físico visual com cartões rotativos magnéticos para cada turno.",
            refined_idea_authority=PromotionAuthorityBasis.MODEL_HYPOTHESIS,
            what_changed=["Substituição de sistema abstrato por artefato físico visual."],
            assumptions=["Funcionários comparecem nos horários estabelecidos."],
            assumptions_authority=PromotionAuthorityBasis.MODEL_HYPOTHESIS,
            uncertainties=["Adesão dos funcionários ao quadro físico."],
            recommended_next_action="Testar com protótipo de papel durante 1 semana.",
            human_decision_required=False,
            model_name="fake-model",
            provider="fake",
            total_model_calls=1,
        )

    def _create_focused_escalation_artifact(self) -> EvolutionArtifact:
        return EvolutionArtifact(
            artifact_id="ART-ESCALATED-001",
            run_id="RUN-ESCALATED-001",
            treatment_mode=TreatmentMode.LEAN_L1,
            terminal_status="COMPLETED_WITH_FOCUSED_ESCALATION",
            original_idea=self.sample_idea,
            original_idea_authority=PromotionAuthorityBasis.USER_EXPLICIT,
            human_intent="Distribuir tarefas diárias de cafeteria de forma equitativa.",
            intent_provenance=PromotionAuthorityBasis.VALID_USER_DERIVATION,
            refined_idea="Quadro magnético por turnos com matriz de competências compartilhada.",
            refined_idea_authority=PromotionAuthorityBasis.MODEL_HYPOTHESIS,
            what_changed=[
                "Inclusão de matriz de competências.",
                "Divisão explícita de horários de pico.",
            ],
            critique=[
                CritiqueItem(
                    vulnerability="Sobrecarga do barista experiente em horários de pico.",
                    severity="HIGH",
                    why_it_matters="Pode gerar atrito e atraso no atendimento aos clientes.",
                    affected_aspect="Operação matinal",
                    authority_basis=PromotionAuthorityBasis.MODEL_HYPOTHESIS,
                ),
                CritiqueItem(
                    vulnerability="Desgaste físico das etiquetas magnéticas.",
                    severity="LOW",
                    why_it_matters="Custo marginal de reposição.",
                    affected_aspect="Material",
                    authority_basis=PromotionAuthorityBasis.MODEL_HYPOTHESIS,
                ),
            ],
            assumptions=[
                "Existe rotatividade entre atendimento e preparo.",
                "Três funcionários trabalham simultaneamente.",
            ],
            uncertainties=[
                "Velocidade de aprendizado de funcionários novos.",
            ],
            candidate_possibilities=[
                CandidatePossibility(
                    mechanism="Checklist digital em tablet compartilhado",
                    authority_basis=PromotionAuthorityBasis.MODEL_HYPOTHESIS,
                    ontology_state=OntologyState.CANDIDATE,
                    justification="Reduz atrito visual no balcão.",
                    tradeoffs=["Requer hardware no balcão", "Risco de molhar a tela"],
                )
            ],
            recommended_next_action="Validar matriz de competências com o gerente da cafeteria.",
            human_decision_required=False,
            total_model_calls=2,
        )

    # ---------------------------------------------------------------------------
    # Testes 1 a 3: Formatos e Desfechos de Domínio
    # ---------------------------------------------------------------------------

    def test_01_direct_completion_renders_clean_markdown(self):
        """1: Renderização de conclusão direta do Lean L1 produz Markdown limpo e estruturado."""
        art = self._create_direct_completion_artifact()
        rendered = HumanResultRenderer.render(art)

        self.assertIn("# FIOIDEIAS V1 — Maturação de Ideia", rendered)
        self.assertIn("## Ideia Original:", rendered)
        self.assertIn(self.sample_idea, rendered)
        self.assertIn("## Ideia Refinada (Proposta pelo Sistema)", rendered)
        self.assertIn("Quadro físico visual com cartões rotativos", rendered)
        self.assertIn("## Intenção Identificada", rendered)
        self.assertIn("## Premissas", rendered)
        self.assertIn("## Incertezas Mapeadas", rendered)
        self.assertIn("## Próximo Passo Recomendado", rendered)

    def test_02_focused_escalation_renders_critiques_and_candidates(self):
        """2: Renderização de escalação focada exibe críticas com severidade e possibilidades propostas."""
        art = self._create_focused_escalation_artifact()
        rendered = HumanResultRenderer.render(art)

        self.assertIn("## Pontos de Atenção e Críticas", rendered)
        self.assertIn("[Severidade Alta]", rendered)
        self.assertIn("Sobrecarga do barista experiente", rendered)
        self.assertIn("*Impacto:* Pode gerar atrito", rendered)
        self.assertIn("## Possibilidades e Alternativas", rendered)
        self.assertIn("Checklist digital em tablet compartilhado", rendered)
        self.assertIn("*Compensações (Trade-offs):*", rendered)

    def test_03_human_decision_required_renders_as_valid_state_not_error(self):
        """3: HUMAN_DECISION_REQUIRED é apresentado como estado deliberativo válido, nunca como erro ou crash."""
        art = self._create_direct_completion_artifact()
        art.terminal_status = "HUMAN_DECISION_REQUIRED"
        art.human_decision_required = True
        art.human_decision_description = "Escolher entre rodízio estritamente igualitário ou baseado em competência técnica."

        rendered = HumanResultRenderer.render(art)

        self.assertIn("## Decisão Humana Necessária (BIFURCAÇÃO NORMATIVA DETECTADA)", rendered)
        self.assertIn("Esta ideia exige uma decisão humana soberana para prosseguir.", rendered)
        self.assertIn("Escolher entre rodízio estritamente igualitário", rendered)
        # NUNCA deve ser rotulado como falha ou erro
        self.assertNotIn("ERROR", rendered)
        self.assertNotIn("FAILURE", rendered)
        self.assertNotIn("CRASH", rendered)
        self.assertNotIn("FAILED", rendered)

    # ---------------------------------------------------------------------------
    # Testes 4 a 10: Preservação de Autoridade e Honestidade Epistêmica
    # ---------------------------------------------------------------------------

    def test_04_original_idea_appears_unchanged_and_faithful(self):
        """4: A ideia original é apresentada na íntegra sem truncamento ou normalização silenciosa."""
        art = self._create_direct_completion_artifact()
        rendered = HumanResultRenderer.render(art)
        self.assertIn(self.sample_idea, rendered)

    def test_05_refined_idea_presented_as_system_proposal(self):
        """5: A ideia refinada é explicitamente enquadrada como proposta pelo sistema, não fato consumado."""
        art = self._create_direct_completion_artifact()
        rendered = HumanResultRenderer.render(art)
        self.assertIn("## Ideia Refinada (Proposta pelo Sistema)", rendered)
        self.assertIn("- **Mecanismo Proposto:**", rendered)

    def test_06_derived_intent_not_worded_as_explicit_user_statement(self):
        """6: Intenção derivada pelo sistema (VALID_USER_DERIVATION) não finge ser declaração direta do usuário."""
        art = self._create_direct_completion_artifact()
        rendered = HumanResultRenderer.render(art)
        # Não pode alegar que o usuário disse expressamente isso
        self.assertNotIn("Você disse que sua intenção é", rendered)
        self.assertNotIn("Intenção declarada por você:", rendered)
        self.assertIn("Leitura da intenção (identificada a partir da ideia):", rendered)

    def test_06b_user_explicit_intent_worded_correctly(self):
        """6b: Intenção comprovadamente explícita (USER_EXPLICIT) usa formulação de declaração direta."""
        art = self._create_direct_completion_artifact()
        # Modificar autoridade da intenção para USER_EXPLICIT com texto presente na ideia
        art.human_intent = "sistema simples de rodízio"
        art.intent_provenance = PromotionAuthorityBasis.USER_EXPLICIT
        rendered = HumanResultRenderer.render(art)
        self.assertIn("Intenção declarada por você:", rendered)

    def test_07_assumptions_visibly_remain_assumptions(self):
        """7: Premissas são explicitamente rotuladas como suposições que requerem validação empírica."""
        art = self._create_direct_completion_artifact()
        rendered = HumanResultRenderer.render(art)
        self.assertIn("## Premissas", rendered)
        self.assertIn("As seguintes premissas foram assumidas pelo sistema e requerem validação empírica:", rendered)
        self.assertIn("Funcionários comparecem nos horários estabelecidos", rendered)

    def test_08_uncertainties_visibly_remain_uncertainties(self):
        """8: Incertezas são apresentadas com destaque e não são mascaradas pela estética do produto."""
        art = self._create_direct_completion_artifact()
        rendered = HumanResultRenderer.render(art)
        self.assertIn("## Incertezas Mapeadas", rendered)
        self.assertIn("Adesão dos funcionários ao quadro físico", rendered)

    def test_09_model_candidates_visibly_remain_possibilities(self):
        """9: Candidatos gerados por modelo permanecem possibilidades exploratórias não-incorporadas ao núcleo."""
        art = self._create_focused_escalation_artifact()
        rendered = HumanResultRenderer.render(art)
        self.assertIn("## Possibilidades e Alternativas", rendered)
        self.assertIn("Alternativas e extensões exploratórias geradas pelo sistema (não incorporadas ao núcleo):", rendered)
        self.assertIn("Checklist digital em tablet compartilhado", rendered)

    def test_10_next_action_is_preserved_without_generic_fabrication(self):
        """10: O próximo passo recomendado é preservado fielmente sem geração de conselhos genéricos."""
        art = self._create_direct_completion_artifact()
        rendered = HumanResultRenderer.render(art)
        self.assertIn("## Próximo Passo Recomendado", rendered)
        self.assertIn("Testar com protótipo de papel durante 1 semana.", rendered)
        # Nenhuma dica genérica inventada
        self.assertNotIn("faça uma pesquisa de mercado", rendered.lower())

    # ---------------------------------------------------------------------------
    # Testes 11 a 15: Higiene, Omissão Limpa e Supressão de Internos
    # ---------------------------------------------------------------------------

    def test_11_empty_optional_sections_omitted_cleanly(self):
        """11: Seções opcionais vazias são omitidas sem emitir '[]' ou 'None'."""
        minimal_art = EvolutionArtifact(
            artifact_id="ART-MINIMAL-001",
            run_id="RUN-MINIMAL-001",
            treatment_mode=TreatmentMode.FAST_FALLBACK,
            terminal_status="COMPLETED_FAST_FALLBACK",
            original_idea="Idéia mínima de teste.",
            human_intent="Refinamento genérico.",
            refined_idea="Versão sintetizada da ideia.",
            critique=[],
            assumptions=[],
            uncertainties=[],
            candidate_possibilities=[],
            recommended_next_action="",
        )
        rendered = HumanResultRenderer.render(minimal_art)

        self.assertNotIn("## Pontos de Atenção e Críticas", rendered)
        self.assertNotIn("## Premissas", rendered)
        self.assertNotIn("## Incertezas Mapeadas", rendered)
        self.assertNotIn("## Possibilidades e Alternativas", rendered)
        self.assertNotIn("## Próximo Passo Recomendado", rendered)
        self.assertNotIn("[]", rendered)
        self.assertNotIn("None", rendered)

    def test_12_no_experimental_terminology_exposed(self):
        """12: Jargões de laboratório e de pesquisa experimental não vazam para a saída humana."""
        art = self._create_focused_escalation_artifact()
        rendered = HumanResultRenderer.render(art)

        forbidden_terms = [
            "Condition A",
            "Condition B",
            "Condition C",
            "Condição A",
            "Condição B",
            "Condição C",
            "M05",
            "M06",
            "RPL",
            "holdout",
            "EarlyEpistemicGate",
            "epistemic_rent",
            "decision_delta",
            "reconstruction_count",
            "SimpleLoopRunner",
            "LeanLoopRunner",
        ]
        for term in forbidden_terms:
            self.assertNotIn(term, rendered, f"Termo experimental proibido vazou: {term}")

    def test_13_no_raw_ontology_enums_exposed(self):
        """13: Nomes brutos de enums ontológicos internos não aparecem na saída de produto."""
        art = self._create_focused_escalation_artifact()
        rendered = HumanResultRenderer.render(art)

        raw_enums = [
            "MODEL_HYPOTHESIS",
            "VALID_USER_DERIVATION",
            "USER_EXPLICIT",
            "BORROWED_MODEL",
            "SYSTEM_PROPOSED_REFINEMENT",
            "OntologyState.CANDIDATE",
        ]
        for enum_name in raw_enums:
            self.assertNotIn(enum_name, rendered, f"Enum ontológico interno vazou: {enum_name}")

    def test_14_provider_telemetry_absent_in_default_human_output(self):
        """14: Contadores de tokens, contadores de chamadas e HTTP status não aparecem na saída padrão."""
        art = self._create_focused_escalation_artifact()
        rendered = HumanResultRenderer.render(art)

        self.assertNotIn("total_model_calls", rendered)
        self.assertNotIn("Chamadas de Modelo Utilizadas", rendered)
        self.assertNotIn("token_count", rendered)
        self.assertNotIn("HTTP 200", rendered)

    def test_15_secrets_absent_from_rendered_output(self):
        """15: Segredos eventualmente injetados no artefato são 100% mascarados."""
        art = self._create_direct_completion_artifact()
        art.refined_idea = "Usar chave csk-secret12345 e token Bearer topsecret_token_777 no conector."
        rendered = HumanResultRenderer.render(art)

        self.assertNotIn("csk-secret12345", rendered)
        self.assertNotIn("topsecret_token_777", rendered)
        self.assertIn("csk-***", rendered)
        self.assertIn("Bearer ***", rendered)

    # ---------------------------------------------------------------------------
    # Testes 16 a 21: Determinismo, CLI, Custo Zero e Integridade do Núcleo
    # ---------------------------------------------------------------------------

    def test_16_rendering_is_strictly_deterministic(self):
        """16: Renderizar o mesmo artefato repetidamente gera exatamente a mesma saída de caracteres."""
        art = self._create_focused_escalation_artifact()
        first_render = HumanResultRenderer.render(art)

        for _ in range(10):
            self.assertEqual(HumanResultRenderer.render(art), first_render)

    def test_17_condition_a_fast_fallback_renders_honestly(self):
        """17: Condição A (fallback rápido) renderiza sem fingir ser Lean L1 e sem erros."""
        art = EvolutionArtifact(
            artifact_id="ART-FASTA-001",
            run_id="RUN-FASTA-001",
            treatment_mode=TreatmentMode.FAST_FALLBACK,
            terminal_status="COMPLETED_FAST_FALLBACK",
            original_idea=self.sample_idea,
            human_intent="Refinamento direto da ideia.",
            refined_idea="Quadro com blocos adesivos coloridos.",
            what_changed=["Simplificação direta em passada única."],
            recommended_next_action="Validar quadro físico no balcão.",
        )
        rendered = HumanResultRenderer.render(art)
        self.assertIn("# FIOIDEIAS V1 — Maturação de Ideia", rendered)
        self.assertIn("Quadro com blocos adesivos coloridos.", rendered)
        self.assertIn("Validar quadro físico no balcão.", rendered)

    def test_18_cli_json_output_unchanged(self):
        """18: A opção --json continua retornando o EvolutionArtifact canônico serializado em JSON."""
        runner = self._create_fake_runner()
        stdout = io.StringIO()

        with contextlib.redirect_stdout(stdout):
            main(["evolve", self.sample_idea, "--json", "--runs-dir", str(self.temp_dir)], runner=runner)

        data = json.loads(stdout.getvalue())
        self.assertEqual(data["schema_version"], "1.0")
        self.assertIn("artifact_id", data)
        self.assertIn("original_idea", data)
        self.assertIn("refined_idea", data)
        # Não contém o cabeçalho Markdown de apresentação humana
        self.assertNotIn("# FIOIDEIAS V1", stdout.getvalue())

    def test_19_default_cli_invokes_human_renderer(self):
        """19: O comando padrão iee evolve invoca o HumanResultRenderer e exibe Markdown legível."""
        runner = self._create_fake_runner()
        stdout = io.StringIO()

        with contextlib.redirect_stdout(stdout):
            exit_code = main(["evolve", self.sample_idea, "--runs-dir", str(self.temp_dir)], runner=runner)

        self.assertEqual(exit_code, 0)
        output = stdout.getvalue()
        self.assertIn("# FIOIDEIAS V1 — Maturação de Ideia", output)
        self.assertIn("## Ideia Original:", output)
        self.assertIn("## Ideia Refinada (Proposta pelo Sistema)", output)
        self.assertIn("## Intenção Identificada", output)

    def test_20_renderer_makes_zero_model_calls(self):
        """20: O renderizador não invoca nenhum modelo de IA (RENDERER_MODEL_CALLS = 0)."""
        art = self._create_focused_escalation_artifact()
        initial_calls = art.total_model_calls

        _ = HumanResultRenderer.render(art)

        # O artefato e a execução não realizam chamadas adicionais
        self.assertEqual(art.total_model_calls, initial_calls)

    def test_21_scientific_core_hash_remains_strictly_unchanged(self):
        """21: Invariância inegociável do hash combinado SHA-256 do núcleo científico Lean L1."""
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

        computed_core_hash = combined.hexdigest()
        self.assertEqual(
            computed_core_hash,
            FROZEN_LEAN_CORE_HASH,
            "VIOLAÇÃO DO NÚCLEO CIENTÍFICO: Os arquivos congelados foram modificados!",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
