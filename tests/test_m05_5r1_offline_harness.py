"""Synthetic-only R3 tests; all namespaces are supplied by pytest."""

from dataclasses import replace
from datetime import datetime, timedelta, timezone
import json

import pytest

from tools.experiments.execute_m05_5r1 import (
    ATTEMPT_ID, MAX_REQUEST_COUNT, VALID_OUTCOMES, SealedHoldoutBoundary,
    authorize_start, build_capacity_envelope, create_start_receipt,
    evaluate_capacity, make_capacity_receipt, make_holdout_receipt,
    verify_start_receipt,
)

NOW = datetime(2026, 9, 1, tzinfo=timezone.utc)
PROVENANCE = {"source_commit": "synthetic-source", "freeze_manifest_sha256": "a" * 64, "config_sha256": "b" * 64}


def envelope():
    return build_capacity_envelope([10] * MAX_REQUEST_COUNT, [20] * MAX_REQUEST_COUNT, "synthetic-tokenizer-v1")


def capacity(item):
    return make_capacity_receipt(item, available_tpd=item.tpd_required + 1, available_tpm=item.tpm_required + 1,
                                 available_rpd=item.rpd_required + 1, available_rpm=item.rpm_required + 1,
                                 observed_at=NOW, expires_at=NOW + timedelta(hours=1), source="SYNTHETIC")


def holdout():
    items = [f"synthetic-item-{number}" for number in range(8)]
    return items, make_holdout_receipt(items, "synthetic-guardian", NOW)


def test_receipt_create_read_collision_tamper_and_substitution(tmp_path):
    receipt = create_start_receipt(tmp_path, ATTEMPT_ID, PROVENANCE)
    assert verify_start_receipt(receipt, PROVENANCE)["attempt_id"] == ATTEMPT_ID
    with pytest.raises(FileExistsError, match="ATTEMPT_NAMESPACE_COLLISION"):
        create_start_receipt(tmp_path, ATTEMPT_ID, PROVENANCE)
    data = json.loads(receipt.read_text(encoding="utf-8"))
    data["body"]["config_sha256"] = "c" * 64
    receipt.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(ValueError, match="START_RECEIPT_TAMPERED"):
        verify_start_receipt(receipt, PROVENANCE)
    second = create_start_receipt(tmp_path, "SYNTHETIC-002", PROVENANCE)
    with pytest.raises(ValueError, match="START_RECEIPT_IDENTITY_OR_CONFIG_MISMATCH"):
        verify_start_receipt(second, {**PROVENANCE, "source_commit": "other"})


def test_real_attempt_is_not_modified(tmp_path):
    real = tmp_path / ATTEMPT_ID
    real.mkdir()
    sentinel = real / "sentinel"
    sentinel.write_text("unchanged", encoding="utf-8")
    create_start_receipt(tmp_path, "SYNTHETIC-001", PROVENANCE)
    assert sentinel.read_text(encoding="utf-8") == "unchanged"
    assert not (real / "start-receipt.json").exists()


def test_holdout_sealing_development_denial_and_audit(tmp_path):
    items, receipt = holdout()
    assert all(item not in json.dumps(receipt.__dict__) for item in items)
    boundary = SealedHoldoutBoundary(receipt, lambda: items)
    with pytest.raises(PermissionError, match="HOLDOUT_ACCESS_DENIED"):
        boundary.access_for_evaluation("DEVELOPMENT", tmp_path / "audit.jsonl")
    assert boundary.access_for_evaluation("EVALUATION", tmp_path / "audit.jsonl") == items
    audit = (tmp_path / "audit.jsonl").read_text(encoding="utf-8")
    assert receipt.content_sha256 in audit and all(item not in audit for item in items)


def test_capacity_ready_and_insufficient_tpd_tpm():
    item = envelope()
    assert evaluate_capacity(item, capacity(item), NOW) == "READY"
    low_tpd = make_capacity_receipt(item, available_tpd=item.tpd_required - 1, available_tpm=item.tpm_required + 1,
                                    available_rpd=item.rpd_required + 1, available_rpm=item.rpm_required + 1,
                                    observed_at=NOW, expires_at=NOW + timedelta(hours=1), source="SYNTHETIC")
    low_tpm = make_capacity_receipt(item, available_tpd=item.tpd_required + 1, available_tpm=item.tpm_required - 1,
                                    available_rpd=item.rpd_required + 1, available_rpm=item.rpm_required + 1,
                                    observed_at=NOW, expires_at=NOW + timedelta(hours=1), source="SYNTHETIC")
    assert evaluate_capacity(item, low_tpd, NOW) == "NOT_READY_TPD"
    assert evaluate_capacity(item, low_tpm, NOW) == "NOT_READY_TPM"


def test_capacity_missing_unverifiable_stale_and_corrupt_are_denied():
    item, good = envelope(), capacity(envelope())
    assert evaluate_capacity(item, None, NOW) == "NOT_READY_CAPACITY"
    assert evaluate_capacity(item, replace(good, verified=False), NOW) == "NOT_READY_CAPACITY"
    stale = make_capacity_receipt(item, available_tpd=item.tpd_required + 1, available_tpm=item.tpm_required + 1,
                                  available_rpd=item.rpd_required + 1, available_rpm=item.rpm_required + 1,
                                  observed_at=NOW - timedelta(hours=2), expires_at=NOW - timedelta(seconds=1), source="SYNTHETIC")
    assert evaluate_capacity(item, stale, NOW) == "NOT_READY_CAPACITY"
    assert evaluate_capacity(item, replace(good, integrity_sha256="0" * 64), NOW) == "NOT_READY_CAPACITY"


@pytest.mark.parametrize("broken", ["provenance", "holdout", "capacity", "collision", "attempt_id"])
def test_start_gate_denies_every_missing_or_invalid_prerequisite(tmp_path, broken):
    items, sealed = holdout()
    item = envelope()
    if broken == "collision":
        (tmp_path / "SYNTHETIC").mkdir()
    decision, receipt, reasons = authorize_start(
        tmp_path, "" if broken == "attempt_id" else "SYNTHETIC",
        {} if broken == "provenance" else PROVENANCE,
        replace(sealed, content_sha256="0" * 64) if broken == "holdout" else sealed,
        item, None if broken == "capacity" else capacity(item), NOW,
    )
    assert decision == "START_DENIED" and receipt is None and reasons and items[0].startswith("synthetic")


def test_start_gate_accepts_complete_synthetic_preflight(tmp_path):
    _, sealed = holdout()
    item = envelope()
    decision, receipt, reasons = authorize_start(tmp_path, "SYNTHETIC-ALLOWED", PROVENANCE, sealed, item, capacity(item), NOW)
    assert decision == "START_ALLOWED" and receipt is not None and reasons == []


def test_outcomes_are_distinct_and_complete():
    assert VALID_OUTCOMES == {"SUPPORTED", "NOT_SUPPORTED", "INCONCLUSIVE", "INVALID_EXECUTION", "ABORTED_CAPACITY", "NO_USEFUL_WORK_FOUND"}
