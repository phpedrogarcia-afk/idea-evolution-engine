#!/usr/bin/env python3
"""
tools/experiments/execute_m05_5r1.py
M05.5R1 Execution Harness with integrity guards.

ARCHITECTURE
============
PRE_EXECUTION_INTEGRITY_PLANE
  1. preflight_treatment_hashes()
  2. quota_gate()
  3. reserve_attempt()
  4. create_lock()

TREATMENT_EXECUTION_PLANE
  5. run_cells()
  6. write_cell()

Treatment runner imports are lazy (inside execute_replication) so
module-level constants are always reachable on bare import for tests.

Invariants:
  EXECUTION_PLANE_HAS_NO_BLIND_KNOWLEDGE = True
  TREATMENT_SEMANTICS_UNCHANGED_FROM_M05_4 = True
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(line_buffering=True)

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

# ---------------------------------------------------------------------------
# Constants 
# ---------------------------------------------------------------------------
EXPERIMENT_ID     = "EXP-M05.5R1-CONTROLLED-REPLICATION-20260901"
ATTEMPT_ID        = "REAL-EXECUTION-ATTEMPT-001"
EXPECTED_PROVIDER = "groq"
EXPECTED_MODEL    = "openai/gpt-oss-120b"
CELL_COUNT = 24
MAX_REQUEST_COUNT = 104
VALID_OUTCOMES = {
    "SUPPORTED", "NOT_SUPPORTED", "INCONCLUSIVE", "INVALID_EXECUTION",
    "ABORTED_CAPACITY", "NO_USEFUL_WORK_FOUND",
}

EXP_DIR         = REPO_ROOT / "experiments" / EXPERIMENT_ID
ATTEMPT_DIR     = EXP_DIR / ATTEMPT_ID
RAW_DIR         = ATTEMPT_DIR / "raw"
LOCK_FILE       = ATTEMPT_DIR / ".attempt_immutability_lock"
REGISTRY_FILE   = EXP_DIR / "ATTEMPT-REGISTRY.jsonl"

M054_FREEZE_MANIFEST = (
    REPO_ROOT
    / "experiments"
    / "EXP-M05.4-PROSPECTIVE-RERUN-20260829"
    / "RERUN-FREEZE-MANIFEST.json"
)

TREATMENT_CRITICAL_FILES: Dict[str, Path] = {
    "baseline.py":             REPO_ROOT / "src/idea_evolution/orchestration/baseline.py",
    "simple_loop.py":          REPO_ROOT / "src/idea_evolution/orchestration/simple_loop.py",
    "lean_loop.py":            REPO_ROOT / "src/idea_evolution/orchestration/lean_loop.py",
    "early_epistemic_gate.py": REPO_ROOT / "src/idea_evolution/domain/early_epistemic_gate.py",
    "routing.py":              REPO_ROOT / "src/idea_evolution/config/routing.py",
    "native.py":               REPO_ROOT / "src/idea_evolution/providers/native.py",
    "router.py":               REPO_ROOT / "src/idea_evolution/providers/router.py",
}


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

def sha256_file(path: Path) -> str:
    data = path.read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha256(data).hexdigest()


def _git_head() -> str:
    try:
        r = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True, text=True, cwd=str(REPO_ROOT)
        )
        return r.stdout.strip() or "UNKNOWN"
    except Exception:
        return "UNKNOWN"


# ---------------------------------------------------------------------------
# PRE_EXECUTION_INTEGRITY_PLANE
# ---------------------------------------------------------------------------

def preflight_treatment_hashes() -> None:
    if not M054_FREEZE_MANIFEST.exists():
        raise RuntimeError(
            f"PREFLIGHT_FAIL: M05.4 freeze manifest not found: {M054_FREEZE_MANIFEST}"
        )
    manifest = json.loads(M054_FREEZE_MANIFEST.read_text(encoding="utf-8"))
    ref_hashes: Dict[str, str] = manifest.get("execution_critical_hashes", {})

    mismatches: List[str] = []
    for name, path in TREATMENT_CRITICAL_FILES.items():
        ref = ref_hashes.get(name)
        if ref is None:
            print(f"  [WARN] {name}: not in M05.4 freeze manifest")
            continue
        cur = sha256_file(path)
        if cur != ref:
            mismatches.append(f"{name}: ref={ref[:16]} cur={cur[:16]}")

    if mismatches:
        raise RuntimeError(
            "PREFLIGHT_FAIL: TREATMENT_HASH_MISMATCH\n" + "\n".join(mismatches)
        )
    print("PREFLIGHT_OK: All treatment-critical hashes match M05.4 freeze manifest.")


def quota_gate() -> str:
    """Offline R3 must never infer provider capacity from a network probe."""
    return "UNKNOWN"


def _canonical_hash(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class HoldoutReceipt:
    content_sha256: str
    count: int
    guardian_id: str
    sealed_at: str
    integrity_sha256: str


def make_holdout_receipt(items: Sequence[str], guardian_id: str, sealed_at: datetime) -> HoldoutReceipt:
    payload = {"content_sha256": _canonical_hash(list(items)), "count": len(items),
               "guardian_id": guardian_id, "sealed_at": sealed_at.isoformat()}
    return HoldoutReceipt(**payload, integrity_sha256=_canonical_hash(payload))


def _valid_holdout_receipt(receipt: HoldoutReceipt) -> bool:
    payload = asdict(receipt)
    integrity = payload.pop("integrity_sha256")
    return bool(receipt.content_sha256 and receipt.guardian_id and receipt.count == 8 and integrity == _canonical_hash(payload))


class SealedHoldoutBoundary:
    """Contents cross the boundary only in the explicit evaluation phase."""

    def __init__(self, receipt: HoldoutReceipt, loader: Callable[[], Sequence[str]]):
        self.receipt = receipt
        self._loader = loader

    def access_for_evaluation(self, phase: str, audit_path: Path) -> list[str]:
        if phase != "EVALUATION":
            raise PermissionError("HOLDOUT_ACCESS_DENIED")
        if not _valid_holdout_receipt(self.receipt):
            raise ValueError("HOLDOUT_RECEIPT_INVALID")
        items = list(self._loader())
        if _canonical_hash(items) != self.receipt.content_sha256 or len(items) != self.receipt.count:
            raise ValueError("HOLDOUT_RECEIPT_MISMATCH")
        audit_path.parent.mkdir(parents=True, exist_ok=True)
        event = {"event": "holdout_access", "phase": phase, "content_sha256": self.receipt.content_sha256,
                 "count": self.receipt.count, "guardian_id": self.receipt.guardian_id}
        with audit_path.open("a", encoding="utf-8") as output:
            output.write(json.dumps(event, sort_keys=True) + "\n")
        return items


@dataclass(frozen=True)
class CapacityEnvelope:
    request_count: int
    input_tokens: int
    output_tokens: int
    tpd_required: int
    tpm_required: int
    rpd_required: int
    rpm_required: int
    tokenizer_id: str

    @property
    def sha256(self) -> str:
        return _canonical_hash(asdict(self))


def build_capacity_envelope(inputs: Sequence[int], outputs: Sequence[int], tokenizer_id: str) -> CapacityEnvelope:
    if len(inputs) != MAX_REQUEST_COUNT or len(outputs) != MAX_REQUEST_COUNT:
        raise ValueError("CAPACITY_ENVELOPE_REQUEST_COUNT_MISMATCH")
    if not tokenizer_id or any(value < 0 for value in [*inputs, *outputs]):
        raise ValueError("CAPACITY_ENVELOPE_INVALID")
    input_total, output_total = sum(inputs), sum(outputs)
    return CapacityEnvelope(MAX_REQUEST_COUNT, input_total, output_total, input_total + output_total,
                            max(a + b for a, b in zip(inputs, outputs)), MAX_REQUEST_COUNT, 1, tokenizer_id)


@dataclass(frozen=True)
class CapacityReceipt:
    envelope_sha256: str
    available_tpd: int
    available_tpm: int
    available_rpd: int
    available_rpm: int
    observed_at: str
    expires_at: str
    source: str
    verified: bool
    integrity_sha256: str


def make_capacity_receipt(envelope: CapacityEnvelope, *, available_tpd: int, available_tpm: int,
                          available_rpd: int, available_rpm: int, observed_at: datetime,
                          expires_at: datetime, source: str) -> CapacityReceipt:
    payload = {"envelope_sha256": envelope.sha256, "available_tpd": available_tpd, "available_tpm": available_tpm,
               "available_rpd": available_rpd, "available_rpm": available_rpm, "observed_at": observed_at.isoformat(),
               "expires_at": expires_at.isoformat(), "source": source, "verified": True}
    return CapacityReceipt(**payload, integrity_sha256=_canonical_hash(payload))


def evaluate_capacity(envelope: CapacityEnvelope, receipt: CapacityReceipt | None, now: datetime) -> str:
    if receipt is None or not receipt.verified or receipt.envelope_sha256 != envelope.sha256 or not receipt.source:
        return "NOT_READY_CAPACITY"
    try:
        payload = asdict(receipt)
        integrity = payload.pop("integrity_sha256")
        expired = datetime.fromisoformat(receipt.expires_at.replace("Z", "+00:00")) <= now
    except (TypeError, ValueError):
        return "NOT_READY_CAPACITY"
    if integrity != _canonical_hash(payload) or expired:
        return "NOT_READY_CAPACITY"
    for available, required, status in ((receipt.available_tpd, envelope.tpd_required, "NOT_READY_TPD"),
                                       (receipt.available_tpm, envelope.tpm_required, "NOT_READY_TPM"),
                                       (receipt.available_rpd, envelope.rpd_required, "NOT_READY_RPD"),
                                       (receipt.available_rpm, envelope.rpm_required, "NOT_READY_RPM")):
        if available < required:
            return status
    return "READY"


def _start_payload(attempt_id: str, provenance: Dict[str, str]) -> Dict[str, object]:
    if not all(provenance.get(key) for key in ("source_commit", "freeze_manifest_sha256", "config_sha256")):
        raise ValueError("START_RECEIPT_PROVENANCE_MISSING")
    body: Dict[str, object] = {"experiment_id": EXPERIMENT_ID, "attempt_id": attempt_id, **provenance}
    return {"body": body, "integrity_sha256": _canonical_hash(body)}


def create_start_receipt(namespace: Path, attempt_id: str, provenance: Dict[str, str]) -> Path:
    if not attempt_id:
        raise ValueError("ATTEMPT_ID_INVALID")
    attempt = namespace / attempt_id
    try:
        attempt.mkdir(parents=False)
    except FileExistsError as error:
        raise FileExistsError("ATTEMPT_NAMESPACE_COLLISION") from error
    receipt = attempt / "start-receipt.json"
    receipt.write_text(json.dumps(_start_payload(attempt_id, provenance), sort_keys=True), encoding="utf-8")
    return receipt


def verify_start_receipt(receipt: Path, expected_provenance: Dict[str, str]) -> Dict[str, object]:
    data = json.loads(receipt.read_text(encoding="utf-8"))
    body = data.get("body")
    if not isinstance(body, dict) or data.get("integrity_sha256") != _canonical_hash(body):
        raise ValueError("START_RECEIPT_TAMPERED")
    expected = _start_payload(str(body.get("attempt_id", "")), expected_provenance)["body"]
    if body != expected:
        raise ValueError("START_RECEIPT_IDENTITY_OR_CONFIG_MISMATCH")
    return body


def authorize_start(namespace: Path, attempt_id: str, provenance: Dict[str, str], holdout: HoldoutReceipt,
                    envelope: CapacityEnvelope, capacity: CapacityReceipt | None, now: datetime) -> tuple[str, Path | None, List[str]]:
    reasons: List[str] = []
    if not attempt_id:
        reasons.append("ATTEMPT_ID_INVALID")
    elif (namespace / attempt_id).exists():
        reasons.append("ATTEMPT_NAMESPACE_NOT_FRESH")
    if not all(provenance.get(key) for key in ("source_commit", "freeze_manifest_sha256", "config_sha256")):
        reasons.append("PROVENANCE_MISSING")
    if not _valid_holdout_receipt(holdout):
        reasons.append("HOLDOUT_RECEIPT_INVALID")
    capacity_status = evaluate_capacity(envelope, capacity, now)
    if capacity_status != "READY":
        reasons.append(capacity_status)
    if reasons:
        return "START_DENIED", None, reasons
    return "START_ALLOWED", create_start_receipt(namespace, attempt_id, provenance), []


def _registry_entries() -> List[Dict[str, Any]]:
    if not REGISTRY_FILE.exists():
        return []
    entries: List[Dict[str, Any]] = []
    for line in REGISTRY_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            entries.append(json.loads(line))
    return entries


def reserve_attempt() -> None:
    for entry in _registry_entries():
        if entry.get("attempt_id") == ATTEMPT_ID:
            status = entry.get("status", "UNKNOWN")
            raise RuntimeError(
                f"ATTEMPT_REGISTRY_GUARD: Attempt '{ATTEMPT_ID}' already registered "
                f"with status={status}. Directory presence is irrelevant. "
                "Create a new attempt ID (e.g. REAL-EXECUTION-ATTEMPT-002)."
            )

    if RAW_DIR.exists() and list(RAW_DIR.glob("*.json")):
        raise RuntimeError(
            "ATTEMPT_REGISTRY_GUARD: Orphaned raw evidence exists for this attempt "
            "without a registry entry. Investigate before proceeding."
        )

    EXP_DIR.mkdir(parents=True, exist_ok=True)
    entry: Dict[str, Any] = {
        "experiment_id":      EXPERIMENT_ID,
        "attempt_id":         ATTEMPT_ID,
        "created_at":         datetime.utcnow().isoformat() + "Z",
        "start_head":         _git_head(),
        "freeze_manifest_sha": (
            sha256_file(M054_FREEZE_MANIFEST) if M054_FREEZE_MANIFEST.exists() else "UNKNOWN"
        ),
        "status":             "RUNNING",
    }
    with open(REGISTRY_FILE, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry) + "\n")
    print(f"REGISTRY: Attempt '{ATTEMPT_ID}' reserved.")


def create_lock() -> None:
    ATTEMPT_DIR.mkdir(parents=True, exist_ok=True)
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    lock_data: Dict[str, Any] = {
        "experiment_id":      EXPERIMENT_ID,
        "attempt_id":         ATTEMPT_ID,
        "start_timestamp":    datetime.utcnow().isoformat() + "Z",
        "start_head":         _git_head(),
        "freeze_manifest_sha": (
            sha256_file(M054_FREEZE_MANIFEST) if M054_FREEZE_MANIFEST.exists() else "UNKNOWN"
        ),
    }
    LOCK_FILE.write_text(json.dumps(lock_data, indent=2), encoding="utf-8")
    print("LOCK: Per-attempt immutability lock written.")


def update_attempt_status(status: str) -> None:
    if not REGISTRY_FILE.exists():
        return
    lines = REGISTRY_FILE.read_text(encoding="utf-8").splitlines()
    updated: List[str] = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        entry = json.loads(line)
        if entry.get("attempt_id") == ATTEMPT_ID:
            entry["status"] = status
            entry["completed_at"] = datetime.utcnow().isoformat() + "Z"
        updated.append(json.dumps(entry))
    REGISTRY_FILE.write_text("\n".join(updated) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# TREATMENT_EXECUTION_PLANE
# ---------------------------------------------------------------------------

def write_cell(path: Path, data: Dict[str, Any]) -> None:
    if path.exists():
        raise RuntimeError(
            f"CELL_OVERWRITE_GUARD: Cell '{path.name}' already exists. "
            "Overwriting is forbidden."
        )
    path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8"
    )


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def execute_replication(api_key: Optional[str] = None) -> None:
    raise RuntimeError("OFFLINE_HARNESS_ONLY: separate execution authority is required")


if __name__ == "__main__":
    print("OFFLINE_HARNESS_ONLY: no provider, model, or holdout execution is available.")
