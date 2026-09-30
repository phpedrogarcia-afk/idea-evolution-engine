"""RQ-11 regression tests for unsupported model-generated numeric criteria."""

import re

from src.idea_evolution.artifacts.evolution_artifact import (
    CandidatePossibility,
    EvolutionArtifact,
    FROZEN_LEAN_CORE_HASH,
    FROZEN_LEAN_CORE_HASH_RQ11,
    FROZEN_LEAN_CORE_HASH_V1_1,
    TreatmentMode,
)
from src.idea_evolution.artifacts.mapper import EvolutionArtifactMapper
from src.idea_evolution.domain.decision_relevance import (
    FalsificationCriterion,
    FalsePrecisionGuard,
    IdeaStage,
    MetricEvidenceBasis,
    NextActionArbitrationPolicy,
)
from src.idea_evolution.domain.early_epistemic_gate import (
    EarlyEpistemicGate,
    GateAuthority,
    GateOutcome,
    LeanCandidateMechanism,
    LeanFirstPassOutput,
)
from src.idea_evolution.domain.epistemic_contracts import SourceAnchor
from src.idea_evolution.domain.state import PromotionAuthorityBasis
from src.idea_evolution.providers.fake import FakeModelRunner
from src.idea_evolution.orchestration.lean_loop import LeanLoopRunner
from src.idea_evolution.rendering.human_result import HumanResultRenderer


PROVISIONAL_MARKER = "PROVISIONAL_HEURISTIC"
PRE_RQ11_V1_1_CORE_HASH = "3fa70e0ede15888ee5650fa08572508748eef1462de0a8bd01aa4a66a58b151f"


def qualify(text, *, source_text="", evidence_basis=None):
    return FalsePrecisionGuard.qualify_quantitative_decision_text(
        text,
        source_text=source_text,
        evidence_basis=evidence_basis,
    )


def case_e_runner(tmp_path):
    source = (
        "Estou desenvolvendo uma plataforma para aprender inglês online para adultos; "
        "quero avaliar sinais de fadiga por digitação e tom de áudio sem gravar muito conteúdo."
    )
    response = {
        "interpreted_problem": "Detectar sinais de fadiga em atividades de aprendizagem de inglês.",
        "human_intent": "Avaliar sinais de fadiga sem armazenar áudio excessivo.",
        "primary_mechanism": {
            "mechanism": "Analisar velocidade de digitação e tom do áudio.",
        },
        "proposed_next_action": "Investigar a viabilidade de um piloto com consentimento explícito.",
        "action_authority": {"basis": "MODEL_HYPOTHESIS"},
        "idea_stage": "DISCOVERY",
        "falsification_criteria": [
            {
                "hypothesis": "Digitação e tom de áudio correlacionam-se com fadiga autorrelatada.",
                "what_would_kill_it": (
                    "Nenhuma correlação estatisticamente significativa em estudo piloto com N≥30 usuários."
                ),
                "lowest_cost_discriminating_test": (
                    "Estudo de 1–2 semanas com 30 participantes, comparando as métricas com escalas de fadiga."
                ),
                # Deliberately untrusted model self-attestation must not be accepted.
                "quantitative_basis": "MEASURED",
            },
            {
                "hypothesis": "Usuários adultos consentirão em gravar áudio curto sem armazená-lo.",
                "what_would_kill_it": "Taxa de consentimento inferior a 30% nas entrevistas iniciais.",
                "lowest_cost_discriminating_test": (
                    "Questionário em entrevistas de 10–15 minutos com 20 potenciais usuários."
                ),
            },
        ],
    }
    model = FakeModelRunner(custom_responses={"LEAN_FIRST_PASS": response})
    result = LeanLoopRunner(runner=model, runs_dir=tmp_path).run(
        source,
        run_id="RUN-RQ11-CASE-E",
    )
    return source, result


def test_unsupported_numeric_kill_threshold_stays_provisional():
    qualified, changed = qualify(
        "A hipótese cairia se o piloto N≥30 usuários não mostrasse correlação."
    )

    assert changed is True
    assert "N≥30 usuários" in qualified
    assert PROVISIONAL_MARKER in qualified
    assert "não é um corte validado" in qualified.lower()


def test_unsupported_numeric_continue_threshold_stays_provisional():
    qualified, changed = qualify("Continuar somente se a conversão superar 7%.")

    assert changed is True
    assert "7%" in qualified
    assert PROVISIONAL_MARKER in qualified


def test_unsupported_percentage_is_not_rendered_as_fact():
    qualified, changed = qualify("A taxa abaixo de 30% derrubaria a hipótese.")

    assert changed is True
    assert "30%" in qualified
    assert PROVISIONAL_MARKER in qualified
    assert "sem vínculo textual" in qualified


def test_user_explicit_threshold_is_preserved_without_downgrade():
    source = "Abandonar o piloto se a taxa de consentimento ficar abaixo de 30%."
    claim = "Abandonar o piloto se a taxa de consentimento ficar abaixo de 30%."

    qualified, changed = qualify(claim, source_text=source)

    assert changed is False
    assert qualified == claim
    assert PROVISIONAL_MARKER not in qualified


def test_same_number_from_unrelated_source_does_not_authorize_new_threshold():
    source = "A taxa de conversão observada atualmente é 30%."
    claim = "Abandonar se a taxa de consentimento atingir 30%."

    qualified, changed = qualify(claim, source_text=source)

    assert changed is True
    assert "30%" in qualified
    assert PROVISIONAL_MARKER in qualified


def test_evidence_backed_number_is_preserved():
    claim = "O benchmark mediu latência de 50 ms."

    qualified, changed = qualify(claim, evidence_basis=MetricEvidenceBasis.MEASURED)

    assert changed is False
    assert qualified == claim


def test_deterministic_arithmetic_is_preserved():
    claim = "Com receita 1000 e custo 800, a margem calculada é 20%."

    qualified, changed = qualify(
        claim,
        evidence_basis=MetricEvidenceBasis.DETERMINISTIC_CALCULATION,
    )

    assert changed is False
    assert qualified == claim


def test_provisional_numeric_heuristic_is_allowed_but_labeled():
    qualified, changed = qualify(
        "Como hipótese operacional, testar 7% como limiar inicial.",
        evidence_basis=MetricEvidenceBasis.EXPLICIT_HYPOTHESIS,
    )

    assert changed is True
    assert "7%" in qualified
    assert PROVISIONAL_MARKER in qualified


def test_case_e_runner_qualifies_every_unsupported_numeric_decision_text(tmp_path):
    _, result = case_e_runner(tmp_path)

    assert result.gate_result.outcome == GateOutcome.RETURN_NOW
    rendered = result.final_markdown
    provisional_notes = re.findall(r"\[PROVISIONAL_HEURISTIC[^\]]+\]", rendered)
    assert len(provisional_notes) >= 4
    qualified_values = " ".join(provisional_notes)
    for value in (
        "N≥30 usuários",
        "1–2 semanas",
        "30 participantes",
        "30%",
        "10–15 minutos",
        "20 potenciais usuários",
    ):
        assert value in qualified_values
    assert "N≥30 usuários" in rendered
    assert "1–2 semanas" in rendered
    assert "inferior a 30%" in rendered
    assert "10–15 minutos" in rendered
    assert "20 potenciais usuários" in rendered

    artifact = EvolutionArtifactMapper.map_lean_result(result)
    assert PROVISIONAL_MARKER in artifact.recommended_next_action_support_ref


def test_provisional_kill_threshold_does_not_trigger_gate_or_auto_abandonment():
    source = "Explorar uma plataforma de aprendizagem de inglês com cuidado de privacidade."
    criterion = FalsificationCriterion(
        hypothesis="O áudio curto ajuda a identificar fadiga.",
        what_would_kill_it="Abandonar se consentimento ficar abaixo de 30%.",
        lowest_cost_discriminating_test="Medir consentimento em um piloto pequeno.",
    )
    criterion.what_would_kill_it, _ = qualify(criterion.what_would_kill_it, source_text=source)
    first_pass = LeanFirstPassOutput(
        interpreted_problem="Avaliar aprendizagem sem coleta excessiva.",
        human_intent="Avaliar sinais de fadiga.",
        primary_mechanism=LeanCandidateMechanism(mechanism="Áudio curto", claimed_basis=PromotionAuthorityBasis.MODEL_HYPOTHESIS),
        proposed_next_action="Investigar consentimento antes de decidir.",
        action_authority=GateAuthority(basis=PromotionAuthorityBasis.MODEL_HYPOTHESIS),
        idea_stage=IdeaStage.DISCOVERY,
        falsification_criteria=[criterion],
    )

    result = EarlyEpistemicGate.evaluate(SourceAnchor.create_human_input_anchor(source), first_pass)

    assert result.outcome == GateOutcome.RETURN_NOW
    assert "30%" in criterion.what_would_kill_it
    assert PROVISIONAL_MARKER in criterion.what_would_kill_it
    assert "abandonar" not in result.explanation.lower()


def test_provisional_continue_threshold_does_not_authorize_next_action():
    claim = "Continuar somente se mais de 70% dos usuários aceitarem."
    qualified, changed = qualify(claim)
    action, _ = NextActionArbitrationPolicy.arbitrate(
        first_pass_next_action=qualified,
        escalation_candidate_next_action=None,
        stage=IdeaStage.DISCOVERY,
        original_idea="Ideia em descoberta.",
        first_pass_action_basis=PromotionAuthorityBasis.MODEL_HYPOTHESIS,
        first_pass_action_gate_eligible=False,
    )

    assert changed is True
    assert PROVISIONAL_MARKER in action
    assert "70%" in action


def test_rq09_unverified_claim_still_renders_as_hypothesis():
    artifact = EvolutionArtifact(
        artifact_id="ART-RQ11-RQ09",
        run_id="RUN-RQ11-RQ09",
        treatment_mode=TreatmentMode.LEAN_L1,
        terminal_status="COMPLETED_DIRECT_ONE_PASS",
        original_idea="Uma plataforma simples para aprender idiomas.",
        human_intent="Avaliar aprendizagem de idiomas.",
        refined_idea="Uma plataforma simples para aprender idiomas.",
        candidate_possibilities=[
            CandidatePossibility(
                mechanism="A solução poderia superar concorrentes em 20%.",
                authority_basis=PromotionAuthorityBasis.MODEL_HYPOTHESIS,
            )
        ],
    )

    rendered = HumanResultRenderer.render(artifact)

    assert "Hipótese do sistema" in rendered
    assert "fatos estabelecidos" in rendered
    assert "superar concorrentes em 20%" in rendered


def test_rq11_core_identity_preserves_historical_v1_1_hash():
    assert FROZEN_LEAN_CORE_HASH_V1_1 == PRE_RQ11_V1_1_CORE_HASH
    assert FROZEN_LEAN_CORE_HASH_RQ11 == FROZEN_LEAN_CORE_HASH
    assert FROZEN_LEAN_CORE_HASH_RQ11 != FROZEN_LEAN_CORE_HASH_V1_1
