"""M1 typed contract, fail-closed references, and 1.0/1.1 compatibility."""

import json

import pytest
from pydantic import ValidationError

from src.idea_evolution.artifacts.evolution_artifact import (
    CandidatePossibility,
    CoverageIssue,
    CoverageIssueType,
    CoverageStatus,
    EvolutionArtifact,
    IntentImportance,
    IntentLedgerItem,
    IntentOriginType,
    IntentTreatmentStatus,
    SCHEMA_VERSION_1_0,
    SCHEMA_VERSION_1_1,
    UsefulInsight,
    OpenDecision,
)
from src.idea_evolution.artifacts.mapper import EvolutionArtifactMapper
from src.idea_evolution.domain.state import PromotionAuthorityBasis
from src.idea_evolution.rendering.human_result import HumanResultRenderer
from src.idea_evolution.service.contracts import EvolutionResponse, TreatmentMode
from src.idea_evolution.ui.server import evolution_response_to_ui_data


def item(**overrides):
    value = {
        "intent_id": "I1",
        "source_quote": "criar a base na pasta escolhida",
        "interpretation": "Preparar a estrutura inicial no destino escolhido.",
        "importance": IntentImportance.CORE_INTENT,
        "origin_type": IntentOriginType.USER_EXPLICIT,
        "treatment_in_current_form": "Preservada como requisito do produto.",
        "status": IntentTreatmentStatus.PRESERVED,
    }
    value.update(overrides)
    return value


def artifact(**overrides):
    value = {
        "artifact_id": "ART-M1",
        "run_id": "RUN-M1",
        "treatment_mode": TreatmentMode.LEAN_L1,
        "terminal_status": "COMPLETED",
        "original_idea": "Quero criar a base na pasta escolhida e começar pelo README.",
        "human_intent": "Preparar a base do projeto.",
        "refined_idea": "Uma proposta inicial.",
    }
    value.update(overrides)
    return EvolutionArtifact(**value)


def test_new_artifacts_use_1_1_safe_defaults_and_optional_insights():
    result = artifact()

    assert result.schema_version == SCHEMA_VERSION_1_1
    assert result.intent_ledger == []
    assert result.useful_insights == []
    assert result.open_decisions == []
    assert result.coverage_status == CoverageStatus.NOT_EVALUATED
    assert result.coverage_issues == []
    assert result.human_decision_required is False


def test_historical_1_0_artifact_and_candidate_load_with_safe_coverage_default():
    historical = {
        "schema_version": "1.0",
        "artifact_id": "ART-OLD",
        "run_id": "RUN-OLD",
        "treatment_mode": "LEAN_L1",
        "terminal_status": "COMPLETED",
        "original_idea": "Uma ideia antiga.",
        "human_intent": "Uma intenção antiga.",
        "refined_idea": "Uma proposta antiga.",
        "candidate_possibilities": [{"mechanism": "Possibilidade histórica"}],
    }

    loaded = EvolutionArtifact.model_validate(historical)

    assert loaded.schema_version == SCHEMA_VERSION_1_0
    assert loaded.coverage_status == CoverageStatus.NOT_EVALUATED
    assert loaded.coverage_issues == []
    assert loaded.candidate_possibilities[0].path_id is None
    assert loaded.candidate_possibilities[0].intent_ids == []


def test_legacy_1_0_cannot_claim_coverage_that_did_not_exist():
    historical = {
        "schema_version": "1.0",
        "artifact_id": "ART-OLD-COVERAGE",
        "run_id": "RUN-OLD-COVERAGE",
        "treatment_mode": "LEAN_L1",
        "terminal_status": "COMPLETED",
        "original_idea": "Uma ideia antiga.",
        "human_intent": "Uma intenção antiga.",
        "refined_idea": "Uma proposta antiga.",
        "coverage_status": "NO_BLOCKING_GAP_DETECTED",
        "coverage_issues": [{"issue_type": "STRUCTURAL_COVERAGE_FAILURE", "description": "Untrusted legacy claim."}],
    }

    loaded = EvolutionArtifact.model_validate(historical)

    assert loaded.coverage_status == CoverageStatus.NOT_EVALUATED
    assert loaded.coverage_issues == []


def test_1_1_serialization_round_trips_additive_contract_without_promoting_authority():
    result = artifact(
        intent_ledger=[item()],
        candidate_possibilities=[CandidatePossibility(
            mechanism="Uma hipótese de mecanismo.", path_id="P1", intent_ids=["I1"]
        )],
        useful_insights=[UsefulInsight(insight_id="U1", description="Um insight opcional.", related_intent_ids=["I1"])],
        open_decisions=[OpenDecision(decision_id="D1", question="Qual conteúdo inicial usar?", related_intent_ids=["I1"])],
        uncertainties=["Qual conteúdo inicial usar?"],
        recommended_next_action_target_uncertainty="Qual conteúdo inicial usar?",
    )

    loaded = EvolutionArtifact.model_validate_json(result.model_dump_json())

    assert loaded.schema_version == SCHEMA_VERSION_1_1
    assert loaded.intent_ledger[0].origin_type == IntentOriginType.USER_EXPLICIT
    assert loaded.candidate_possibilities[0].authority_basis == PromotionAuthorityBasis.MODEL_HYPOTHESIS
    assert loaded.candidate_possibilities[0].intent_ids == ["I1"]
    assert loaded.useful_insights[0].authority_basis == PromotionAuthorityBasis.MODEL_HYPOTHESIS
    assert loaded.open_decisions[0].decision_id == "D1"
    assert loaded.recommended_next_action_target_uncertainty == "Qual conteúdo inicial usar?"
    assert loaded.human_decision_required is False


def test_user_explicit_quote_must_be_exact_and_substring_validation_does_not_normalize():
    with pytest.raises(ValidationError, match="source_quote"):
        artifact(intent_ledger=[item(source_quote="criar a base no destino")])

    with pytest.raises(ValidationError, match="source_quote"):
        artifact(intent_ledger=[item(source_quote="criar  a base na pasta escolhida")])

    valid = artifact(intent_ledger=[item(source_quote="criar a base na pasta escolhida")])
    assert valid.intent_ledger[0].source_quote in valid.original_idea


def test_user_explicit_requires_quote_and_model_interpretation_stays_separately_typed():
    with pytest.raises(ValidationError, match="USER_EXPLICIT exige"):
        artifact(intent_ledger=[item(source_quote="")])

    interpreted = IntentLedgerItem(**item(
        origin_type=IntentOriginType.MODEL_INTERPRETATION,
        source_quote="",
        status=IntentTreatmentStatus.DEFERRED,
        treatment_in_current_form="",
    ))
    assert interpreted.origin_type == IntentOriginType.MODEL_INTERPRETATION
    with pytest.raises(ValidationError):
        IntentLedgerItem(**item(origin_type="USER_DERIVED"))


def test_duplicate_intent_ids_and_path_ids_fail():
    with pytest.raises(ValidationError, match="intent_id duplicado"):
        artifact(intent_ledger=[item(), item()])

    paths = [
        CandidatePossibility(mechanism="A", path_id="P1"),
        CandidatePossibility(mechanism="B", path_id="P1"),
    ]
    with pytest.raises(ValidationError, match="path_id duplicado"):
        artifact(candidate_possibilities=paths)


def test_candidate_path_and_other_contract_references_must_resolve():
    with pytest.raises(ValidationError, match="intent_ids desconhecidos"):
        artifact(candidate_possibilities=[CandidatePossibility(mechanism="A", path_id="P1", intent_ids=["I404"])])

    with pytest.raises(ValidationError, match="intent_ids desconhecidos"):
        artifact(useful_insights=[UsefulInsight(insight_id="U1", description="I.", related_intent_ids=["I404"])])

    with pytest.raises(ValidationError, match="intent_ids desconhecidos"):
        artifact(open_decisions=[OpenDecision(decision_id="D1", question="Q?", related_intent_ids=["I404"])])

    with pytest.raises(ValidationError, match="não existe em uncertainties"):
        artifact(recommended_next_action_target_uncertainty="Não existe")


def test_material_treatment_is_required_only_for_treated_statuses():
    with pytest.raises(ValidationError, match="treatment_in_current_form obrigatório"):
        artifact(intent_ledger=[item(status=IntentTreatmentStatus.PRESERVED, treatment_in_current_form=" ")])

    deferred = artifact(intent_ledger=[item(status=IntentTreatmentStatus.DEFERRED, treatment_in_current_form="")])
    assert deferred.intent_ledger[0].status == IntentTreatmentStatus.DEFERRED


def test_invalid_coverage_state_and_inconsistent_coverage_contents_fail():
    with pytest.raises(ValidationError, match="coverage_status"):
        artifact(coverage_status="SEMANTICALLY_CORRECT")

    issue = CoverageIssue(issue_type=CoverageIssueType.STRUCTURAL_COVERAGE_FAILURE, description="Gap estrutural.")
    with pytest.raises(ValidationError, match="NOT_EVALUATED"):
        artifact(coverage_issues=[issue])
    with pytest.raises(ValidationError, match="NO_BLOCKING_GAP_DETECTED"):
        artifact(coverage_status=CoverageStatus.NO_BLOCKING_GAP_DETECTED, coverage_issues=[issue])
    with pytest.raises(ValidationError, match="REPAIR_REQUIRED"):
        artifact(coverage_status=CoverageStatus.REPAIR_REQUIRED)


def test_conflict_status_and_issue_must_be_linked_consistently():
    conflict_item = item(status=IntentTreatmentStatus.CONFLICT_FOUND, treatment_in_current_form="Conflito exposto.")
    with pytest.raises(ValidationError, match="CONFLICT_FOUND"):
        artifact(intent_ledger=[conflict_item], coverage_status=CoverageStatus.UNRESOLVED)

    conflict_issue = CoverageIssue(issue_type=CoverageIssueType.CONFLICT_FOUND, description="Conflito.", intent_id="I1")
    valid = artifact(intent_ledger=[conflict_item], coverage_status=CoverageStatus.UNRESOLVED, coverage_issues=[conflict_issue])
    assert valid.coverage_issues[0].intent_id == "I1"

    with pytest.raises(ValidationError, match="CONFLICT_FOUND"):
        artifact(intent_ledger=[item()], coverage_status=CoverageStatus.UNRESOLVED, coverage_issues=[conflict_issue])


def test_default_mappers_do_not_fabricate_m1_content_but_emit_schema_1_1():
    mapped = EvolutionArtifactMapper.map_baseline_result(
        baseline_data={"success": True, "parsed_output": {"summary": "Resumo.", "refined_version": "Refinada."}},
        original_idea="Ideia original.",
        run_id="RUN-MAPPER-M1",
    )

    assert mapped.schema_version == SCHEMA_VERSION_1_1
    assert mapped.intent_ledger == []
    assert mapped.useful_insights == []
    assert mapped.open_decisions == []
    assert mapped.coverage_status == CoverageStatus.NOT_EVALUATED
    assert mapped.coverage_issues == []


def test_existing_renderer_and_ui_adapter_accept_1_1_without_exposing_new_fields():
    result = artifact(
        intent_ledger=[item()],
        candidate_possibilities=[CandidatePossibility(mechanism="Mecanismo", path_id="P1", intent_ids=["I1"])],
        open_decisions=[OpenDecision(decision_id="D1", question="Qual conteúdo inicial?", related_intent_ids=["I1"])],
    )
    rendered = HumanResultRenderer.render(result)
    response = EvolutionResponse(
        success=True,
        run_id=result.run_id,
        treatment_used=TreatmentMode.LEAN_L1,
        raw_idea=result.original_idea,
        terminal_status=result.terminal_status,
        artifact=result,
    )

    ui_data = evolution_response_to_ui_data(response)

    assert rendered
    assert ui_data["artifact"]["refined_idea"] == result.refined_idea
    assert "intent_ledger" not in ui_data["artifact"]
    assert "open_decisions" not in ui_data["artifact"]
    assert result.intent_ledger[0].intent_id == "I1"
