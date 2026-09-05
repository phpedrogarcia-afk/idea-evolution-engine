"""
tests/test_m05_5r1_amendment_002_resilience.py
Deterministic offline regression tests for Amendment 002 bounded strict-schema resilience.

Zero network calls.
Zero provider calls.
Zero holdout semantic debugging.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping
import pytest
from unittest.mock import patch
from pydantic import BaseModel, Field

from tools.experiments.execute_m05_5r1_confirmatory import (
    AppendOnlyUsageLedger,
    ConfirmatoryPreRequestGuard,
    GuardedGroqConfirmatoryRunner,
    is_strict_schema_replay_eligible,
    preflight_verification,
    DEFAULT_ATTEMPT_ID,
    M054_FREEZE_MANIFEST,
)


class DummyOutputSchema(BaseModel):
    summary: str = Field(description="Summary")
    proposed_mechanism: str = Field(description="Core mechanism")


class MockGroqError(Exception):
    def __init__(self, message: str, body: Mapping[str, Any], http_status: int = 400, headers: Mapping[str, str] = None):
        super().__init__(message)
        self.body = body
        self.response = type("Resp", (), {"headers": headers or {}, "status_code": http_status})()
        self.status_code = http_status


def _make_schema_fail_exc(missing_prop: str = "proposed_mechanism") -> MockGroqError:
    return MockGroqError(
        message=f"Error: jsonschema: '' does not validate with /required: missing properties: '{missing_prop}'",
        body={
            "error": {
                "message": f"Generated JSON does not match expected schema. Missing '{missing_prop}'",
                "code": "json_validate_failed",
                "failed_generation": '{"summary": "incomplete"}',
            }
        },
        http_status=400,
    )


# ---------------------------------------------------------------------------
# 1. Eligibility Classification Tests
# ---------------------------------------------------------------------------

def test_exact_http400_json_validate_failed_with_failed_gen_is_eligible():
    eligible = is_strict_schema_replay_eligible(
        http_status=400,
        provider_error_code="json_validate_failed",
        failed_generation_present=True,
        replay_attempt=0,
    )
    assert eligible is True


def test_json_validate_failed_without_failed_gen_is_not_eligible():
    eligible = is_strict_schema_replay_eligible(
        http_status=400,
        provider_error_code="json_validate_failed",
        failed_generation_present=False,
        replay_attempt=0,
    )
    assert eligible is False


def test_arbitrary_http400_is_not_eligible():
    eligible = is_strict_schema_replay_eligible(
        http_status=400,
        provider_error_code="invalid_request_error",
        failed_generation_present=True,
        replay_attempt=0,
    )
    assert eligible is False


def test_http429_is_not_eligible():
    eligible = is_strict_schema_replay_eligible(
        http_status=429,
        provider_error_code="rate_limit_exceeded",
        failed_generation_present=False,
        replay_attempt=0,
    )
    assert eligible is False


def test_http500_is_not_eligible():
    eligible = is_strict_schema_replay_eligible(
        http_status=500,
        provider_error_code="internal_server_error",
        failed_generation_present=False,
        replay_attempt=0,
    )
    assert eligible is False


def test_network_failure_is_not_eligible():
    eligible = is_strict_schema_replay_eligible(
        http_status=None,
        provider_error_code=None,
        failed_generation_present=False,
        replay_attempt=0,
    )
    assert eligible is False


def test_second_replay_attempt_is_not_eligible():
    eligible = is_strict_schema_replay_eligible(
        http_status=400,
        provider_error_code="json_validate_failed",
        failed_generation_present=True,
        replay_attempt=1,  # Already replayed once
    )
    assert eligible is False


# ---------------------------------------------------------------------------
# 2. Replay Behavior and Accounting Tests
# ---------------------------------------------------------------------------

def test_successful_http200_dispatches_once_no_replay(tmp_path):
    ledger = AppendOnlyUsageLedger(tmp_path / "ledger.jsonl")
    guard = ConfirmatoryPreRequestGuard(ledger, sleep=lambda s: None)

    call_count = 0

    def mock_transport(payload):
        nonlocal call_count
        call_count += 1
        return {
            "content": json.dumps({"summary": "Valid", "proposed_mechanism": "Working"}),
            "usage": {"prompt_tokens": 100, "completion_tokens": 50, "total_tokens": 150},
            "system_fingerprint": "fp_test1",
            "rate_limit_headers": {},
        }

    runner = GuardedGroqConfirmatoryRunner(
        guard,
        block_id="REAL-EXECUTION-ATTEMPT-004-H01",
        treatment="CONDITION_B",
        transport=mock_transport,
    )

    response = runner.generate("Prompt text", DummyOutputSchema, stage_name="UNDERSTAND")
    assert response.error is None
    assert response.retry_count == 0
    assert call_count == 1
    assert guard.strict_schema_failure_count == 0
    assert guard.strict_schema_replay_count == 0
    assert guard.strict_schema_replay_success_count == 0
    assert guard.closed_outcome is None


def test_schema_failure_then_identical_replay_succeeds(tmp_path):
    ledger = AppendOnlyUsageLedger(tmp_path / "ledger.jsonl")
    guard = ConfirmatoryPreRequestGuard(ledger, sleep=lambda s: None)

    call_count = 0
    payloads_seen = []

    def mock_transport(payload):
        nonlocal call_count
        call_count += 1
        payloads_seen.append(payload)
        if call_count == 1:
            raise _make_schema_fail_exc()
        return {
            "content": json.dumps({"summary": "Recovered", "proposed_mechanism": "Working now"}),
            "usage": {"prompt_tokens": 100, "completion_tokens": 50, "total_tokens": 150},
            "system_fingerprint": "fp_test2",
            "rate_limit_headers": {},
        }

    runner = GuardedGroqConfirmatoryRunner(
        guard,
        block_id="REAL-EXECUTION-ATTEMPT-004-H08",
        treatment="CONDITION_B",
        transport=mock_transport,
    )

    response = runner.generate("Prompt text", DummyOutputSchema, stage_name="UNDERSTAND")
    assert response.error is None
    assert response.retry_count == 1
    assert call_count == 2
    assert guard.strict_schema_failure_count == 1
    assert guard.strict_schema_replay_count == 1
    assert guard.strict_schema_replay_success_count == 1
    assert guard.strict_schema_replay_exhausted_count == 0
    assert guard.condition_schema_replays["CONDITION_B"] == 1
    assert guard.closed_outcome is None

    # Assert payloads were 100% identical
    assert len(payloads_seen) == 2
    assert payloads_seen[0] == payloads_seen[1]

    # Check ledger events: pre_dispatch, post_error, schema_replay_dispatch, pre_dispatch, post_response
    event_types = [e["event"] for e in ledger.events]
    assert event_types == ["pre_dispatch", "post_error", "schema_replay_dispatch", "pre_dispatch", "post_response"]
    assert ledger.events[1]["is_replay_eligible"] is True
    assert ledger.events[2]["replay_reason"] == "PROVIDER_STRICT_JSON_SCHEMA_DELIVERY_FAILURE"
    assert ledger.events[4]["is_schema_replay"] is True


def test_schema_failure_and_replay_also_fails_is_terminal(tmp_path):
    ledger = AppendOnlyUsageLedger(tmp_path / "ledger.jsonl")
    guard = ConfirmatoryPreRequestGuard(ledger, sleep=lambda s: None)

    call_count = 0

    def mock_transport(payload):
        nonlocal call_count
        call_count += 1
        raise _make_schema_fail_exc()

    runner = GuardedGroqConfirmatoryRunner(
        guard,
        block_id="REAL-EXECUTION-ATTEMPT-004-H08",
        treatment="CONDITION_B",
        transport=mock_transport,
    )

    response = runner.generate("Prompt text", DummyOutputSchema, stage_name="UNDERSTAND")
    assert response.error is not None
    assert "STRICT_SCHEMA_REPLAY_EXHAUSTED" in response.error
    assert call_count == 2  # Exactly 2 calls, no third call
    assert guard.strict_schema_failure_count == 1
    assert guard.strict_schema_replay_count == 1
    assert guard.strict_schema_replay_success_count == 0
    assert guard.strict_schema_replay_exhausted_count == 1
    assert guard.closed_outcome == "INVALID_EXECUTION"


def test_identical_resilience_rule_across_conditions_a_b_c(tmp_path):
    for cond in ["CONDITION_A", "CONDITION_B", "CONDITION_C"]:
        ledger = AppendOnlyUsageLedger(tmp_path / f"ledger_{cond}.jsonl")
        guard = ConfirmatoryPreRequestGuard(ledger, sleep=lambda s: None)
        call_count = 0

        def mock_transport(payload):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise _make_schema_fail_exc()
            return {
                "content": json.dumps({"summary": f"Valid {cond}", "proposed_mechanism": "Works"}),
                "usage": {"prompt_tokens": 50, "completion_tokens": 25, "total_tokens": 75},
            }

        runner = GuardedGroqConfirmatoryRunner(
            guard,
            block_id=f"REAL-EXECUTION-ATTEMPT-004-{cond}",
            treatment=cond,
            transport=mock_transport,
        )

        resp = runner.generate("Prompt", DummyOutputSchema, stage_name="UNDERSTAND")
        assert resp.error is None
        assert resp.retry_count == 1
        assert call_count == 2
        assert guard.condition_schema_replays[cond] == 1
        assert guard.strict_schema_replay_success_count == 1


def test_attempt_registry_blocks_002_003_004_and_allows_fresh():
    manifest = json.loads(M054_FREEZE_MANIFEST.read_text(encoding="utf-8"))
    ref_hashes = manifest.get("execution_critical_hashes", {})
    with patch("tools.experiments.execute_m05_5r1_confirmatory.sha256_file", side_effect=lambda p: ref_hashes.get(p.name, "0" * 64)):
        with pytest.raises(RuntimeError, match="ATTEMPT_REGISTRY_GUARD"):
            preflight_verification(attempt_id="REAL-EXECUTION-ATTEMPT-002")

        with pytest.raises(RuntimeError, match="ATTEMPT_REGISTRY_GUARD"):
            preflight_verification(attempt_id="REAL-EXECUTION-ATTEMPT-003")

        with pytest.raises(RuntimeError, match="ATTEMPT_REGISTRY_GUARD"):
            preflight_verification(attempt_id="REAL-EXECUTION-ATTEMPT-004")

        holdouts, sched = preflight_verification(attempt_id="REAL-EXECUTION-ATTEMPT-RESERVED-TEST")
        assert len(holdouts) == 8
        assert len(sched) == 24
