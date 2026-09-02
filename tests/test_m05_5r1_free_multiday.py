from datetime import datetime, timedelta, timezone
from hashlib import sha256
import inspect
from pathlib import Path

import pytest

from tools.experiments.m05_5r1_free_multiday import (
    AppendOnlyUsageLedger, CONFIRMATORY_IDS, FREE_TPM, FreePreRequestGuard,
    FROZEN_PILOT_TREATMENT_ORDER, OUTPUT_CAP_TOKENS, QuotaIsolatedBlockWindow,
    SACRIFICIAL_CLASSIFICATION, SACRIFICIAL_SOURCE_CONTENT_SHA256,
    GuardedGroqRunner, load_sacrificial_source, sacrificial_source_path,
    run_sacrificial_pilot,
)
from src.idea_evolution.stages.contracts import BaselineRefineOutput


def clock():
    return datetime(2026, 9, 1, tzinfo=timezone.utc)


def guard(tmp_path: Path, **kwargs):
    return FreePreRequestGuard(AppendOnlyUsageLedger(tmp_path / "usage.jsonl"), now=clock, **kwargs)


def admissible(g, request_id="r1", user="texto curto"):
    return g.pre_dispatch(request_id=request_id, block_id="PILOT-01",
                          classification=SACRIFICIAL_CLASSIFICATION,
                          treatment="CONDITION_A", call_index=1,
                          system="sistema", user=user)


def test_exact_chat_count_and_zero_cache_are_used_pre_dispatch(tmp_path):
    g = guard(tmp_path)
    decision = admissible(g)
    assert decision.serialized_input_tokens > 0
    assert decision.reserved_output_tokens == OUTPUT_CAP_TOKENS
    assert decision.conservative_request_load == decision.serialized_input_tokens + OUTPUT_CAP_TOKENS
    assert decision.cache_assumed_tokens == 0


def test_over_tpm_is_denied_before_dispatch(tmp_path):
    g = guard(tmp_path)
    decision = admissible(g, user="x " * FREE_TPM)
    assert not decision.allowed and decision.outcome == "ABORTED_CAPACITY"


def test_post_response_records_cache_only_after_response(tmp_path):
    g = guard(tmp_path)
    decision = admissible(g)
    g.post_response(decision, {"usage": {"prompt_tokens": 10, "completion_tokens": 5,
                    "total_tokens": 15, "prompt_tokens_details": {"cached_tokens": 4}},
                    "system_fingerprint": "fp-a"})
    post = g.ledger.events[-1]
    assert post["actual_cached_tokens"] == 4 and post["actual_prompt_tokens"] == 10


def test_ledger_is_append_only_tamper_evident_and_duplicate_ids_fail(tmp_path):
    g = guard(tmp_path)
    admissible(g, "same")
    with pytest.raises(RuntimeError, match="DUPLICATE_REQUEST_ID_DENIED"):
        admissible(g, "same")
    assert len(AppendOnlyUsageLedger(tmp_path / "usage.jsonl").events) == 1
    path = tmp_path / "usage.jsonl"
    path.write_text(path.read_text(encoding="utf-8").replace("PILOT-01", "tampered"), encoding="utf-8")
    with pytest.raises(RuntimeError, match="USAGE_LEDGER_INTEGRITY_INVALID"):
        AppendOnlyUsageLedger(path)


def test_schedule_mutation_and_confirmatory_selection_fail_closed(tmp_path):
    g = guard(tmp_path)
    g.assert_frozen_order(FROZEN_PILOT_TREATMENT_ORDER)
    with pytest.raises(RuntimeError, match="SCHEDULE_MUTATION"):
        g.assert_frozen_order(tuple(reversed(FROZEN_PILOT_TREATMENT_ORDER)))
    for holdout in CONFIRMATORY_IDS:
        with pytest.raises(PermissionError, match="CONFIRMATORY"):
            g.ensure_pilot_source(holdout, SACRIFICIAL_CLASSIFICATION)


def test_fingerprint_drift_and_429_abort(tmp_path):
    g = guard(tmp_path)
    first = admissible(g, "one")
    g.post_response(first, {"usage": {}, "system_fingerprint": "fp-a"})
    second = admissible(g, "two")
    g.post_response(second, {"usage": {}, "system_fingerprint": "fp-b"})
    assert g.closed_outcome == "INVALID_EXECUTION:BACKEND_DRIFT_WITHIN_BLOCK"
    third = admissible(g, "three")
    g.post_error(third, http_status=429, error="RATE_LIMIT")
    assert g.closed_outcome == "ABORTED_CAPACITY"


def test_sacrificial_fingerprint_drift_is_journaled_without_closing_capacity_pilot(tmp_path):
    g = guard(tmp_path, allow_sacrificial_fingerprint_drift=True)
    first = admissible(g, "one")
    g.post_response(first, {"usage": {}, "system_fingerprint": "fp-a"})
    second = admissible(g, "two")
    g.post_response(second, {"usage": {}, "system_fingerprint": "fp-b"})
    assert g.closed_outcome is None
    assert g.fingerprint_drift_observed
    assert g.fingerprints == ("fp-a", "fp-b")
    drift = g.ledger.events[-1]
    assert drift["event"] == "fingerprint_drift_observed"
    assert drift["fingerprints_in_order"] == ["fp-a", "fp-b"]


def test_rpm_and_tpm_window_and_restart_survival(tmp_path):
    ledger = AppendOnlyUsageLedger(tmp_path / "usage.jsonl")
    now = clock()
    ledger.append({"event": "pre_dispatch", "request_id": "prior", "allowed": True,
                   "timestamp": now.isoformat(), "conservative_request_load": FREE_TPM,
                   "block_id": "PILOT-01"})
    g = FreePreRequestGuard(ledger, now=clock)
    denied = admissible(g, "next")
    assert not denied.allowed and denied.outcome == "ABORTED_CAPACITY"
    assert len(AppendOnlyUsageLedger(tmp_path / "usage.jsonl").events) == 2


def test_next_block_not_before_survives_restart_and_denies_early_start(tmp_path):
    first = QuotaIsolatedBlockWindow(tmp_path / "block-window.json")
    state = first.close(clock())
    assert "previous_block_last_request_at" in state
    restarted = QuotaIsolatedBlockWindow(tmp_path / "block-window.json")
    with pytest.raises(RuntimeError, match="NEXT_BLOCK_NOT_BEFORE_DENIED"):
        restarted.assert_may_start(clock() + timedelta(hours=23, minutes=59))
    restarted.assert_may_start(clock() + timedelta(hours=24, minutes=5))


def test_live_pilot_entry_fails_before_source_or_provider_without_local_auth(tmp_path, monkeypatch):
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    with pytest.raises(RuntimeError, match="HUMAN_API_KEY_LOCAL_SETUP_REQUIRED"):
        run_sacrificial_pilot(tmp_path, tmp_path / "runtime")


def test_canonical_attempt_004_source_is_loaded_through_representation_only_adapter():
    repo_root = Path(__file__).resolve().parents[1]
    path = sacrificial_source_path(repo_root)
    normalized = load_sacrificial_source(repo_root)
    assert path.name == "input.json"
    assert set(normalized) == {"source_idea"}
    assert sha256(normalized["source_idea"].encode("utf-8")).hexdigest() == SACRIFICIAL_SOURCE_CONTENT_SHA256


def test_transport_is_called_once_and_never_retried(tmp_path):
    calls = []
    def unavailable(payload):
        calls.append(payload)
        raise RuntimeError("network unavailable")
    runner = GuardedGroqRunner(guard(tmp_path), block_id="PILOT-01", treatment="CONDITION_A",
                               transport=unavailable)
    response = runner.generate("texto", BaselineRefineOutput, "BASELINE_REFINE")
    assert len(calls) == 1
    assert response.retry_count == 0
    assert response.error.startswith("PROVIDER_EXECUTION_ERROR")


def test_429_aborts_capacity_and_is_not_a_product_response(tmp_path):
    class RateLimit(Exception):
        status_code = 429
    def rate_limited(payload):
        raise RateLimit("rate limited")
    g = guard(tmp_path)
    response = GuardedGroqRunner(g, block_id="PILOT-01", treatment="CONDITION_A",
                                 transport=rate_limited).generate(
                                     "texto", BaselineRefineOutput, "BASELINE_REFINE")
    assert g.closed_outcome == "ABORTED_CAPACITY"
    assert response.parsed is None and response.error.startswith("PROVIDER_EXECUTION_ERROR")


def test_pilot_entry_has_no_confirmatory_or_reveal_parameter():
    parameters = set(inspect.signature(run_sacrificial_pilot).parameters)
    assert "holdout_id" not in parameters
    assert "reveal_path" not in parameters
