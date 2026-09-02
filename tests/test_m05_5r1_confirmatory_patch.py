"""
tests/test_m05_5r1_confirmatory_patch.py
Deterministic offline regression tests for the M05.5R1 reviewability classifier and harness guards.

Zero network calls.
Zero provider calls.
Zero holdout semantic debugging.
"""

from __future__ import annotations

import json
from pathlib import Path
import pytest

from tools.experiments.execute_m05_5r1_confirmatory import (
    classify_cell_reviewability,
    preflight_verification,
    execute_confirmatory_cell,
    REPO_ROOT,
    EXP_DIR,
)


# ---------------------------------------------------------------------------
# 1. Condition A Unit Tests
# ---------------------------------------------------------------------------

def test_condition_a_valid_candidate_is_reviewable():
    cell_result = {
        "condition": "CONDITION_A",
        "status": "SUCCESS",
        "error": None,
        "parsed_output": {
            "summary": "Um resumo claro.",
            "refined_version": "Uma versão refinada substantiva da ideia.",
            "strengths": ["Forte"],
            "weaknesses": ["Fraco"],
            "next_steps": ["Próximo"],
        },
        "rendered_semantic_text": (
            "### Resumo\nUm resumo claro.\n\n"
            "### Versão Refinada\nUma versão refinada substantiva da ideia.\n\n"
            "### Pontos Fortes e Fracos\n- **Fortes:** Forte\n- **Fracos:** Fraco\n\n"
            "### Próximos Passos\nPróximo"
        ),
    }
    reviewable, reason = classify_cell_reviewability(cell_result)
    assert reviewable is True
    assert reason == "A_VALID_BASELINE_CANDIDATE"


def test_condition_a_failure_is_not_reviewable():
    cell_result = {
        "condition": "CONDITION_A",
        "status": "FAILED",
        "error": "PROVIDER_TIMEOUT",
        "parsed_output": {},
        "rendered_semantic_text": "",
    }
    reviewable, reason = classify_cell_reviewability(cell_result)
    assert reviewable is False
    assert "A_EXECUTION_ERROR" in reason


def test_condition_a_missing_refined_version_is_not_reviewable():
    cell_result = {
        "condition": "CONDITION_A",
        "status": "SUCCESS",
        "error": None,
        "parsed_output": {"summary": "Sem refinada"},
        "rendered_semantic_text": "### Resumo\nSem refinada",
    }
    reviewable, reason = classify_cell_reviewability(cell_result)
    assert reviewable is False
    assert reason == "A_MISSING_REFINED_VERSION"


# ---------------------------------------------------------------------------
# 2. Condition B Unit Tests
# ---------------------------------------------------------------------------

def test_condition_b_refinement_incomplete_with_substantive_candidate_is_reviewable():
    cell_result = {
        "condition": "CONDITION_B",
        "status": "FAILED",  # Orchestration status is FAILED when hard gates detect contradictions
        "terminal_status": "REFINEMENT_INCOMPLETE",
        "error": None,
        "stages_executed": [
            "UNDERSTAND", "ATTACK", "ALTERNATIVES", "SYNTHESIZE", "REALITY_CHECK", "FINAL_REVIEW"
        ],
        "rendered_semantic_text": (
            "### Ideia Refinada Final\nTexto substantivo da ideia refinada.\n\n"
            "### Intenção Humana Preservada\nIntenção substantiva preservada.\n\n"
            "### Mecanismo Central\nMecanismo substantivo construído.\n\n"
            "### Incertezas Críticas Remanescentes\n- Incerteza ontológica 1.\n\n"
            "### Próxima Ação Recomendada\nConstruir protótipo experimental."
        ),
    }
    reviewable, reason = classify_cell_reviewability(cell_result)
    assert reviewable is True
    assert reason == "B_SUBSTANTIVE_CANDIDATE_REFINEMENT_INCOMPLETE"


def test_condition_b_provider_failure_with_intermediate_text_is_not_reviewable():
    # Attempt-001 failure mode: crashed at SYNTHESIZE before FINAL_REVIEW, leaving partial text
    cell_result = {
        "condition": "CONDITION_B",
        "status": "FAILED",
        "terminal_status": "FAILED",
        "error": None,
        "stages_executed": ["UNDERSTAND", "ATTACK", "ALTERNATIVES", "SYNTHESIZE"],
        "rendered_semantic_text": (
            "### Ideia Refinada Final\nTexto preliminar.\n\n"
            "### Intenção Humana Preservada\nIntenção.\n\n"
            "### Mecanismo Central\nMecanismo.\n\n"
            "### Incertezas Críticas Remanescentes\n\n\n"
            "### Próxima Ação Recomendada\n"
        ),
    }
    reviewable, reason = classify_cell_reviewability(cell_result)
    assert reviewable is False
    assert "B_INVALID_TERMINAL_STATUS" in reason or "B_FINAL_REVIEW_NOT_REACHED" in reason


def test_condition_b_empty_substantive_section_is_not_reviewable():
    cell_result = {
        "condition": "CONDITION_B",
        "status": "FAILED",
        "terminal_status": "REFINEMENT_INCOMPLETE",
        "error": None,
        "stages_executed": ["UNDERSTAND", "ATTACK", "ALTERNATIVES", "SYNTHESIZE", "REALITY_CHECK", "FINAL_REVIEW"],
        "rendered_semantic_text": (
            "### Ideia Refinada Final\nTexto preliminar.\n\n"
            "### Intenção Humana Preservada\nIntenção.\n\n"
            "### Mecanismo Central\nMecanismo.\n\n"
            "### Incertezas Críticas Remanescentes\n\n\n"
            "### Próxima Ação Recomendada\n"
        ),
    }
    reviewable, reason = classify_cell_reviewability(cell_result)
    assert reviewable is False
    assert "B_EMPTY_SECTION_BODY" in reason


# ---------------------------------------------------------------------------
# 3. Condition C Unit Tests
# ---------------------------------------------------------------------------

def test_condition_c_human_decision_required_is_reviewable():
    cell_result = {
        "condition": "CONDITION_C",
        "status": "SUCCESS",
        "terminal_status": "HUMAN_DECISION_REQUIRED",
        "error": None,
        "rendered_semantic_text": (
            "### Intenção Central\nIntenção central preservada.\n\n"
            "### Mecanismo Proposto\nMecanismo primário.\n\n"
            "### Vulnerabilidades Identificadas\n- Risco alto.\n\n"
            "### Próxima Ação Recomendada\nDecisão humana necessária."
        ),
    }
    reviewable, reason = classify_cell_reviewability(cell_result)
    assert reviewable is True
    assert reason == "C_SUBSTANTIVE_CANDIDATE_HUMAN_DECISION_REQUIRED"


def test_condition_c_completed_with_focused_escalation_is_reviewable():
    cell_result = {
        "condition": "CONDITION_C",
        "status": "SUCCESS",
        "terminal_status": "COMPLETED_WITH_FOCUSED_ESCALATION",
        "error": None,
        "rendered_semantic_text": (
            "### Intenção Central\nIntenção central preservada.\n\n"
            "### Mecanismo Proposto\nMecanismo escalado.\n\n"
            "### Vulnerabilidades Identificadas\n- Resolvidas.\n\n"
            "### Próxima Ação Recomendada\nImplementar."
        ),
    }
    reviewable, reason = classify_cell_reviewability(cell_result)
    assert reviewable is True
    assert reason == "C_SUBSTANTIVE_CANDIDATE_COMPLETED_WITH_FOCUSED_ESCALATION"


def test_condition_c_first_pass_failed_is_not_reviewable():
    # Attempt-001 failure mode: rate limit on first pass with error message in markdown
    cell_result = {
        "condition": "CONDITION_C",
        "status": "FAILED",
        "terminal_status": "FIRST_PASS_FAILED",
        "error": "PROVIDER_RATE_LIMIT",
        "rendered_semantic_text": "### Falha na Execução\nRate limit exceeded.",
    }
    reviewable, reason = classify_cell_reviewability(cell_result)
    assert reviewable is False


# ---------------------------------------------------------------------------
# 4. Infrastructure Guard Closure Tests
# ---------------------------------------------------------------------------

def test_infrastructure_guard_closed_aborts():
    cell_result = {
        "condition": "CONDITION_A",
        "status": "SUCCESS",
        "rendered_semantic_text": "Valid text",
    }
    reviewable, reason = classify_cell_reviewability(cell_result, guard_closed_outcome="ABORTED_CAPACITY")
    assert reviewable is False
    assert reason == "INFRASTRUCTURE_GUARD_CLOSED:ABORTED_CAPACITY"


# ---------------------------------------------------------------------------
# 5. Registry & Immutability Tests
# ---------------------------------------------------------------------------

def test_attempt_002_003_004_reuse_is_refused():
    with pytest.raises(RuntimeError, match="ATTEMPT_REGISTRY_GUARD"):
        preflight_verification(attempt_id="REAL-EXECUTION-ATTEMPT-002")
    with pytest.raises(RuntimeError, match="ATTEMPT_REGISTRY_GUARD"):
        preflight_verification(attempt_id="REAL-EXECUTION-ATTEMPT-003")
    with pytest.raises(RuntimeError, match="ATTEMPT_REGISTRY_GUARD"):
        preflight_verification(attempt_id="REAL-EXECUTION-ATTEMPT-004")


def test_attempt_fresh_reservation_is_allowed():
    holdout_map, schedule = preflight_verification(attempt_id="REAL-EXECUTION-ATTEMPT-RESERVED-TEST")
    assert len(holdout_map) == 8
    assert len(schedule) == 24


def test_existing_cell_overwrite_is_refused(tmp_path):
    existing_file = tmp_path / "H01_condition_a.json"
    existing_file.write_text("{}", encoding="utf-8")
    with pytest.raises(RuntimeError, match="CELL_OVERWRITE_GUARD"):
        execute_confirmatory_cell(
            holdout_id="H01",
            condition="CONDITION_A",
            raw_idea="Idea text",
            runner=None,
            raw_dir=tmp_path,
            attempt_id="REAL-EXECUTION-ATTEMPT-003",
        )


# ---------------------------------------------------------------------------
# 6. M05.4 Prospective Reference Regression Oracle (8/8 A, 8/8 B, 8/8 C)
# ---------------------------------------------------------------------------

def test_m05_4_prospective_reference_regression_oracle():
    m054_raw = REPO_ROOT / "experiments" / "EXP-M05.4-PROSPECTIVE-RERUN-20260829" / "REAL-EXECUTION-ATTEMPT-004" / "raw"
    assert m054_raw.is_dir()

    a_reviewable = 0
    b_reviewable = 0
    c_reviewable = 0

    for file_path in sorted(m054_raw.glob("*.json")):
        cell_data = json.loads(file_path.read_text(encoding="utf-8"))
        is_rev, reason = classify_cell_reviewability(cell_data)
        assert is_rev is True, f"M05.4 cell {file_path.name} failed reviewability: {reason}"

        cond = cell_data["condition"]
        if cond == "CONDITION_A":
            a_reviewable += 1
        elif cond == "CONDITION_B":
            b_reviewable += 1
        elif cond == "CONDITION_C":
            c_reviewable += 1

    assert a_reviewable == 8, f"Expected 8 reviewable Condition A cells, got {a_reviewable}"
    assert b_reviewable == 8, f"Expected 8 reviewable Condition B cells, got {b_reviewable}"
    assert c_reviewable == 8, f"Expected 8 reviewable Condition C cells, got {c_reviewable}"
