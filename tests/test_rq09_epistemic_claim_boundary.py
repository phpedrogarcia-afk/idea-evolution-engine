"""RQ-09 regressions for visible epistemic status of model-generated claims."""

from src.idea_evolution.artifacts.evolution_artifact import (
    CandidatePossibility,
    EvolutionArtifact,
    TreatmentMode,
)
from src.idea_evolution.domain.decision_relevance import RiskCategory
from src.idea_evolution.domain.early_epistemic_gate import (
    EarlyEpistemicGate,
    GateAuthority,
    GateOutcome,
    LeanCandidateMechanism,
    LeanFirstPassOutput,
    LeanVulnerability,
)
from src.idea_evolution.domain.epistemic_contracts import SourceAnchor
from src.idea_evolution.domain.state import OntologyState, PromotionAuthorityBasis
from src.idea_evolution.rendering.human_result import HumanResultRenderer


class TestRQ09EpistemicClaimBoundary:
    """A model candidate may be useful, but its external claims are not facts."""

    @staticmethod
    def _artifact(candidate, *, original_idea="Explorar uma ideia.", human_intent="Explorar uma ideia.", intent_basis=PromotionAuthorityBasis.VALID_USER_DERIVATION):
        return EvolutionArtifact(
            artifact_id="ART-RQ09-001",
            run_id="RUN-RQ09-001",
            treatment_mode=TreatmentMode.LEAN_L1,
            terminal_status="COMPLETED_DIRECT_ONE_PASS",
            original_idea=original_idea,
            original_idea_authority=PromotionAuthorityBasis.USER_EXPLICIT,
            human_intent=human_intent,
            intent_provenance=intent_basis,
            refined_idea="Explorar uma possibilidade nova.",
            refined_idea_authority=PromotionAuthorityBasis.MODEL_HYPOTHESIS,
            candidate_possibilities=[candidate],
        )

    @staticmethod
    def _model_candidate(mechanism, justification, tradeoffs=()):
        return CandidatePossibility(
            mechanism=mechanism,
            authority_basis=PromotionAuthorityBasis.MODEL_HYPOTHESIS,
            ontology_state=OntologyState.CANDIDATE,
            justification=justification,
            tradeoffs=list(tradeoffs),
        )

    def test_model_hypothesis_in_alternative_justification(self):
        """RQ-08 B: an app-only risk comparison remains visibly unverified."""
        justification = "Solução de baixo esforço que evita riscos de estabilidade e segurança associados a ROMs customizadas."
        tradeoff = "Dependência de permissões de apps"
        artifact = self._artifact(
            self._model_candidate(
                "Manter a ROM padrão do POCO e usar apenas aplicativos de IA instalados via Play Store.",
                justification,
                [tradeoff],
            )
        )

        rendered = HumanResultRenderer.render(artifact)

        self._assert_model_hypothesis_label(rendered)
        assert justification in rendered
        assert tradeoff in rendered

    def test_model_hypothesis_in_value_reasoning(self):
        """RQ-08 C: an unsupported user-time/value assertion is not rendered as fact."""
        justification = "Criadores costumam organizar ideias manualmente, mas o processo consome tempo e depende da criatividade individual."
        artifact = self._artifact(
            self._model_candidate(
                "Organização manual de ideias em planilhas ou documentos",
                justification,
                ["Consome tempo", "Depende de criatividade individual"],
            )
        )

        rendered = HumanResultRenderer.render(artifact)

        self._assert_model_hypothesis_label(rendered)
        assert justification in rendered

    def test_technical_external_claim_without_evidence(self):
        """Unsupported compatibility claims remain candidate hypotheses."""
        claim = "Há uma ROM estável compatível com o POCO M3 Pro 5G e pronta para receber módulos de IA."
        rendered = HumanResultRenderer.render(
            self._artifact(self._model_candidate("Adaptar uma ROM compatível ao dispositivo", claim))
        )

        self._assert_model_hypothesis_label(rendered)
        assert claim in rendered

    def test_user_explicit_fact_preserved(self):
        """Explicit source text stays verbatim and keeps its human-declared label."""
        source = "Criar uma ROM personalizada para o POCO M3 Pro 5G."
        rendered = HumanResultRenderer.render(
            self._artifact(
                self._model_candidate("Uma proposta exploratória", "Hipótese de teste."),
                original_idea=source,
                human_intent=source,
                intent_basis=PromotionAuthorityBasis.USER_EXPLICIT,
            )
        )

        assert source in rendered
        assert "Intenção declarada por você:" in rendered

    def test_valid_derivation_preserved(self):
        """A derived interpretation remains labeled as an interpretation, not downgraded."""
        derived = "Apoiar criadores a organizar ideias de conteúdo."
        rendered = HumanResultRenderer.render(
            self._artifact(
                self._model_candidate("Explorar um painel de ideias", "Possibilidade para testar."),
                original_idea="Quero organizar ideias de conteúdo para criadores.",
                human_intent=derived,
                intent_basis=PromotionAuthorityBasis.VALID_USER_DERIVATION,
            )
        )

        assert derived in rendered
        assert "Leitura da inten" in rendered
        assert "Intenção declarada por você:" not in rendered

    def test_creative_hypothesis_allowed(self):
        """A status label must preserve, not suppress, a novel useful possibility."""
        novel = "Um launcher que sugere ações de IA a partir do contexto local do usuário."
        rendered = HumanResultRenderer.render(
            self._artifact(self._model_candidate(novel, "Possibilidade criativa para investigação."))
        )

        assert novel in rendered
        self._assert_model_hypothesis_label(rendered)

    def test_rq07_gate_invariants(self):
        """Model hypotheses remain ineligible for normative and vulnerability gates."""
        source = "Explorar uma ideia conceitual sem escolher uma arquitetura ainda."
        vulnerability = LeanVulnerability(
            vulnerability="O produto certamente falhará com usuários.",
            why_it_matters="A hipótese de valor poderia falhar.",
            severity="HIGH",
            category=RiskCategory.USER_BEHAVIOR,
            authority=GateAuthority(basis=PromotionAuthorityBasis.MODEL_HYPOTHESIS),
        )
        first_pass = LeanFirstPassOutput(
            interpreted_problem="Explorar uma ideia.",
            human_intent="Compreender a ideia antes de decidir.",
            primary_mechanism=LeanCandidateMechanism(
                mechanism="Uma possibilidade gerada pelo modelo",
                claimed_basis=PromotionAuthorityBasis.MODEL_HYPOTHESIS,
            ),
            material_vulnerabilities=[vulnerability],
            requires_human_normative_choice=True,
            human_choice_description="Escolher uma arquitetura.",
            normative_authority=GateAuthority(basis=PromotionAuthorityBasis.MODEL_HYPOTHESIS),
            proposed_next_action="Implementar agora",
            action_authority=GateAuthority(basis=PromotionAuthorityBasis.MODEL_HYPOTHESIS),
        )

        result = EarlyEpistemicGate.evaluate(
            SourceAnchor.create_human_input_anchor(source),
            first_pass,
        )

        assert result.outcome != GateOutcome.REQUEST_HUMAN_DECISION
        assert result.escalation_reason.value != "MATERIAL_VULNERABILITY"
        assert vulnerability.gate_eligible is False
        assert first_pass.normative_gate_eligible is False
        assert first_pass.next_action_gate_eligible is False

    @staticmethod
    def _assert_model_hypothesis_label(rendered):
        assert "mecanismo, justificativa e" in rendered
        assert "fatos estabelecidos." in rendered
