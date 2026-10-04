"""M3 deterministic coverage checks; fixtures are known regressions, not blind tests."""

from copy import deepcopy
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

import pytest

_M2_FIXTURES_SPEC = spec_from_file_location(
    "_m2_known_regression_fixtures",
    Path(__file__).with_name("test_v12_m2_strong_first_pass.py"),
)
assert _M2_FIXTURES_SPEC is not None and _M2_FIXTURES_SPEC.loader is not None
_M2_FIXTURES = module_from_spec(_M2_FIXTURES_SPEC)
_M2_FIXTURES_SPEC.loader.exec_module(_M2_FIXTURES)
FIOBASE_IDEA = _M2_FIXTURES.FIOBASE_IDEA
fiobase_response = _M2_FIXTURES.fiobase_response
from src.idea_evolution.artifacts.evolution_artifact import (
    CandidatePossibility,
    CoverageIssueType,
    CoverageStatus,
    EvolutionArtifact,
    IntentImportance,
    IntentTreatmentStatus,
    OpenDecision,
    SCHEMA_VERSION_1_0,
)
from src.idea_evolution.domain.state import PromotionAuthorityBasis
from src.idea_evolution.providers.fake import FakeModelRunner
from src.idea_evolution.service.evolution_service import IdeaEvolutionService
from src.idea_evolution.service.maturation_coverage_gate import MaturationCoverageGate
from src.idea_evolution.service.contracts import TreatmentMode


SOURCE = "Criar uma base que reaproveita scars e preserve controle humano."
CORE_QUOTE = "Criar uma base"
SCARS_QUOTE = "reaproveita scars"
CONSTRAINT_QUOTE = "preserve controle humano"
TARGET_UNCERTAINTY = "Quais scars são relevantes para o novo projeto?"


def _intent(intent_id, quote, importance, *, status="PRESERVED", treatment="Tratada na forma atual."):
    return {
        "intent_id": intent_id,
        "source_quote": quote,
        "interpretation": f"Interpretação estruturada de {intent_id}.",
        "importance": importance,
        "origin_type": "USER_EXPLICIT",
        "treatment_in_current_form": treatment,
        "status": status,
    }


def _artifact(**overrides):
    value = {
        "artifact_id": "ART-M3-TEST",
        "run_id": "RUN-M3-TEST",
        "treatment_mode": TreatmentMode.LEAN_L1,
        "terminal_status": "COMPLETED_DIRECT_ONE_PASS",
        "original_idea": SOURCE,
        "human_intent": "Preparar uma base reutilizável sem retirar controle do criador.",
        "refined_idea": "Uma base consultiva reaproveita scars e permanece sob controle humano.",
        "intent_ledger": [
            _intent("I-CORE", CORE_QUOTE, "CORE_INTENT"),
            _intent("I-SCARS", SCARS_QUOTE, "MATERIAL_SUBINTENT"),
            _intent("I-CONTROL", CONSTRAINT_QUOTE, "EXPLICIT_CONSTRAINT"),
        ],
        "candidate_possibilities": [
            {
                "path_id": "PATH-001",
                "mechanism": "Uma skill consultiva prepara contexto reutilizável.",
                "intent_ids": ["I-CORE", "I-SCARS", "I-CONTROL"],
                "authority_basis": PromotionAuthorityBasis.MODEL_HYPOTHESIS,
            }
        ],
        "uncertainties": [TARGET_UNCERTAINTY],
        "recommended_next_action": "Comparar quais scars seriam relevantes.",
        "recommended_next_action_target_uncertainty": TARGET_UNCERTAINTY,
    }
    value.update(overrides)
    return EvolutionArtifact(**value)


def _with_item(artifact, intent_id, **updates):
    ledger = [
        item.model_copy(update=updates) if item.intent_id == intent_id else item
        for item in artifact.intent_ledger
    ]
    return artifact.model_copy(update={"intent_ledger": ledger})


def _service_response(idea, first_pass, tmp_path):
    # M3 only reports the initial finding; under M4, an intentionally malformed
    # offline repair response proves that the service preserves it as UNRESOLVED.
    runner = FakeModelRunner(
        custom_responses={"LEAN_FIRST_PASS": first_pass},
        should_fail_schema_stages={"MATURATION_FOCUSED_REPAIR": 1},
    )
    service = IdeaEvolutionService(runner=runner, runs_dir=tmp_path / "runs")
    response = service.evolve_idea(idea, run_id="RUN-M3-SERVICE")
    return response, runner


def test_valid_fiobase_maturation_passes_after_mapping_with_one_fake_call(tmp_path):
    response, runner = _service_response(FIOBASE_IDEA, fiobase_response(), tmp_path)

    assert response.success is True
    assert response.artifact.coverage_status == CoverageStatus.NO_BLOCKING_GAP_DETECTED
    assert response.artifact.coverage_issues == []
    assert runner.call_counts == {"LEAN_FIRST_PASS": 1}
    assert response.total_model_calls == 1


def test_material_fiobase_subintent_without_treatment_requires_repair(tmp_path):
    response_data = deepcopy(fiobase_response())
    item = next(entry for entry in response_data["intent_ledger"] if entry["intent_id"] == "I-SCARS")
    item.update(status="DEFERRED", treatment_in_current_form="")

    response, runner = _service_response(FIOBASE_IDEA, response_data, tmp_path)

    assert response.success is True
    assert response.artifact.coverage_status == CoverageStatus.UNRESOLVED
    assert any(issue.issue_type == CoverageIssueType.MATERIAL_INTENT_UNTREATED for issue in response.artifact.coverage_issues)
    assert runner.call_counts == {"LEAN_FIRST_PASS": 1, "MATURATION_FOCUSED_REPAIR": 1}
    assert response.maturation_repair.repair_attempted is True


def test_explicit_fiobase_constraint_deferred_without_exposure_requires_repair(tmp_path):
    response_data = deepcopy(fiobase_response())
    item = next(entry for entry in response_data["intent_ledger"] if entry["intent_id"] == "I-STARTUP")
    item.update(status="DEFERRED", treatment_in_current_form="")

    response, _ = _service_response(FIOBASE_IDEA, response_data, tmp_path)

    issue_types = {issue.issue_type for issue in response.artifact.coverage_issues}
    assert response.artifact.coverage_status == CoverageStatus.UNRESOLVED
    assert CoverageIssueType.EXPLICIT_CONSTRAINT_UNTREATED in issue_types
    assert CoverageIssueType.DEFERRED_ITEM_NOT_EXPOSED in issue_types


def test_hidden_provisional_modification_requires_linked_open_decision(tmp_path):
    response_data = deepcopy(fiobase_response())
    item = next(entry for entry in response_data["intent_ledger"] if entry["intent_id"] == "I-SCARS")
    item.update(status="PROVISIONALLY_MODIFIED", treatment_in_current_form="Reuso provisório sujeito a escolha posterior.")

    response, _ = _service_response(FIOBASE_IDEA, response_data, tmp_path)

    assert response.artifact.coverage_status == CoverageStatus.UNRESOLVED
    assert any(issue.issue_type == CoverageIssueType.PROVISIONAL_MODIFICATION_NOT_EXPOSED for issue in response.artifact.coverage_issues)
    assert response.artifact.human_decision_required is False


def test_explicit_conflict_is_converted_to_linked_repair_issue(tmp_path):
    response_data = deepcopy(fiobase_response())
    item = next(entry for entry in response_data["intent_ledger"] if entry["intent_id"] == "I-SCARS")
    item.update(status="CONFLICT_FOUND", treatment_in_current_form="O ledger expõe o conflito como hipótese a resolver.")

    response, runner = _service_response(FIOBASE_IDEA, response_data, tmp_path)

    assert response.artifact.coverage_status == CoverageStatus.UNRESOLVED
    assert any(
        issue.issue_type == CoverageIssueType.CONFLICT_FOUND and issue.intent_id == "I-SCARS"
        for issue in response.artifact.coverage_issues
    )
    assert runner.call_counts == {"LEAN_FIRST_PASS": 1, "MATURATION_FOCUSED_REPAIR": 1}


def test_a_linked_open_decision_exposes_provisional_intent_without_requesting_authority():
    artifact = _artifact(
        intent_ledger=[
            _intent("I-CORE", CORE_QUOTE, "CORE_INTENT"),
            _intent("I-SCARS", SCARS_QUOTE, "MATERIAL_SUBINTENT", status="PROVISIONALLY_MODIFIED"),
            _intent("I-CONTROL", CONSTRAINT_QUOTE, "EXPLICIT_CONSTRAINT"),
        ],
        open_decisions=[OpenDecision(
            decision_id="DECISION-001",
            question="O reuso de scars será obrigatório ou consultivo?",
            related_intent_ids=["I-SCARS"],
        )],
    )

    evaluated = MaturationCoverageGate.apply(artifact)

    assert evaluated.coverage_status == CoverageStatus.NO_BLOCKING_GAP_DETECTED
    assert evaluated.human_decision_required is False
    assert artifact.coverage_status == CoverageStatus.NOT_EVALUATED  # input is not mutated


def test_deferred_intent_without_linked_open_decision_is_blocking():
    artifact = _with_item(
        _artifact(),
        "I-SCARS",
        status=IntentTreatmentStatus.DEFERRED,
        treatment_in_current_form="",
    )

    evaluation = MaturationCoverageGate.evaluate(artifact)

    assert evaluation.status == CoverageStatus.REPAIR_REQUIRED
    assert {issue.issue_type for issue in evaluation.issues} >= {
        CoverageIssueType.MATERIAL_INTENT_UNTREATED,
        CoverageIssueType.DEFERRED_ITEM_NOT_EXPOSED,
    }


def test_candidate_with_unknown_intent_reference_is_blocking():
    artifact = _artifact()
    path = artifact.candidate_possibilities[0].model_copy(update={"intent_ids": ["I-UNKNOWN"]})
    artifact = artifact.model_copy(update={"candidate_possibilities": [path]})

    evaluation = MaturationCoverageGate.evaluate(artifact)

    assert evaluation.status == CoverageStatus.REPAIR_REQUIRED
    assert any(issue.issue_type == CoverageIssueType.INTENT_REFERENCE_INVALID for issue in evaluation.issues)


def test_missing_current_form_is_blocking():
    artifact = _artifact().model_copy(update={"refined_idea": "  "})

    evaluation = MaturationCoverageGate.evaluate(artifact)

    assert evaluation.status == CoverageStatus.REPAIR_REQUIRED
    assert any(issue.issue_type == CoverageIssueType.CURRENT_FORM_REFERENCE_GAP for issue in evaluation.issues)


def test_next_action_with_invalid_uncertainty_reference_is_blocking():
    artifact = _artifact().model_copy(update={"recommended_next_action_target_uncertainty": "Incerteza inexistente."})

    evaluation = MaturationCoverageGate.evaluate(artifact)

    assert evaluation.status == CoverageStatus.REPAIR_REQUIRED
    assert any(issue.issue_type == CoverageIssueType.STRUCTURAL_COVERAGE_FAILURE for issue in evaluation.issues)


def test_core_and_ledger_checks_deduplicate_same_material_omission():
    artifact = _with_item(
        _artifact(),
        "I-CORE",
        status=IntentTreatmentStatus.DEFERRED,
        treatment_in_current_form="",
    )
    path = artifact.candidate_possibilities[0].model_copy(update={"intent_ids": ["I-SCARS"]})
    artifact = artifact.model_copy(update={"candidate_possibilities": [path]})

    evaluation = MaturationCoverageGate.evaluate(artifact)
    core_omission_issues = [
        issue for issue in evaluation.issues
        if issue.issue_type == CoverageIssueType.MATERIAL_INTENT_UNTREATED and issue.intent_id == "I-CORE"
    ]

    assert len(core_omission_issues) == 1


def test_missing_core_ledger_entry_is_detected_without_inventing_a_replacement():
    artifact = _artifact(
        intent_ledger=[
            _intent("I-SCARS", SCARS_QUOTE, "MATERIAL_SUBINTENT"),
            _intent("I-CONTROL", CONSTRAINT_QUOTE, "EXPLICIT_CONSTRAINT"),
        ],
        candidate_possibilities=[CandidatePossibility(
            path_id="PATH-001",
            mechanism="Uma base consulta referências anteriores.",
            intent_ids=["I-SCARS", "I-CONTROL"],
        )],
    )

    evaluation = MaturationCoverageGate.evaluate(artifact)

    assert evaluation.status == CoverageStatus.REPAIR_REQUIRED
    assert any(issue.issue_type == CoverageIssueType.STRUCTURAL_COVERAGE_FAILURE for issue in evaluation.issues)


def test_unstructured_natural_language_contradiction_is_outside_m3_claim_boundary():
    artifact = _artifact().model_copy(update={
        "refined_idea": "A automação escolhe pelo criador qual caminho deve ser seguido.",
    })

    evaluation = MaturationCoverageGate.evaluate(artifact)

    # No structured CONFLICT_FOUND signal exists; M3 makes no NL contradiction claim.
    assert evaluation.status == CoverageStatus.NO_BLOCKING_GAP_DETECTED
    assert all(issue.issue_type != CoverageIssueType.CONFLICT_FOUND for issue in evaluation.issues)


def test_one_path_narrow_idea_passes_without_diversity_quota():
    narrow_source = "Converter CSV para JSON preservando cabeçalhos."
    artifact = EvolutionArtifact(
        artifact_id="ART-NARROW-M3",
        run_id="RUN-NARROW-M3",
        treatment_mode=TreatmentMode.LEAN_L1,
        terminal_status="COMPLETED_DIRECT_ONE_PASS",
        original_idea=narrow_source,
        human_intent="Converter CSV para JSON sem perder os cabeçalhos.",
        refined_idea="Um conversor mapeia cada linha CSV a JSON preservando os cabeçalhos.",
        intent_ledger=[_intent(
            "I-CSV",
            narrow_source,
            "CORE_INTENT",
            treatment="A conversão e a preservação dos cabeçalhos estão na forma atual.",
        )],
        candidate_possibilities=[CandidatePossibility(
            path_id="PATH-001",
            mechanism="Mapear cabeçalhos CSV a chaves JSON.",
            intent_ids=["I-CSV"],
        )],
    )

    evaluated = MaturationCoverageGate.apply(artifact)

    assert len(evaluated.candidate_possibilities) == 1
    assert evaluated.coverage_status == CoverageStatus.NO_BLOCKING_GAP_DETECTED


def test_historical_schema_1_0_remains_not_evaluated_and_is_not_reprocessed():
    artifact = EvolutionArtifact.model_validate({
        "schema_version": SCHEMA_VERSION_1_0,
        "artifact_id": "ART-HISTORICAL-M3",
        "run_id": "RUN-HISTORICAL-M3",
        "treatment_mode": "LEAN_L1",
        "terminal_status": "COMPLETED",
        "original_idea": "Uma ideia histórica.",
        "human_intent": "Uma intenção antiga.",
        "refined_idea": "Uma forma antiga.",
    })

    assert artifact.coverage_status == CoverageStatus.NOT_EVALUATED
    with pytest.raises(ValueError, match="schema 1.1"):
        MaturationCoverageGate.apply(artifact)
