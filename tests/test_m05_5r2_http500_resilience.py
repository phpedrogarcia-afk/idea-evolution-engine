"""
tests/test_m05_5r2_http500_resilience.py
Testes determinísticos offline para a Emenda 001 de Resiliência Estrita a HTTP 500 (M05.5R2).

Zero chamadas de rede ao vivo.
Zero inferências reais.
"""

import json
import urllib.error
from pathlib import Path
from unittest.mock import MagicMock, patch
import pytest
from pydantic import BaseModel, Field

from tools.experiments.execute_m05_5r2_confirmatory import (
    AppendOnlyUsageLedger,
    AttemptResilienceTracker,
    ConfirmatoryCerebrasRunner,
    TokenAwarePacer,
    MAX_IDENTICAL_HTTP500_REPLAYS_PER_LOGICAL_CALL,
    MAX_TOTAL_HTTP500_REPLAYS_PER_ATTEMPT,
    SDK_MAX_RETRIES,
)


class DummyOutputSchema(BaseModel):
    summary: str = Field(description="Summary text")


def test_sdk_max_retries_remains_zero():
    assert SDK_MAX_RETRIES == 0
    assert MAX_IDENTICAL_HTTP500_REPLAYS_PER_LOGICAL_CALL == 1
    assert MAX_TOTAL_HTTP500_REPLAYS_PER_ATTEMPT == 1


def make_mock_http_response(content_dict):
    m = MagicMock()
    m.read.return_value = json.dumps(content_dict).encode("utf-8")
    m.__enter__.return_value = m
    m.__exit__.return_value = False
    return m


def test_http500_single_replay_success(tmp_path):
    ledger_path = tmp_path / "ledger.jsonl"
    ledger = AppendOnlyUsageLedger(ledger_path)
    pacer = TokenAwarePacer(ledger=ledger, safe_rpm=4, safe_tpm=27000, min_cadence_seconds=0.01)
    tracker = AttemptResilienceTracker(max_attempt_http500_replays=1)

    runner = ConfirmatoryCerebrasRunner(
        ledger=ledger,
        pacer=pacer,
        cell_id="TEST-CELL-H01",
        treatment="CONDITION_B",
        tracker=tracker,
        temperature=0.3,
        max_tokens=4096,
    )

    # Mock urllib: 1ª chamada HTTP 500, 2ª chamada HTTP 200 OK
    resp_200 = make_mock_http_response({
        "choices": [{"message": {"content": '{"summary": "Replay succeeded"}'}, "finish_reason": "stop"}],
        "usage": {"prompt_tokens": 100, "completion_tokens": 50, "total_tokens": 150},
        "system_fingerprint": "fp_test_123",
    })

    err_500 = urllib.error.HTTPError(
        url="https://api.cerebras.ai/v1/chat/completions",
        code=500,
        msg="Internal Server Error",
        hdrs={},
        fp=None,
    )

    with patch("urllib.request.urlopen", side_effect=[err_500, resp_200]), \
         patch("time.sleep", return_value=None):
        res = runner.generate(
            prompt_text="Test prompt text",
            output_schema=DummyOutputSchema,
            stage_name="TEST_STAGE",
        )

    assert res.parsed.summary == "Replay succeeded"
    assert tracker.http500_errors_seen == 1
    assert tracker.http500_replays_used == 1
    assert tracker.http500_replay_successes == 1

    # Verificar ledger: contém provider_error (500), replay_authorized e post_response (200)
    events = ledger.events
    assert any(e["event"] == "provider_error" and e["http_status"] == 500 for e in events)
    assert any(e["event"] == "http500_replay_authorized" for e in events)
    assert any(e["event"] == "post_response" and e.get("is_http500_replay") is True for e in events)

    # Verificar que o hash sanitizado do payload é idêntico entre a falha e o replay
    err_ev = [e for e in events if e["event"] == "provider_error"][0]
    auth_ev = [e for e in events if e["event"] == "http500_replay_authorized"][0]
    succ_ev = [e for e in events if e["event"] == "post_response"][0]
    assert err_ev["sanitized_payload_sha256"] == auth_ev["sanitized_payload_sha256"]
    assert auth_ev["sanitized_payload_sha256"] == succ_ev["sanitized_payload_sha256"]


def test_http500_replay_failure_aborts(tmp_path):
    ledger_path = tmp_path / "ledger.jsonl"
    ledger = AppendOnlyUsageLedger(ledger_path)
    pacer = TokenAwarePacer(ledger=ledger, safe_rpm=4, safe_tpm=27000, min_cadence_seconds=0.01)
    tracker = AttemptResilienceTracker(max_attempt_http500_replays=1)

    runner = ConfirmatoryCerebrasRunner(
        ledger=ledger,
        pacer=pacer,
        cell_id="TEST-CELL-H01",
        treatment="CONDITION_B",
        tracker=tracker,
        temperature=0.3,
        max_tokens=4096,
    )

    err_500 = urllib.error.HTTPError(
        url="https://api.cerebras.ai/v1/chat/completions",
        code=500,
        msg="Internal Server Error",
        hdrs={},
        fp=None,
    )

    # Ambas as tentativas retornam HTTP 500
    with patch("urllib.request.urlopen", side_effect=[err_500, err_500]), \
         patch("time.sleep", return_value=None):
        with pytest.raises(RuntimeError, match="HTTP500_REPLAY_FAILED"):
            runner.generate(
                prompt_text="Test prompt text",
                output_schema=DummyOutputSchema,
                stage_name="TEST_STAGE",
            )

    assert tracker.http500_errors_seen == 1
    assert tracker.http500_replays_used == 1
    assert tracker.http500_replay_successes == 0
    assert any(e["event"] == "http500_replay_failed" for e in ledger.events)


def test_http500_attempt_budget_exhaustion(tmp_path):
    ledger_path = tmp_path / "ledger.jsonl"
    ledger = AppendOnlyUsageLedger(ledger_path)
    pacer = TokenAwarePacer(ledger=ledger, safe_rpm=4, safe_tpm=27000, min_cadence_seconds=0.01)
    # Orçamento de tentativa já consumido (replays_used = 1)
    tracker = AttemptResilienceTracker(max_attempt_http500_replays=1)
    tracker.http500_replays_used = 1

    runner = ConfirmatoryCerebrasRunner(
        ledger=ledger,
        pacer=pacer,
        cell_id="TEST-CELL-H02",
        treatment="CONDITION_B",
        tracker=tracker,
        temperature=0.3,
        max_tokens=4096,
    )

    err_500 = urllib.error.HTTPError(
        url="https://api.cerebras.ai/v1/chat/completions",
        code=500,
        msg="Internal Server Error",
        hdrs={},
        fp=None,
    )

    with patch("urllib.request.urlopen", side_effect=err_500):
        with pytest.raises(RuntimeError, match="HTTP500_ATTEMPT_BUDGET_EXHAUSTED"):
            runner.generate(
                prompt_text="Test prompt text",
                output_schema=DummyOutputSchema,
                stage_name="TEST_STAGE",
            )

    assert tracker.http500_replay_exhausted is True
    assert any(e["event"] == "http500_replay_budget_exhausted" for e in ledger.events)


@pytest.mark.parametrize("error_code", [400, 401, 403, 429, 502, 503, 504])
def test_non_500_errors_fail_closed_without_replay(tmp_path, error_code):
    ledger_path = tmp_path / "ledger.jsonl"
    ledger = AppendOnlyUsageLedger(ledger_path)
    pacer = TokenAwarePacer(ledger=ledger, safe_rpm=4, safe_tpm=27000, min_cadence_seconds=0.01)
    tracker = AttemptResilienceTracker(max_attempt_http500_replays=1)

    runner = ConfirmatoryCerebrasRunner(
        ledger=ledger,
        pacer=pacer,
        cell_id="TEST-CELL-H03",
        treatment="CONDITION_B",
        tracker=tracker,
        temperature=0.3,
        max_tokens=4096,
    )

    http_err = urllib.error.HTTPError(
        url="https://api.cerebras.ai/v1/chat/completions",
        code=error_code,
        msg=f"Error {error_code}",
        hdrs={},
        fp=None,
    )

    with patch("urllib.request.urlopen", side_effect=http_err):
        with pytest.raises(urllib.error.HTTPError):
            runner.generate(
                prompt_text="Test prompt text",
                output_schema=DummyOutputSchema,
                stage_name="TEST_STAGE",
            )

    # Zero replays autorizados
    assert tracker.http500_replays_used == 0
    assert not any(e["event"] == "http500_replay_authorized" for e in ledger.events)
    assert any(e["event"] == "provider_error" and e["http_status"] == error_code for e in ledger.events)


def test_schema_failure_fails_closed_without_replay(tmp_path):
    ledger_path = tmp_path / "ledger.jsonl"
    ledger = AppendOnlyUsageLedger(ledger_path)
    pacer = TokenAwarePacer(ledger=ledger, safe_rpm=4, safe_tpm=27000, min_cadence_seconds=0.01)
    tracker = AttemptResilienceTracker(max_attempt_http500_replays=1)

    runner = ConfirmatoryCerebrasRunner(
        ledger=ledger,
        pacer=pacer,
        cell_id="TEST-CELL-H04",
        treatment="CONDITION_B",
        tracker=tracker,
        temperature=0.3,
        max_tokens=4096,
    )

    # Mock HTTP 200 mas com JSON incompatível com o schema
    resp_invalid_json = make_mock_http_response({
        "choices": [{"message": {"content": '{"invalid_field": 123}'}, "finish_reason": "stop"}],
        "usage": {"prompt_tokens": 100, "completion_tokens": 50, "total_tokens": 150},
        "system_fingerprint": "fp_test",
    })

    with patch("urllib.request.urlopen", return_value=resp_invalid_json):
        with pytest.raises(RuntimeError, match="VALIDATION_ERROR"):
            runner.generate(
                prompt_text="Test prompt text",
                output_schema=DummyOutputSchema,
                stage_name="TEST_STAGE",
            )

    assert tracker.http500_replays_used == 0
    assert not any(e["event"] == "http500_replay_authorized" for e in ledger.events)
    assert any(e["event"] == "validation_error" for e in ledger.events)
