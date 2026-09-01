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

import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

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
    return "UNKNOWN"


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
    key = api_key or os.environ.get("GROQ_API_KEY")
    if not key:
        raise ValueError("GROQ_API_KEY_MISSING")

    preflight_treatment_hashes()

    quota_status = quota_gate()
    if quota_status != "YES":
        raise RuntimeError(
            f"QUOTA_GATE_BLOCKED: PROVIDER_QUOTA_READY={quota_status}. "
            "Blocked until provider capacity is independently verified."
        )

    reserve_attempt()
    create_lock()

    from src.idea_evolution.providers.native import NativeModelRunner  # noqa
    from src.idea_evolution.orchestration.baseline import BaselineRunner  # noqa
    from src.idea_evolution.orchestration.simple_loop import SimpleLoopRunner  # noqa
    from src.idea_evolution.orchestration.lean_loop import LeanLoopRunner  # noqa

    print("TREATMENT_EXECUTION_PLANE: Stub. Pending holdout freeze + quota evidence.")
    update_attempt_status("COMPLETED")


if __name__ == "__main__":
    print("M05.5R1 harness loaded. Do not execute until holdouts frozen + quota proven.")
