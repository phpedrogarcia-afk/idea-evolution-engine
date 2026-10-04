"""M4: one bounded, typed coverage repair, proved with offline fakes."""

from copy import deepcopy
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import pytest

from src.idea_evolution.artifacts.evolution_artifact import (
    CoverageIssueType,
    CoverageStatus,
)
from src.idea_evolution.domain.early_epistemic_gate import (
    EarlyEpistemicGate,
    EscalationReason,
    GateEvaluationResult,
    GateOutcome,
)
from src.idea_evolution.providers.fake import FakeModelRunner
from src.idea_evolution.providers.native import to_strict_json_schema
from src.idea_evolution.service.evolution_service import (
    MAX_LOGICAL_MODEL_CALLS_PER_LEAN_RUN,
    IdeaEvolutionService,
)
from src.idea_evolution.service.maturation_coverage_gate import MaturationCoverageGate
from src.idea_evolution.service.maturation_focused_repair import (
    CandidatePathRepair,
    IntentTreatmentRepair,
    MaturationFocusedRepair,
    MaturationRepairPatch,
    OpenDecisionRepair,
    RepairPatchRejected,
)
from src.idea_evolution.service.contracts import MaturationRepairOutcome


def _load_test_module(name: str, filename: str):
    spec = spec_from_file_location(name, Path(__file__).with_name(filename))
    assert spec is not None and spec.loader is not None
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_M2 = _load_test_module("_m4_m2_fixtures", "test_v12_m2_strong_first_pass.py")
_M3 = _load_test_module("_m4_m3_fixtures", "test_v12_m3_deterministic_coverage_gate.py")
FIOBASE_IDEA = _M2.FIOBASE_IDEA
fiobase_response = _M2.fiobase_response


def _first_pass_gap(intent_id="I-SCARS", status="DEFERRED", treatment=""):
    result = deepcopy(fiobase_response())
    target = next(item for item in result["intent_ledger"] if item["intent_id"] == intent_id)
    target["status"] = status
    target["treatment_in_current_form"] = treatment
    return result


def _service_run(first_pass, repair=None, tmp_path=None, *, fail_repair_schema=False):
    responses = {"LEAN_FIRST_PASS": first_pass}
    if repair is not None:
        responses["MATURATION_FOCUSED_REPAIR"] = repair
    failures = {"MATURATION_FOCUSED_REPAIR": 1} if fail_repair_schema else None
    runner = FakeModelRunner(
        custom_responses=responses,
        should_fail_schema_stages=failures,
    )
    service = IdeaEvolutionService(
        runner=runner,
        runs_dir=(tmp_path / "runs") if tmp_path else None,
    )
    response = service.evolve_idea(FIOBASE_IDEA, run_id="RUN-M4-OFFLINE")
    return response, runner


def test_fiobase_strong_first_pass_needs_one_call_and_no_repair(tmp_path):
    response, runner = _service_run(fiobase_response(), tmp_path=tmp_path)

    assert response.success is True
    assert response.artifact.coverage_status == CoverageStatus.NO_BLOCKING_GAP_DETECTED
    assert response.total_model_calls == 1
    assert runner.call_counts == {"LEAN_FIRST_PASS": 1}
    assert response.maturation_repair.repair_attempted is False
    assert response.maturation_repair.repair_outcome == MaturationRepairOutcome.NOT_NEEDED


@pytest.mark.parametrize(
    ("intent_id", "patch"),
    [
        (
            "I-SCARS",
            {"intent_repairs": [{
                "intent_id": "I-SCARS",
                "treatment_in_current_form": "A forma atual incorpora o reuso de scars como consulta revisável.",
                "status": "PRESERVED",
            }]},
        ),
        (
            "I-STARTUP",
            {"intent_repairs": [{
                "intent_id": "I-STARTUP",
                "treatment_in_current_form": "A forma atual preserva o uso da base no início do projeto.",
                "status": "PRESERVED",
            }]},
        ),
    ],
    ids=["fiobase-material-intent", "fiobase-explicit-constraint"],
)
def test_fiobase_untreated_intent_or_constraint_repairs_in_second_call(intent_id, patch, tmp_path):
    response, runner = _service_run(_first_pass_gap(intent_id), patch, tmp_path)

    assert response.artifact.coverage_status == CoverageStatus.NO_BLOCKING_GAP_DETECTED
    assert response.total_model_calls == 2
    assert runner.call_counts == {"LEAN_FIRST_PASS": 1, "MATURATION_FOCUSED_REPAIR": 1}
    assert response.maturation_repair.repair_attempted is True
    assert response.maturation_repair.repair_applied is True
    assert response.maturation_repair.issue_count_before > 0
    assert response.maturation_repair.issue_count_after == 0


@pytest.mark.parametrize(
    ("status", "treatment", "question"),
    [
        (
            "PROVISIONALLY_MODIFIED",
            "O reuso é provisório e continua sujeito a escolha posterior.",
            "O reaproveitamento de scars será obrigatório ou consultivo?",
        ),
        (
            "DEFERRED",
            "A forma atual mantém o reuso como ponto ainda não decidido.",
            "Quais lições anteriores devem permanecer disponíveis?",
        ),
    ],
    ids=["provisional-exposure", "deferred-exposure"],
)
def test_fiobase_provisional_or_deferred_item_gets_explicit_linked_decision(
    status, treatment, question, tmp_path
):
    first_pass = _first_pass_gap(status=status, treatment=treatment)
    patch = {"open_decision_repairs": [{"related_intent_id": "I-SCARS", "question": question}]}

    response, runner = _service_run(first_pass, patch, tmp_path)

    assert response.artifact.coverage_status == CoverageStatus.NO_BLOCKING_GAP_DETECTED
    assert response.artifact.human_decision_required is False
    decision = next(item for item in response.artifact.open_decisions if "I-SCARS" in item.related_intent_ids)
    assert decision.question == question
    assert decision.decision_id.startswith("M4-DECISION-")
    assert runner.call_counts["MATURATION_FOCUSED_REPAIR"] == 1


def test_narrow_idea_still_uses_one_call_without_repair(tmp_path):
    idea, first_pass = _M2.narrow_response()
    runner = FakeModelRunner(custom_responses={"LEAN_FIRST_PASS": first_pass})
    response = IdeaEvolutionService(runner=runner, runs_dir=tmp_path / "runs").evolve_idea(
        idea, run_id="RUN-M4-NARROW"
    )

    assert response.artifact.coverage_status == CoverageStatus.NO_BLOCKING_GAP_DETECTED
    assert len(response.artifact.candidate_possibilities) == 1
    assert response.total_model_calls == 1
    assert runner.call_counts == {"LEAN_FIRST_PASS": 1}


def test_path_reference_repair_targets_exact_existing_path_and_intents():
    artifact = _M3._artifact()
    broken_path = artifact.candidate_possibilities[0].model_copy(update={"intent_ids": ["I-UNKNOWN"]})
    broken = artifact.model_copy(update={"candidate_possibilities": [broken_path]})
    evaluation = MaturationCoverageGate.evaluate(broken)
    patch = MaturationRepairPatch(path_repairs=[CandidatePathRepair(
        path_id="PATH-001",
        intent_ids=["I-CORE", "I-SCARS", "I-CONTROL"],
    )])

    candidate = MaturationFocusedRepair.apply_patch(broken, patch, list(evaluation.issues))
    evaluated = MaturationCoverageGate.apply(candidate)

    assert evaluated.coverage_status == CoverageStatus.NO_BLOCKING_GAP_DETECTED
    assert evaluated.candidate_possibilities[0].path_id == "PATH-001"
    assert evaluated.candidate_possibilities[0].mechanism == artifact.candidate_possibilities[0].mechanism


def test_missing_current_form_can_be_repaired_without_authority_promotion():
    artifact = _M3._artifact().model_copy(update={"refined_idea": " "})
    evaluation = MaturationCoverageGate.evaluate(artifact)
    patch = MaturationRepairPatch(refined_idea="Uma forma atual provisória que preserva a intenção expressa.")

    candidate = MaturationFocusedRepair.apply_patch(artifact, patch, list(evaluation.issues))
    evaluated = MaturationCoverageGate.apply(candidate)

    assert evaluated.coverage_status == CoverageStatus.NO_BLOCKING_GAP_DETECTED
    assert evaluated.refined_idea_authority == artifact.refined_idea_authority
    assert evaluated.refined_idea_authority.value == "MODEL_HYPOTHESIS"
    assert evaluated.original_idea == artifact.original_idea


def test_invalid_next_uncertainty_can_be_retargeted_or_cleared_without_invention():
    artifact = _M3._artifact().model_copy(update={
        "recommended_next_action_target_uncertainty": "Incerteza inexistente."
    })
    evaluation = MaturationCoverageGate.evaluate(artifact)
    patch = MaturationRepairPatch(
        recommended_next_action_target_uncertainty=artifact.uncertainties[0]
    )

    candidate = MaturationFocusedRepair.apply_patch(artifact, patch, list(evaluation.issues))
    evaluated = MaturationCoverageGate.apply(candidate)

    assert evaluated.coverage_status == CoverageStatus.NO_BLOCKING_GAP_DETECTED
    assert evaluated.recommended_next_action_target_uncertainty == artifact.uncertainties[0]
    assert evaluated.uncertainties == artifact.uncertainties


def test_conflict_cannot_be_erased_without_a_new_explicit_treatment(tmp_path):
    first_pass = _first_pass_gap(status="CONFLICT_FOUND", treatment="O conflito foi identificado.")
    invalid_patch = {"intent_repairs": [{"intent_id": "I-SCARS", "status": "PRESERVED"}]}

    response, runner = _service_run(first_pass, invalid_patch, tmp_path)

    assert response.artifact.coverage_status == CoverageStatus.UNRESOLVED
    assert any(issue.issue_type == CoverageIssueType.CONFLICT_FOUND for issue in response.artifact.coverage_issues)
    assert response.total_model_calls == 2
    assert runner.call_counts["MATURATION_FOCUSED_REPAIR"] == 1
    assert response.maturation_repair.repair_applied is False


def test_valid_patch_that_leaves_deferred_exposure_becomes_unresolved(tmp_path):
    response, _ = _service_run(
        _first_pass_gap(status="DEFERRED", treatment=""),
        {"intent_repairs": [{
            "intent_id": "I-SCARS",
            "treatment_in_current_form": "A síntese agora registra como o intent é tratado.",
        }]},
        tmp_path,
    )

    assert response.artifact.coverage_status == CoverageStatus.UNRESOLVED
    assert [issue.issue_type for issue in response.artifact.coverage_issues] == [
        CoverageIssueType.DEFERRED_ITEM_NOT_EXPOSED
    ]
    assert response.maturation_repair.repair_applied is True
    assert response.maturation_repair.repair_outcome == MaturationRepairOutcome.REPAIR_INCOMPLETE
    assert response.total_model_calls == 2


def test_malformed_repair_output_fails_closed_without_runner_retry(tmp_path):
    response, runner = _service_run(
        _first_pass_gap(),
        tmp_path=tmp_path,
        fail_repair_schema=True,
    )

    assert response.artifact.coverage_status == CoverageStatus.UNRESOLVED
    assert response.maturation_repair.repair_attempted is True
    assert response.maturation_repair.repair_applied is False
    assert response.total_model_calls == 2
    assert runner.call_counts == {"LEAN_FIRST_PASS": 1, "MATURATION_FOCUSED_REPAIR": 1}


def test_unknown_target_rejects_entire_patch_and_preserves_first_pass(tmp_path):
    response, _ = _service_run(
        _first_pass_gap(),
        {"intent_repairs": [{
            "intent_id": "I-UNKNOWN",
            "treatment_in_current_form": "Conteúdo para alvo inexistente.",
        }]},
        tmp_path,
    )

    assert response.artifact.coverage_status == CoverageStatus.UNRESOLVED
    assert response.artifact.intent_ledger[1].intent_id == "I-SCARS"
    assert response.artifact.intent_ledger[1].treatment_in_current_form == ""
    assert response.maturation_repair.repair_applied is False


@pytest.mark.parametrize(
    "patch",
    [
        {"intent_repairs": [{
            "intent_id": "I-SCARS",
            "treatment_in_current_form": "Tratamento inventado.",
            "source_quote": "citação alterada",
        }]},
        {"intent_repairs": [{
            "intent_id": "I-SCARS",
            "treatment_in_current_form": "Tratamento inventado.",
        }], "human_decision_required": True},
    ],
    ids=["user-explicit-source-mutation", "authority-mutation"],
)
def test_forbidden_source_or_authority_mutations_fail_closed(patch, tmp_path):
    response, _ = _service_run(_first_pass_gap(), patch, tmp_path)

    assert response.artifact.coverage_status == CoverageStatus.UNRESOLVED
    assert response.artifact.original_idea == FIOBASE_IDEA
    assert response.artifact.human_decision_required is False
    assert response.artifact.intent_ledger[1].source_quote == _M2.SCARS_QUOTE
    assert response.maturation_repair.repair_applied is False


def test_repair_call_failure_returns_unresolved_instead_of_crashing(tmp_path):
    class RaisingRunner(FakeModelRunner):
        def generate(self, prompt_text, output_schema, stage_name, model_name=None, max_repairs=1):
            if stage_name == "MATURATION_FOCUSED_REPAIR":
                self.call_counts[stage_name] = self.call_counts.get(stage_name, 0) + 1
                self.prompt_history.setdefault(stage_name, []).append(prompt_text)
                raise RuntimeError("offline injected failure")
            return super().generate(prompt_text, output_schema, stage_name, model_name, max_repairs)

    runner = RaisingRunner(custom_responses={"LEAN_FIRST_PASS": _first_pass_gap()})
    response = IdeaEvolutionService(runner=runner, runs_dir=tmp_path / "runs").evolve_idea(
        FIOBASE_IDEA, run_id="RUN-M4-CALL-FAILURE"
    )

    assert response.success is True
    assert response.artifact.coverage_status == CoverageStatus.UNRESOLVED
    assert response.maturation_repair.repair_outcome == MaturationRepairOutcome.REPAIR_CALL_FAILED
    assert response.total_model_calls == 2
    assert runner.call_counts == {"LEAN_FIRST_PASS": 1, "MATURATION_FOCUSED_REPAIR": 1}


def test_early_epistemic_escalation_and_coverage_share_two_call_ceiling(monkeypatch, tmp_path):
    escalation = GateEvaluationResult(
        outcome=GateOutcome.ESCALATE_FOCUSED,
        escalation_reason=EscalationReason.MATERIAL_VULNERABILITY,
        explanation="A chamada existente consome a segunda posição lógica.",
    )
    monkeypatch.setattr(EarlyEpistemicGate, "evaluate", classmethod(lambda cls, **_: escalation))
    response, runner = _service_run(
        _first_pass_gap(),
        {"intent_repairs": [{
            "intent_id": "I-SCARS",
            "treatment_in_current_form": "Não deve ser solicitado por estar fora do budget.",
        }]},
        tmp_path,
    )

    assert MAX_LOGICAL_MODEL_CALLS_PER_LEAN_RUN == 2
    assert response.total_model_calls == 2
    assert response.lean_result.total_model_calls == 2
    assert response.artifact.total_model_calls == 2
    assert runner.call_counts == {"LEAN_FIRST_PASS": 1, "FOCUSED_ESCALATION": 1}
    assert response.maturation_repair.repair_attempted is False
    assert response.maturation_repair.repair_outcome == MaturationRepairOutcome.CALL_BUDGET_EXHAUSTED
    assert response.artifact.coverage_status == CoverageStatus.UNRESOLVED


def test_repair_patch_schema_is_closed_and_forbids_immutable_fields():
    with pytest.raises(ValueError):
        MaturationRepairPatch.model_validate({
            "intent_repairs": [{"intent_id": "I1", "status": "PRESERVED"}],
            "original_idea": "tampered",
        })
    with pytest.raises(ValueError):
        IntentTreatmentRepair.model_validate({
            "intent_id": "I1",
            "source_quote": "tampered",
            "status": "PRESERVED",
        })

    strict_schema = to_strict_json_schema(MaturationRepairPatch)
    assert strict_schema["additionalProperties"] is False
    assert set(strict_schema["properties"]) == {
        "intent_repairs",
        "path_repairs",
        "open_decision_repairs",
        "refined_idea",
        "recommended_next_action_target_uncertainty",
    }
    assert set(strict_schema["required"]) == set(strict_schema["properties"])
    for definition in strict_schema.get("$defs", {}).values():
        if definition.get("type") == "object":
            assert definition["additionalProperties"] is False
            assert set(definition["required"]) == set(definition["properties"])


def test_unknown_open_decision_id_rejects_patch_atomically():
    artifact = _M3._artifact(
        intent_ledger=[
            _M3._intent("I-CORE", _M3.CORE_QUOTE, "CORE_INTENT"),
            _M3._intent("I-SCARS", _M3.SCARS_QUOTE, "MATERIAL_SUBINTENT", status="PROVISIONALLY_MODIFIED"),
            _M3._intent("I-CONTROL", _M3.CONSTRAINT_QUOTE, "EXPLICIT_CONSTRAINT"),
        ]
    )
    evaluation = MaturationCoverageGate.evaluate(artifact)
    patch = MaturationRepairPatch(open_decision_repairs=[OpenDecisionRepair(
        related_intent_id="I-SCARS",
        question="Qual opção manter?",
        target_decision_id="DECISION-UNKNOWN",
    )])

    with pytest.raises(RepairPatchRejected, match="unknown open-decision target"):
        MaturationFocusedRepair.apply_patch(artifact, patch, list(evaluation.issues))
