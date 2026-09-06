"""RQ-07 regression tests for anchored derivation and gate eligibility."""

from src.idea_evolution.domain.decision_relevance import (
    DecisionRelevance,
    FalsificationCriterion,
    IdeaStage,
    NextActionArbitrationPolicy,
    RiskCategory,
)
from src.idea_evolution.domain.early_epistemic_gate import (
    EarlyEpistemicGate,
    EscalationReason,
    FocusedEscalationOutput,
    GateAuthority,
    GateOutcome,
    LeanCandidateMechanism,
    LeanFirstPassOutput,
    LeanVulnerability,
)
from src.idea_evolution.domain.epistemic_contracts import SourceAnchor
from src.idea_evolution.domain.state import PromotionAuthorityBasis
from src.idea_evolution.artifacts.evolution_artifact import EvolutionArtifact, TreatmentMode
from src.idea_evolution.artifacts.mapper import EvolutionArtifactMapper
from src.idea_evolution.orchestration.lean_loop import LeanRunResult


def first_pass(**overrides) -> LeanFirstPassOutput:
    data = {
        "interpreted_problem": "Investigar uma ideia conceitual.",
        "human_intent": "Compreender a ideia antes de decidir ou construir.",
        "primary_mechanism": LeanCandidateMechanism(
            mechanism="Possibilidade exploratória",
            claimed_basis=PromotionAuthorityBasis.MODEL_HYPOTHESIS,
        ),
        "competing_alternatives": [],
        "key_assumptions": [],
        "material_ambiguities": [],
        "material_vulnerabilities": [],
        "remaining_uncertainties": [],
        "requires_human_normative_choice": False,
        "human_choice_description": "",
        "proposed_next_action": "",
        "idea_stage": IdeaStage.DISCOVERY,
    }
    data.update(overrides)
    return LeanFirstPassOutput(**data)


def evaluate(source: str, output: LeanFirstPassOutput):
    return EarlyEpistemicGate.evaluate(SourceAnchor.create_human_input_anchor(source), output)


def test_model_hypothesis_alone_cannot_trigger_normative_bifurcation():
    output = first_pass(
        requires_human_normative_choice=True,
        human_choice_description="Humanos devem escolher qual arquitetura adotar.",
        normative_authority=GateAuthority(basis=PromotionAuthorityBasis.MODEL_HYPOTHESIS),
    )

    result = evaluate("Explorar modos de representar memória.", output)

    assert result.outcome != GateOutcome.REQUEST_HUMAN_DECISION
    assert output.normative_gate_eligible is False


def test_model_hypothesis_alone_cannot_be_material_vulnerability():
    vulnerability = LeanVulnerability(
        vulnerability="Usuários abandonarão o produto imediatamente",
        why_it_matters="A hipótese de valor falharia.",
        severity="HIGH",
        category=RiskCategory.USER_BEHAVIOR,
        authority=GateAuthority(basis=PromotionAuthorityBasis.MODEL_HYPOTHESIS),
    )

    result = evaluate("Uma ideia de agenda comunitária.", first_pass(material_vulnerabilities=[vulnerability]))

    assert result.escalation_reason != EscalationReason.MATERIAL_VULNERABILITY
    assert vulnerability.gate_eligible is False


def test_input_contradiction_cannot_acquire_derived_authority():
    source = "A Testemunha recebe múltiplas fontes externas e também realiza auto-observação."
    vulnerability = LeanVulnerability(
        vulnerability="Dependência exclusiva em auto-observação",
        why_it_matters="A visão ficaria limitada.",
        severity="HIGH",
        category=RiskCategory.PRODUCT,
        authority=GateAuthority(
            basis=PromotionAuthorityBasis.VALID_USER_DERIVATION,
            support_ref="múltiplas fontes externas e também realiza auto-observação",
            derivation="A conclusão deveria decorrer estritamente da arquitetura descrita.",
        ),
    )

    result = evaluate(source, first_pass(material_vulnerabilities=[vulnerability]))

    assert result.escalation_reason != EscalationReason.MATERIAL_VULNERABILITY
    assert vulnerability.authority.basis == PromotionAuthorityBasis.MODEL_HYPOTHESIS
    assert any("INPUT_CONTRADICTION" in claim for claim in result.ineligible_gate_claims)


def test_user_explicit_can_still_trigger_legitimate_material_gate():
    source = "Existe risco material de perda permanente de dados e quero avaliar esse risco agora."
    vulnerability = LeanVulnerability(
        vulnerability="risco material de perda permanente de dados",
        why_it_matters="A fonte humana declarou o risco como material.",
        severity="HIGH",
        category=RiskCategory.PRODUCT,
        authority=GateAuthority(
            basis=PromotionAuthorityBasis.USER_EXPLICIT,
            support_ref="risco material de perda permanente de dados",
        ),
    )

    result = evaluate(source, first_pass(material_vulnerabilities=[vulnerability]))

    assert result.escalation_reason == EscalationReason.MATERIAL_VULNERABILITY
    assert vulnerability.gate_eligible is True


def test_valid_user_derivation_requires_traceable_source_support():
    source = "O responsável humano deve escolher entre priorizar renda ou diversidade regional."
    unsupported = first_pass(
        requires_human_normative_choice=True,
        human_choice_description="escolher entre priorizar renda ou diversidade regional",
        normative_authority=GateAuthority(
            basis=PromotionAuthorityBasis.VALID_USER_DERIVATION,
            derivation="A escolha normativa é necessária para definir o critério.",
        ),
    )
    supported = first_pass(
        requires_human_normative_choice=True,
        human_choice_description="escolher entre priorizar renda ou diversidade regional",
        normative_authority=GateAuthority(
            basis=PromotionAuthorityBasis.VALID_USER_DERIVATION,
            support_ref="deve escolher entre priorizar renda ou diversidade regional",
            derivation="A escolha normativa é necessária para definir o critério.",
        ),
    )

    assert evaluate(source, unsupported).outcome != GateOutcome.REQUEST_HUMAN_DECISION
    assert evaluate(source, supported).outcome == GateOutcome.REQUEST_HUMAN_DECISION
    assert supported.normative_gate_eligible is True


def test_model_derived_severity_cannot_substitute_decision_relevance():
    vulnerability = LeanVulnerability(
        vulnerability="Falha catastrófica imaginada pelo modelo",
        why_it_matters="Foi declarada severa sem suporte.",
        severity="HIGH",
        decision_relevance=DecisionRelevance.CRITICAL_NOW,
        authority=GateAuthority(basis=PromotionAuthorityBasis.MODEL_HYPOTHESIS),
    )

    result = evaluate("Investigar uma nova forma de organizar notas.", first_pass(material_vulnerabilities=[vulnerability]))

    assert result.escalation_reason != EscalationReason.MATERIAL_VULNERABILITY
    assert vulnerability.effective_severity == "UNCONFIRMED"


def test_next_action_does_not_jump_to_implementation_with_open_uncertainty():
    action, changed = NextActionArbitrationPolicy.arbitrate(
        first_pass_next_action="Construir um protótipo completo agora",
        escalation_candidate_next_action=None,
        stage=IdeaStage.DISCOVERY,
        original_idea="Ainda não sabemos se o problema existe para usuários.",
        first_pass_action_basis=PromotionAuthorityBasis.MODEL_HYPOTHESIS,
        first_pass_action_gate_eligible=False,
        remaining_uncertainties=["Se o problema realmente ocorre para usuários"],
        falsification_criteria=[],
    )

    assert "Se o problema realmente ocorre para usuários" in action
    assert "protótipo completo" not in action
    assert changed is True


def test_model_possibilities_remain_available_without_gate_authority():
    output = first_pass(
        primary_mechanism=LeanCandidateMechanism(
            mechanism="Usar mapas espaciais como possibilidade",
            claimed_basis=PromotionAuthorityBasis.MODEL_HYPOTHESIS,
        )
    )

    result = evaluate("Quero explorar diferentes representações de ideias.", output)

    assert output.primary_mechanism.claimed_basis == PromotionAuthorityBasis.MODEL_HYPOTHESIS
    assert result.unsupported_candidate_count == 1
    assert result.authority_spoofing_detected is False
    assert result.outcome == GateOutcome.RETURN_NOW


def test_missing_anchor_degrades_claim_instead_of_fabricating_certainty():
    vulnerability = LeanVulnerability(
        vulnerability="A arquitetura exige consenso distribuído",
        why_it_matters="Seria complexo.",
        severity="HIGH",
        authority=GateAuthority(
            basis=PromotionAuthorityBasis.VALID_USER_DERIVATION,
            derivation="A arquitetura descrita exigiria necessariamente consenso.",
        ),
    )

    result = evaluate("Ferramenta simples para organizar notas locais.", first_pass(material_vulnerabilities=[vulnerability]))

    assert vulnerability.authority.basis == PromotionAuthorityBasis.MODEL_HYPOTHESIS
    assert vulnerability.gate_eligible is False
    assert result.authority_spoofing_detected is True
    assert result.unsupported_candidate_count == 2


def test_model_next_action_may_remain_only_as_explicit_evidence_needed():
    criterion = FalsificationCriterion(
        hypothesis="O problema ocorre com frequência suficiente.",
        what_would_kill_it="Nenhum usuário relata o problema.",
        lowest_cost_discriminating_test="Entrevistar usuários sobre ocorrências recentes.",
    )

    action, changed = NextActionArbitrationPolicy.arbitrate(
        first_pass_next_action="Implementar a solução",
        escalation_candidate_next_action=None,
        stage=IdeaStage.DISCOVERY,
        original_idea="Ideia ainda conceitual.",
        first_pass_action_basis=PromotionAuthorityBasis.MODEL_HYPOTHESIS,
        first_pass_action_gate_eligible=False,
        remaining_uncertainties=["Frequência real do problema"],
        falsification_criteria=[criterion],
    )

    assert action == "Entrevistar usuários sobre ocorrências recentes."
    assert changed is True


def test_english_model_implementation_action_is_replaced_by_evidence_test():
    criterion = FalsificationCriterion(
        hypothesis="The observed problem is reproducible.",
        what_would_kill_it="No controlled observation reproduces it.",
        lowest_cost_discriminating_test="Compare controlled observations with and without the condition.",
    )

    action, changed = NextActionArbitrationPolicy.arbitrate(
        first_pass_next_action="Develop a prototype engine",
        escalation_candidate_next_action=None,
        stage=IdeaStage.DISCOVERY,
        original_idea="A conceptual idea with open empirical uncertainty.",
        first_pass_action_basis=PromotionAuthorityBasis.MODEL_HYPOTHESIS,
        first_pass_action_gate_eligible=False,
        remaining_uncertainties=["Whether the observed problem is reproducible"],
        falsification_criteria=[criterion],
    )

    assert action == "Compare controlled observations with and without the condition."
    assert changed is True


def test_model_interpretation_cannot_silently_become_human_intent_derivation():
    artifact = EvolutionArtifact(
        artifact_id="ART-RQ07-INTENT",
        run_id="RUN-RQ07-INTENT",
        treatment_mode=TreatmentMode.LEAN_L1,
        terminal_status="COMPLETED_DIRECT_ONE_PASS",
        original_idea="Explorar uma forma de organizar notas.",
        human_intent="O usuário quer construir uma plataforma colaborativa.",
        refined_idea="Possível plataforma colaborativa.",
    )

    assert artifact.intent_provenance == PromotionAuthorityBasis.MODEL_HYPOTHESIS
    assert artifact.audit_provenance().is_epistemically_safe is True


def test_regression_observado_execute_prototype_action_is_replaced():
    criteria = [
        FalsificationCriterion(
            hypothesis="Contrafactuais gerados são qualitativamente distintos.",
            what_would_kill_it="As saídas são apenas paráfrases umas das outras.",
            lowest_cost_discriminating_test=(
                "Executar o protótipo com uma observação de exemplo e avaliar se surgem "
                "ao menos duas contrafactuais qualitativamente distintas."
            ),
        ),
        FalsificationCriterion(
            hypothesis="As premissas não contradizem a observação.",
            what_would_kill_it="Uma premissa contradiz um fato declarado.",
            lowest_cost_discriminating_test=(
                "Validar manualmente as premissas de cada contrafactual contra o contrato "
                "de observação em um pequeno conjunto de casos."
            ),
        ),
    ]

    action, changed = NextActionArbitrationPolicy.arbitrate(
        first_pass_next_action=(
            "Executar o protótipo com uma observação de exemplo e avaliar se surgem "
            "ao menos duas contrafactuais qualitativamente distintas."
        ),
        escalation_candidate_next_action=None,
        stage=IdeaStage.DISCOVERY,
        original_idea="Uma entidade contrafactual ainda conceitual.",
        first_pass_action_basis=PromotionAuthorityBasis.MODEL_HYPOTHESIS,
        first_pass_action_gate_eligible=False,
        remaining_uncertainties=["Se as saídas são realmente distintas"],
        falsification_criteria=criteria,
    )

    assert action.startswith("Validar manualmente as premissas")
    assert "protótipo" not in action
    assert changed is True


def test_focused_model_analysis_does_not_inherit_target_authority():
    source = "A ideia declara explicitamente a doença da busca infinita."
    vulnerability = LeanVulnerability(
        vulnerability="doença da busca infinita",
        why_it_matters="A busca precisa de condição de parada.",
        severity="HIGH",
        authority=GateAuthority(
            basis=PromotionAuthorityBasis.USER_EXPLICIT,
            support_ref="doença da busca infinita",
        ),
    )
    vulnerability.gate_eligible = True
    vulnerability.effective_severity = "HIGH"
    output = first_pass(material_vulnerabilities=[vulnerability])
    escalation = FocusedEscalationOutput(
        escalation_reason=EscalationReason.MATERIAL_VULNERABILITY,
        target_hypothesis="doença da busca infinita",
        focused_critique_or_analysis="Uma nova falha estrutural existe na camada de pressupostos.",
    )
    result = LeanRunResult(
        run_id="RUN-RQ07-FOCUSED",
        source_anchor=SourceAnchor.create_human_input_anchor(source),
        first_pass=output,
        escalation_result=escalation,
        total_model_calls=2,
        terminal_status="COMPLETED_WITH_FOCUSED_ESCALATION",
    )

    artifact = EvolutionArtifactMapper.map_lean_result(result)
    target, focused = artifact.critique

    assert target.authority_basis == PromotionAuthorityBasis.USER_EXPLICIT
    assert target.gate_eligible is True
    assert focused.authority_basis == PromotionAuthorityBasis.MODEL_HYPOTHESIS
    assert focused.severity == "UNCONFIRMED"
    assert focused.gate_eligible is False
