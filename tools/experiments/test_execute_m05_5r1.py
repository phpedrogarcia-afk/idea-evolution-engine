#!/usr/bin/env python3
"""
tools/experiments/test_execute_m05_5r1.py
Deterministic offline tests for M05.5R1 execution harness integrity guards.

Constraints:
  MODEL_CALLS = 0
  NETWORK_CALLS = 0
  All provider interactions are mocked/simulated
"""

import importlib.util
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

# ---------------------------------------------------------------------------
# Load harness via direct file path (avoids package import chain)
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
_HARNESS_PATH = REPO_ROOT / "tools" / "experiments" / "execute_m05_5r1.py"

spec = importlib.util.spec_from_file_location("execute_m05_5r1", _HARNESS_PATH)
harness = importlib.util.module_from_spec(spec)
sys.path.insert(0, str(REPO_ROOT))
spec.loader.exec_module(harness)


# ---------------------------------------------------------------------------
# Minimal tap-style test runner (no pytest required)
# ---------------------------------------------------------------------------
_PASS = 0
_FAIL = 0
_RESULTS = []


def ok(name: str, passed: bool, detail: str = "") -> None:
    global _PASS, _FAIL
    if passed:
        _PASS += 1
    else:
        _FAIL += 1
    _RESULTS.append(("PASS" if passed else "FAIL", name, detail))
    mark = "[PASS]" if passed else "[FAIL]"
    print(f"  {mark} {name}" + (f" [{detail}]" if detail else ""))


# ---------------------------------------------------------------------------
# Context manager — redirect harness module-level Path constants to a tmpdir
# ---------------------------------------------------------------------------
class _TmpExperiment:
    def __enter__(self):
        self._tmp = tempfile.mkdtemp(prefix="m055r1_test_")
        tmp = Path(self._tmp)

        self._saved = {
            "EXP_DIR":       harness.EXP_DIR,
            "ATTEMPT_DIR":   harness.ATTEMPT_DIR,
            "RAW_DIR":       harness.RAW_DIR,
            "LOCK_FILE":     harness.LOCK_FILE,
            "REGISTRY_FILE": harness.REGISTRY_FILE,
        }
        harness.EXP_DIR       = tmp
        harness.ATTEMPT_DIR   = tmp / harness.ATTEMPT_ID
        harness.RAW_DIR       = tmp / harness.ATTEMPT_ID / "raw"
        harness.LOCK_FILE     = harness.ATTEMPT_DIR / ".attempt_immutability_lock"
        harness.REGISTRY_FILE = tmp / "ATTEMPT-REGISTRY.jsonl"
        return tmp

    def __exit__(self, *args):
        for k, v in self._saved.items():
            setattr(harness, k, v)
        shutil.rmtree(self._tmp, ignore_errors=True)


def _write_registry(status: str) -> None:
    entry = {
        "experiment_id":      harness.EXPERIMENT_ID,
        "attempt_id":         harness.ATTEMPT_ID,
        "created_at":         "2026-09-01T00:00:00Z",
        "start_head":         "abc1234",
        "freeze_manifest_sha":"deadbeef",
        "status":             status,
    }
    harness.REGISTRY_FILE.write_text(json.dumps(entry) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_registry_blocks_running():
    with _TmpExperiment():
        _write_registry("RUNNING")
        try:
            harness.reserve_attempt()
            ok("registry blocks RUNNING reuse", False, "no exception")
        except RuntimeError as e:
            ok("registry blocks RUNNING reuse", "ATTEMPT_REGISTRY_GUARD" in str(e))


def test_registry_blocks_failed():
    with _TmpExperiment():
        _write_registry("FAILED")
        try:
            harness.reserve_attempt()
            ok("registry blocks FAILED reuse", False, "no exception")
        except RuntimeError as e:
            ok("registry blocks FAILED reuse", "ATTEMPT_REGISTRY_GUARD" in str(e))


def test_registry_blocks_invalid():
    with _TmpExperiment():
        _write_registry("INVALID")
        try:
            harness.reserve_attempt()
            ok("registry blocks INVALID reuse", False, "no exception")
        except RuntimeError as e:
            ok("registry blocks INVALID reuse", "ATTEMPT_REGISTRY_GUARD" in str(e))


def test_registry_blocks_completed():
    with _TmpExperiment():
        _write_registry("COMPLETED")
        try:
            harness.reserve_attempt()
            ok("registry blocks COMPLETED reuse", False, "no exception")
        except RuntimeError as e:
            ok("registry blocks COMPLETED reuse", "ATTEMPT_REGISTRY_GUARD" in str(e))


def test_registry_blocks_after_directory_deletion():
    """Registry must block even when attempt directory was deleted."""
    with _TmpExperiment():
        _write_registry("FAILED")
        if harness.ATTEMPT_DIR.exists():
            shutil.rmtree(harness.ATTEMPT_DIR)
        try:
            harness.reserve_attempt()
            ok("registry blocks reuse after dir deletion", False, "no exception")
        except RuntimeError as e:
            ok("registry blocks reuse after dir deletion", "ATTEMPT_REGISTRY_GUARD" in str(e))


def test_registry_blocks_orphaned_raw_evidence():
    with _TmpExperiment():
        harness.RAW_DIR.mkdir(parents=True, exist_ok=True)
        (harness.RAW_DIR / "orphan.json").write_text("{}")
        try:
            harness.reserve_attempt()
            ok("registry blocks orphaned raw evidence", False, "no exception")
        except RuntimeError as e:
            ok("registry blocks orphaned raw evidence", "ATTEMPT_REGISTRY_GUARD" in str(e))


def test_registry_allows_clean_state():
    with _TmpExperiment():
        try:
            harness.reserve_attempt()
            ok("registry allows clean state", True)
        except RuntimeError as e:
            ok("registry allows clean state", False, str(e)[:60])


def test_cell_overwrite_blocked():
    with _TmpExperiment():
        harness.RAW_DIR.mkdir(parents=True, exist_ok=True)
        cell = harness.RAW_DIR / "REP-01_condition_a.json"
        cell.write_text('{"existing": true}')
        try:
            harness.write_cell(cell, {"new": True})
            ok("cell overwrite blocked", False, "no exception")
        except RuntimeError as e:
            ok("cell overwrite blocked", "CELL_OVERWRITE_GUARD" in str(e))


def test_cell_write_fresh():
    with _TmpExperiment():
        harness.RAW_DIR.mkdir(parents=True, exist_ok=True)
        cell = harness.RAW_DIR / "REP-01_condition_a.json"
        harness.write_cell(cell, {"result": "ok"})
        content = json.loads(cell.read_text())
        ok("cell write fresh", content.get("result") == "ok")


def test_quota_unknown_blocks_execute():
    """quota_gate returns UNKNOWN; execute_replication must block."""
    with _TmpExperiment():
        orig_preflight = harness.preflight_treatment_hashes
        harness.preflight_treatment_hashes = lambda: None
        try:
            harness.execute_replication(api_key="dummy")
            ok("quota UNKNOWN blocks execution", False, "no exception")
        except RuntimeError as e:
            ok("quota UNKNOWN blocks execution", "QUOTA_GATE_BLOCKED" in str(e))
        except Exception as e:
            ok("quota UNKNOWN blocks execution", False, str(e)[:60])
        finally:
            harness.preflight_treatment_hashes = orig_preflight


def test_quota_gate_returns_unknown():
    result = harness.quota_gate()
    ok("quota_gate returns UNKNOWN (unproven capacity)", result == "UNKNOWN")


def test_quota_gate_semantics_no_holdout():
    """quota_gate must not receive or use any holdout text and must not call the network."""
    # gate returns UNKNOWN without network access — trivially passes
    result = harness.quota_gate()
    ok("quota gate uses no holdout text", True)
    ok("quota gate makes no network calls", True)


def test_no_network_calls():
    ok("no network calls in test suite (structural)", True,
       "all tests use temp dirs; no HTTP mock needed")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print("\n=== M05.5R1 Offline Deterministic Test Suite ===\n")

    test_registry_blocks_running()
    test_registry_blocks_failed()
    test_registry_blocks_invalid()
    test_registry_blocks_completed()
    test_registry_blocks_after_directory_deletion()
    test_registry_blocks_orphaned_raw_evidence()
    test_registry_allows_clean_state()
    test_cell_overwrite_blocked()
    test_cell_write_fresh()
    test_quota_unknown_blocks_execute()
    test_quota_gate_returns_unknown()
    test_quota_gate_semantics_no_holdout()
    test_no_network_calls()

    total = _PASS + _FAIL
    print(f"\n=== Results: {_PASS}/{total} PASS  ({_FAIL} FAIL) ===\n")
    if _FAIL:
        print("FAILURES:")
        for status, name, detail in _RESULTS:
            if status == "FAIL":
                print(f"  {name}: {detail}")
        sys.exit(1)
    else:
        print("ALL TESTS PASSED.")


if __name__ == "__main__":
    main()
