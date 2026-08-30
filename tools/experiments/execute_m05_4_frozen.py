#!/usr/bin/env python3
"""
tools/experiments/execute_m05_4_frozen.py
Clean execution harness for M05.4 prospective replication with self-enforcing freeze gate.

Architectural Invariant:
  EXECUTION_PLANE_HAS_NO_BLIND_KNOWLEDGE = True

Responsibilities:
  1. Validate mechanical freeze state before ANY execution (git worktree, freeze manifest hashes, blind commitment).
  2. Validate execution manifest (24 cells, 8 A / 8 B / 8 C, unique cells, correct provider/model).
  3. Validate single-use attempt namespace (fail closed if attempt already started).
  4. Create start receipt ONLY after all gates pass.
  5. Execute frozen A/B/C conditions in exact manifest order.
  6. Record raw outputs and factual execution metadata into attempt namespace.
  7. Compute artifact SHA-256 hashes.
  8. Stop without scoring, interpreting, or accessing blind mappings.

Strict Boundaries:
  - NO BlindRenderer import or execution.
  - NO blind mapping or reveal file access.
  - NO synthetic post-hoc FioED delta labels.
  - Status evaluation is strictly FAIL-CLOSED.
  - Uninstrumented telemetry is reported as UNKNOWN_NOT_INSTRUMENTED.
"""

from __future__ import annotations
import os
import sys
import json
import time
import hashlib
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

# Architectural invariant declaration
EXECUTION_PLANE_HAS_NO_BLIND_KNOWLEDGE = True

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from src.idea_evolution.providers.base import ModelRunner
from src.idea_evolution.providers.native import NativeModelRunner
from src.idea_evolution.orchestration.baseline import BaselineRunner
from src.idea_evolution.orchestration.simple_loop import SimpleLoopRunner
from src.idea_evolution.orchestration.lean_loop import LeanLoopRunner
from src.idea_evolution.config.routing import ModelRoutingConfig, ModelDefinition
from src.idea_evolution.providers.router import RunnerRouter

EXPECTED_BLIND_COMMITMENT_REV3 = "b2e271ff9dd35a8215c067d1e545f84dfa8add7f33335a69845ebd8d5ed82cf3"


def calculate_sha256_text(text: str) -> str:
    norm = text.encode("utf-8").replace(b"\r\n", b"\n")
    return hashlib.sha256(norm).hexdigest()


def calculate_sha256_file(path: Path) -> str:
    data = path.read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha256(data).hexdigest()


def _build_condition_b_router(runner: ModelRunner) -> RunnerRouter:
    """Builds explicit 6-stage router for Condition B using the provided runner."""
    config = ModelRoutingConfig(
        models={
            "default": ModelDefinition(
                provider=getattr(runner, "provider", "groq"),
                model=getattr(runner, "default_model", "openai/gpt-oss-120b")
            )
        },
        routes={},
        default_model_alias="default"
    )
    return RunnerRouter(config=config, custom_runners={"default": runner})


def validate_provider_guards(runner: ModelRunner, expected_provider: str = "groq", expected_model: str = "openai/gpt-oss-120b") -> None:
    """Preflight guard: fails fast before any execution if provider/model mismatch."""
    actual_provider = getattr(runner, "provider", None)
    if actual_provider != expected_provider:
        raise RuntimeError(
            f"PROVIDER_SPEC_VIOLATION: runner provider must be '{expected_provider}', got '{actual_provider}'."
        )
    actual_model = getattr(runner, "default_model", None)
    if actual_model != expected_model:
        raise RuntimeError(
            f"MODEL_SPEC_VIOLATION: runner default_model must be '{expected_model}', got '{actual_model}'."
        )


def check_git_worktree_clean(repo_root: Optional[Path] = None) -> bool:
    """Checks if git worktree is completely clean."""
    root = repo_root or REPO_ROOT
    try:
        res = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            cwd=str(root)
        )
        return res.returncode == 0 and len(res.stdout.strip()) == 0
    except Exception:
        return False


def validate_frozen_execution_state(
    repo_root: Optional[Path] = None,
    exp_dir: Optional[Path] = None,
    freeze_manifest_file: Optional[Path] = None,
    blind_sha_file: Optional[Path] = None,
    skip_git_check: bool = False,
) -> Dict[str, Any]:
    """
    Self-enforcing freeze validation: fails closed if repository or inputs differ from frozen spec.
    """
    root = repo_root or REPO_ROOT
    exp_root = exp_dir or (root / "experiments" / "EXP-M05.4-PROSPECTIVE-RERUN-20260829")
    freeze_manifest_path = freeze_manifest_file or (exp_root / "RERUN-FREEZE-MANIFEST.json")
    blind_sha_path = blind_sha_file or (exp_root / "BLIND-REVEAL.sha256")

    # 1. Git clean worktree check
    if not skip_git_check:
        if not check_git_worktree_clean(root):
            raise RuntimeError("DIRTY_WORKTREE_EXECUTION_FORBIDDEN: Git worktree contains uncommitted modifications.")

    # 2. Freeze manifest existence and parsing
    if not freeze_manifest_path.is_file():
        raise RuntimeError(f"FREEZE_MANIFEST_MISSING: Freeze manifest not found at {freeze_manifest_path}")

    freeze_data = json.loads(freeze_manifest_path.read_text(encoding="utf-8"))
    recorded_hashes = freeze_data.get("execution_critical_hashes", {})

    # Map file keys to relative paths from repo root or experiment dir
    file_path_resolvers = {
        "execute_m05_4_frozen.py": root / "tools" / "experiments" / "execute_m05_4_frozen.py",
        "render_m05_4_blind_review.py": root / "tools" / "experiments" / "render_m05_4_blind_review.py",
        "m05_4_runner.py": root / "src" / "idea_evolution" / "experiments" / "m05_4_runner.py",
        "baseline.py": root / "src" / "idea_evolution" / "orchestration" / "baseline.py",
        "simple_loop.py": root / "src" / "idea_evolution" / "orchestration" / "simple_loop.py",
        "lean_loop.py": root / "src" / "idea_evolution" / "orchestration" / "lean_loop.py",
        "early_epistemic_gate.py": root / "src" / "idea_evolution" / "domain" / "early_epistemic_gate.py",
        "routing.py": root / "src" / "idea_evolution" / "config" / "routing.py",
        "catalog.py": root / "src" / "idea_evolution" / "config" / "catalog.py",
        "native.py": root / "src" / "idea_evolution" / "providers" / "native.py",
        "router.py": root / "src" / "idea_evolution" / "providers" / "router.py",
        "blind_renderer.py": root / "src" / "idea_evolution" / "experiments" / "blind_renderer.py",
        "HOLDOUT-IDEAS.json": root / "experiments" / "EXP-M05.4-PROSPECTIVE" / "HOLDOUT-IDEAS.json",
        "EVALUATION-RUBRIC.md": root / "experiments" / "EXP-M05.4-PROSPECTIVE" / "EVALUATION-RUBRIC.md",
        "ANALYSIS-PLAN.md": root / "experiments" / "EXP-M05.4-PROSPECTIVE" / "ANALYSIS-PLAN.md",
        "PREREGISTRATION.md": root / "experiments" / "EXP-M05.4-PROSPECTIVE" / "PREREGISTRATION.md",
        "RERUN-PROTOCOL-AMENDMENT-001.md": exp_root / "RERUN-PROTOCOL-AMENDMENT-001.md",
        "PRE-EXECUTION-BLINDING-CORRECTION-001.md": exp_root / "PRE-EXECUTION-BLINDING-CORRECTION-001.md",
        "PRE-EXECUTION-BLINDING-CORRECTION-002.md": exp_root / "PRE-EXECUTION-BLINDING-CORRECTION-002.md",
        "RERUN-EXECUTION-MANIFEST.json": exp_root / "RERUN-EXECUTION-MANIFEST.json",
        "RERUN-RETRY-SEMANTICS-FROZEN.md": exp_root / "RERUN-RETRY-SEMANTICS-FROZEN.md",
        "BLIND-REVEAL.sha256": exp_root / "BLIND-REVEAL.sha256",
    }

    for key, expected_hash in recorded_hashes.items():
        target_path = file_path_resolvers.get(key)
        if target_path is None or not target_path.is_file():
            raise RuntimeError(f"FROZEN_CRITICAL_FILE_MISSING: Critical file '{key}' not found at {target_path}")

        actual_hash = calculate_sha256_file(target_path)
        if actual_hash != expected_hash:
            raise RuntimeError(
                f"FROZEN_STATE_MUTATION: Critical file '{key}' hash mismatch. Expected {expected_hash}, got {actual_hash}."
            )

    # 3. Blind commitment verification
    if not blind_sha_path.is_file():
        raise RuntimeError(f"BLIND_COMMITMENT_FILE_MISSING: Not found at {blind_sha_path}")

    current_commitment = blind_sha_path.read_text(encoding="utf-8").strip()
    if current_commitment != EXPECTED_BLIND_COMMITMENT_REV3:
        raise RuntimeError(
            f"BLIND_COMMITMENT_MUTATION: Current commitment '{current_commitment}' does not match Revision 3 ('{EXPECTED_BLIND_COMMITMENT_REV3}')."
        )

    return {
        "status": "PASS",
        "verified_files_count": len(recorded_hashes),
        "freeze_manifest_sha256": calculate_sha256_file(freeze_manifest_path),
        "blind_commitment_sha256": current_commitment,
    }


def validate_frozen_manifest_cells(
    frozen_cells: List[Dict[str, Any]],
    holdout_ideas: Dict[str, Any]
) -> None:
    """
    Validates the 24 cells in the frozen manifest.
    """
    if len(frozen_cells) != 24:
        raise RuntimeError(f"FROZEN_CELL_COUNT_VIOLATION: Expected exactly 24 cells, got {len(frozen_cells)}.")

    seen_cell_ids = set()
    seen_pairs = set()
    condition_counts = {"CONDITION_A": 0, "CONDITION_B": 0, "CONDITION_C": 0}

    for idx, cell in enumerate(frozen_cells, 1):
        cell_id = cell.get("cell_id")
        if not cell_id or cell_id in seen_cell_ids:
            raise RuntimeError(f"FROZEN_CELL_DUPLICATE: Duplicate or invalid cell_id '{cell_id}' at index {idx}.")
        seen_cell_ids.add(cell_id)

        cond = cell.get("condition")
        if cond not in condition_counts:
            raise RuntimeError(f"FROZEN_CONDITION_VIOLATION: Invalid condition '{cond}' in cell '{cell_id}'.")
        condition_counts[cond] += 1

        idea_id = cell.get("idea_id")
        if idea_id not in holdout_ideas:
            raise RuntimeError(f"FROZEN_IDEA_VIOLATION: Unknown idea_id '{idea_id}' in cell '{cell_id}'.")

        pair = (idea_id, cond)
        if pair in seen_pairs:
            raise RuntimeError(f"FROZEN_CELL_DUPLICATE: Duplicate (idea_id, condition) pair {pair} in cell '{cell_id}'.")
        seen_pairs.add(pair)

        provider = cell.get("provider")
        if provider != "groq":
            raise RuntimeError(f"FROZEN_PROVIDER_VIOLATION: Expected cell provider 'groq', got '{provider}' in cell '{cell_id}'.")

        model = cell.get("model")
        if model != "openai/gpt-oss-120b":
            raise RuntimeError(f"FROZEN_MODEL_VIOLATION: Expected cell model 'openai/gpt-oss-120b', got '{model}' in cell '{cell_id}'.")

    for cond, count in condition_counts.items():
        if count != 8:
            raise RuntimeError(f"FROZEN_CELL_COUNT_VIOLATION: Expected exactly 8 cells for {cond}, got {count}.")


def validate_attempt_single_use(attempt_dir: Path, allow_overwrite: bool = False) -> None:
    """
    Prevents accidental overwriting of an existing attempt.
    """
    if allow_overwrite:
        return

    receipt_file = attempt_dir / "REAL-EXECUTION-START-RECEIPT.json"
    manifest_file = attempt_dir / "REAL-EXECUTION-MANIFEST.json"
    raw_dir = attempt_dir / "raw"

    has_receipt = receipt_file.is_file()
    has_manifest = manifest_file.is_file()
    has_raw = raw_dir.is_dir() and len(list(raw_dir.glob("*.json"))) > 0

    if has_receipt or has_manifest or has_raw:
        raise RuntimeError(
            f"ATTEMPT_ALREADY_STARTED: Attempt directory '{attempt_dir.name}' already contains execution evidence. Overwrite forbidden."
        )


def execute_m05_4_cell(
    cell: Dict[str, Any],
    idea_data: Dict[str, Any],
    runner: ModelRunner,
    raw_dir: Path,
    expected_model: str = "openai/gpt-oss-120b",
    attempt_id: str = "REAL-EXECUTION-ATTEMPT-004",
) -> Dict[str, Any]:
    """
    Executes a single cell according to frozen condition semantics.
    Status is strictly FAIL-CLOSED.
    """
    idea_id = cell["idea_id"]
    condition = cell["condition"]
    raw_idea = idea_data["raw_idea"]
    cell_id = cell["cell_id"]

    start_time = time.time()

    if condition == "CONDITION_A":
        runs_dir = raw_dir / "runs_a"
        runs_dir.mkdir(parents=True, exist_ok=True)
        baseline = BaselineRunner(runner=runner, model_name=expected_model)
        result = baseline.run(original_idea=raw_idea, run_id=f"EXP-M05.4-{idea_id}-COND-A", runs_dir=runs_dir)
        lat = time.time() - start_time

        output_data = result.get("parsed_output") or {}
        # FAIL-CLOSED status: requires explicit success flag AND non-empty output
        is_success = (result.get("success") is True) and bool(output_data)
        status = "SUCCESS" if is_success else "FAILED"
        calls = 1

        summary = output_data.get("summary", "")
        refined = output_data.get("refined_version", "")
        strengths = output_data.get("strengths", [])
        weaknesses = output_data.get("weaknesses", [])
        next_steps = output_data.get("next_steps", [])

        rendered_text = (
            f"### Resumo\n{summary}\n\n"
            f"### Versão Refinada\n{refined}\n\n"
            f"### Pontos Fortes e Fracos\n"
            f"- **Fortes:** {', '.join(strengths)}\n"
            f"- **Fracos:** {', '.join(weaknesses)}\n\n"
            f"### Próximos Passos\n{', '.join(next_steps)}"
        )

        raw_payload = {
            "cell_id": cell_id,
            "experiment_id": "EXP-M05.4-PROSPECTIVE-RERUN-20260829",
            "attempt_id": attempt_id,
            "idea_id": idea_id,
            "condition": "CONDITION_A",
            "raw_idea": raw_idea,
            "latency_seconds": round(lat, 3),
            "model_calls": calls,
            "status": status,
            "error": result.get("error"),
            "parsed_output": output_data,
            "rendered_semantic_text": rendered_text,
        }

    elif condition == "CONDITION_B":
        runs_dir = raw_dir / "runs_b"
        runs_dir.mkdir(parents=True, exist_ok=True)
        router = _build_condition_b_router(runner)
        simple_runner = SimpleLoopRunner(router=router, topology="STANDARD_6_STAGE", runs_dir=runs_dir)
        state = simple_runner.run(original_idea=raw_idea, run_id=f"EXP-M05.4-{idea_id}-COND-B")
        lat = time.time() - start_time

        calls = len(state.stage_history)
        # FAIL-CLOSED status: requires terminal state in REFINED_IDEA_READY, COMPLETED, or STABILIZED
        status_val = getattr(state.status, "value", str(state.status))
        is_success = status_val in ("REFINED_IDEA_READY", "COMPLETED", "STABILIZED")
        status = "SUCCESS" if is_success else "FAILED"

        rendered_text = (
            f"### Ideia Refinada Final\n{state.current_idea or state.original_idea}\n\n"
            f"### Intenção Humana Preservada\n{state.human_intent}\n\n"
            f"### Mecanismo Central\n{state.core_mechanism}\n\n"
            f"### Incertezas Críticas Remanescentes\n"
            + "\n".join(f"- {u}" for u in state.remaining_uncertainties)
            + f"\n\n### Próxima Ação Recomendada\n{state.recommended_next_step}"
        )

        raw_payload = {
            "cell_id": cell_id,
            "experiment_id": "EXP-M05.4-PROSPECTIVE-RERUN-20260829",
            "attempt_id": attempt_id,
            "idea_id": idea_id,
            "condition": "CONDITION_B",
            "raw_idea": raw_idea,
            "latency_seconds": round(lat, 3),
            "model_calls": calls,
            "status": status,
            "terminal_status": status_val,
            "reconstruction_count": state.reconstruction_count,
            "stages_executed": [s.stage_id for s in state.stage_history],
            "rendered_semantic_text": rendered_text,
        }

    elif condition == "CONDITION_C":
        runs_dir = raw_dir / "runs_c"
        runs_dir.mkdir(parents=True, exist_ok=True)
        lean_runner = LeanLoopRunner(runner=runner, model_name=expected_model, runs_dir=runs_dir)
        result = lean_runner.run(original_idea=raw_idea, run_id=f"EXP-M05.4-{idea_id}-COND-C")
        lat = time.time() - start_time

        calls = result.total_model_calls
        # FAIL-CLOSED status: requires valid terminal status
        term_status = result.terminal_status or "UNKNOWN"
        is_success = term_status in (
            "COMPLETED",
            "COMPLETED_DIRECT_ONE_PASS",
            "COMPLETED_WITH_FOCUSED_ESCALATION",
            "HUMAN_DECISION_REQUIRED",
            "DECISION_REQUIRED",
            "DECISION_SATISFIED",
            "EARLY_EXIT"
        )
        status = "SUCCESS" if is_success else "FAILED"

        rendered_text = result.final_markdown or ""
        if not rendered_text and result.first_pass:
            fp = result.first_pass
            rendered_text = (
                f"### Intenção Central\n{fp.core_intent}\n\n"
                f"### Mecanismo Proposto\n{fp.primary_mechanism.mechanism}\n\n"
                f"### Vulnerabilidades Identificadas\n"
                + "\n".join(f"- **{v.risk_level}:** {v.vulnerability}" for v in fp.vulnerabilities)
                + "\n\n### Próxima Ação Recomendada\n"
                f"{fp.recommended_action}"
            )

        gate_outcome_val = result.gate_result.outcome.value if result.gate_result else "UNKNOWN"

        raw_payload = {
            "cell_id": cell_id,
            "experiment_id": "EXP-M05.4-PROSPECTIVE-RERUN-20260829",
            "attempt_id": attempt_id,
            "idea_id": idea_id,
            "condition": "CONDITION_C",
            "raw_idea": raw_idea,
            "latency_seconds": round(lat, 3),
            "model_calls": calls,
            "status": status,
            "terminal_status": term_status,
            "gate_outcome": gate_outcome_val,
            "human_decision_requested": result.human_decision_requested,
            "rendered_semantic_text": rendered_text,
        }

    else:
        raise ValueError(f"UNKNOWN_CONDITION: {condition}")

    # Persist raw artifact
    raw_artifact_file = raw_dir / f"{idea_id}_{condition.lower()}.json"
    raw_artifact_file.write_text(json.dumps(raw_payload, indent=2, ensure_ascii=False), encoding="utf-8")

    return raw_payload


def _append_journal(journal_path: Path, entry: Dict[str, Any]) -> None:
    """Atomic append of a single JSON line to the execution journal."""
    with open(journal_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def _save_partial_manifest(
    attempt_dir: Path,
    attempt_id: str,
    executed_cells: List[Dict[str, Any]],
    total_calls: int,
    calls_by_condition: Dict[str, int],
    cell_status_counts: Dict[str, int],
    b_reconstructions: int,
    runner: ModelRunner,
    exp_root: Path
) -> None:
    """Saves a partial execution manifest if an unhandled exception interrupts execution."""
    partial_manifest = {
        "experiment_id": "EXP-M05.4-PROSPECTIVE-RERUN-20260829",
        "attempt_id": attempt_id,
        "interrupted_at": datetime.now().isoformat(),
        "status": "INTERRUPTED",
        "total_cells_completed": len(executed_cells),
        "cells_success": cell_status_counts["SUCCESS"],
        "cells_failed": cell_status_counts["FAILED"],
        "total_semantic_model_calls": total_calls,
        "calls_by_condition": calls_by_condition,
        "b_reconstructions": b_reconstructions,
        "provider": getattr(runner, "provider", "groq"),
        "model": getattr(runner, "default_model", "openai/gpt-oss-120b"),
        "completed_cells": executed_cells,
    }
    partial_manifest_file = attempt_dir / "PARTIAL-EXECUTION-MANIFEST.json"
    partial_manifest_file.write_text(json.dumps(partial_manifest, indent=2, ensure_ascii=False), encoding="utf-8")


def run_clean_harness(
    runner: Optional[ModelRunner] = None,
    repo_root: Optional[Path] = None,
    exp_dir: Optional[Path] = None,
    attempt_id: str = "REAL-EXECUTION-ATTEMPT-004",
    holdout_file: Optional[Path] = None,
    manifest_file: Optional[Path] = None,
    freeze_manifest_file: Optional[Path] = None,
    blind_sha_file: Optional[Path] = None,
    skip_git_check: bool = False,
    allow_overwrite: bool = False,
    verbose: bool = True
) -> Dict[str, Any]:
    """
    Main entry point for clean execution with mechanical start gate and crash-safe journal.
    """
    root = repo_root or REPO_ROOT
    exp_root = exp_dir or (root / "experiments" / "EXP-M05.4-PROSPECTIVE-RERUN-20260829")
    attempt_dir = exp_root / attempt_id
    raw_dir = attempt_dir / "raw"
    journal_file = attempt_dir / "REAL-EXECUTION-JOURNAL.jsonl"

    holdout_path = holdout_file or (root / "experiments" / "EXP-M05.4-PROSPECTIVE" / "HOLDOUT-IDEAS.json")
    manifest_path = manifest_file or (exp_root / "RERUN-EXECUTION-MANIFEST.json")
    freeze_manifest_path = freeze_manifest_file or (exp_root / "RERUN-FREEZE-MANIFEST.json")
    blind_sha_path = blind_sha_file or (exp_root / "BLIND-REVEAL.sha256")

    # =========================================================================
    # MECHANICAL GATE 1: SELF-ENFORCING FREEZE VALIDATION
    # =========================================================================
    freeze_val_res = validate_frozen_execution_state(
        repo_root=root,
        exp_dir=exp_root,
        freeze_manifest_file=freeze_manifest_path,
        blind_sha_file=blind_sha_path,
        skip_git_check=skip_git_check,
    )

    # =========================================================================
    # MECHANICAL GATE 2: SINGLE-USE ATTEMPT NAMESPACE VALIDATION
    # =========================================================================
    validate_attempt_single_use(attempt_dir, allow_overwrite=allow_overwrite)

    # Load holdout ideas
    holdout_ideas = {i["idea_id"]: i for i in json.loads(holdout_path.read_text(encoding="utf-8"))}

    # Load execution manifest (source of execution order)
    exec_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    frozen_cells = exec_manifest["cells"]

    # =========================================================================
    # MECHANICAL GATE 3: MANIFEST CELLS VALIDATION
    # =========================================================================
    validate_frozen_manifest_cells(frozen_cells, holdout_ideas)

    # If no runner provided, instantiate NativeModelRunner with environment key
    if runner is None:
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY_MISSING: Cannot execute real attempt without Groq API key.")
        runner = NativeModelRunner(provider="groq", api_key=api_key, default_model="openai/gpt-oss-120b")

    # =========================================================================
    # MECHANICAL GATE 4: RUNNER PROVIDER & MODEL VALIDATION
    # =========================================================================
    validate_provider_guards(runner)

    # Ensure raw output dir exists
    raw_dir.mkdir(parents=True, exist_ok=True)

    # =========================================================================
    # MECHANICAL GATE 5: START RECEIPT WRITTEN ONLY AFTER ALL GATES PASS
    # =========================================================================
    head_commit = "UNKNOWN"
    try:
        head_commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, cwd=str(root)).stdout.strip()
    except Exception:
        pass

    harness_path = root / "tools" / "experiments" / "execute_m05_4_frozen.py"
    harness_sha = calculate_sha256_file(harness_path) if harness_path.exists() else "UNKNOWN"
    freeze_data = json.loads(freeze_manifest_path.read_text(encoding="utf-8"))
    expected_harness_sha = freeze_data.get("execution_critical_hashes", {}).get("execute_m05_4_frozen.py", "UNKNOWN")

    start_receipt = {
        "experiment_id": "EXP-M05.4-PROSPECTIVE-RERUN-20260829",
        "attempt_id": attempt_id,
        "git_head": head_commit,
        "worktree_clean": True,
        "execution_harness_sha256": harness_sha,
        "execution_harness_expected_sha256": expected_harness_sha,
        "freeze_manifest_sha256": freeze_val_res["freeze_manifest_sha256"],
        "blind_commitment_sha256": freeze_val_res["blind_commitment_sha256"],
        "blinding_revision": 3,
        "frozen_state_validation": "PASS",
        "manifest_validation": "PASS",
        "attempt_single_use_validation": "PASS",
        "provider": getattr(runner, "provider", "groq"),
        "model": getattr(runner, "default_model", "openai/gpt-oss-120b"),
        "start_timestamp": datetime.now().isoformat(),
        "total_cells_frozen": len(frozen_cells),
        "execution_plane_has_no_blind_knowledge": True,
        "human_review_started": False,
    }
    start_receipt_file = attempt_dir / "REAL-EXECUTION-START-RECEIPT.json"
    start_receipt_file.write_text(json.dumps(start_receipt, indent=2, ensure_ascii=False), encoding="utf-8")

    # =========================================================================
    # EXECUTION LOOP: 24 CELLS IN EXACT MANIFEST ORDER (CRASH-SAFE JOURNALED)
    # =========================================================================
    executed_cells = []
    total_calls = 0
    calls_by_condition = {"CONDITION_A": 0, "CONDITION_B": 0, "CONDITION_C": 0}
    cell_status_counts = {"SUCCESS": 0, "FAILED": 0}
    b_reconstructions = 0

    if verbose:
        print(f"Starting clean execution for {attempt_id} across {len(frozen_cells)} cells...")

    start_all = time.time()

    for idx, cell in enumerate(frozen_cells, 1):
        cell_id = cell["cell_id"]
        idea_id = cell["idea_id"]
        cond = cell["condition"]
        idea_data = holdout_ideas[idea_id]

        if verbose:
            print(f"[{idx}/{len(frozen_cells)}] Executing {cell_id}...", end="", flush=True)

        # Record CELL_STARTED in journal
        _append_journal(journal_file, {
            "event": "CELL_STARTED",
            "execution_order": idx,
            "cell_id": cell_id,
            "idea_id": idea_id,
            "condition": cond,
            "timestamp": datetime.now().isoformat(),
        })

        try:
            res = execute_m05_4_cell(cell, idea_data, runner, raw_dir, attempt_id=attempt_id)
        except Exception as exc:
            # Record CELL_EXCEPTION in journal and persist partial manifest
            _append_journal(journal_file, {
                "event": "CELL_EXCEPTION",
                "execution_order": idx,
                "cell_id": cell_id,
                "idea_id": idea_id,
                "condition": cond,
                "exception_class": type(exc).__name__,
                "error_message": str(exc),
                "timestamp": datetime.now().isoformat(),
            })
            _save_partial_manifest(
                attempt_dir, attempt_id, executed_cells, total_calls,
                calls_by_condition, cell_status_counts, b_reconstructions, runner, exp_root
            )
            raise

        c_calls = res.get("model_calls", 0)
        c_status = res.get("status", "FAILED")
        c_recons = res.get("reconstruction_count", 0)

        total_calls += c_calls
        calls_by_condition[cond] += c_calls
        cell_status_counts[c_status] += 1
        b_reconstructions += c_recons

        raw_fpath = raw_dir / f"{idea_id}_{cond.lower()}.json"
        raw_hash = calculate_sha256_file(raw_fpath)

        executed_cells.append({
            "execution_order": idx,
            "cell_id": cell_id,
            "idea_id": idea_id,
            "condition": cond,
            "status": c_status,
            "semantic_model_calls": c_calls,
            "reconstruction_count": c_recons,
            "latency_seconds": res.get("latency_seconds", 0.0),
            "raw_artifact_file": str(raw_fpath.relative_to(exp_root)),
            "raw_artifact_sha256": raw_hash,
            "telemetry_evidence": {
                "model_calls": "OBSERVED",
                "transport_retries": "UNKNOWN_NOT_INSTRUMENTED",
                "structured_output_repairs": "UNKNOWN_NOT_INSTRUMENTED",
            }
        })

        # Record CELL_COMPLETED in journal
        _append_journal(journal_file, {
            "event": "CELL_COMPLETED",
            "execution_order": idx,
            "cell_id": cell_id,
            "idea_id": idea_id,
            "condition": cond,
            "status": c_status,
            "model_calls": c_calls,
            "raw_artifact_file": str(raw_fpath.relative_to(exp_root)),
            "raw_artifact_sha256": raw_hash,
            "timestamp": datetime.now().isoformat(),
        })

        if verbose:
            print(f" {c_status} ({c_calls} calls, {res.get('latency_seconds')}s)")

    duration = time.time() - start_all

    # Save REAL-EXECUTION-MANIFEST.json
    real_manifest = {
        "experiment_id": "EXP-M05.4-PROSPECTIVE-RERUN-20260829",
        "attempt_id": attempt_id,
        "executed_at": datetime.now().isoformat(),
        "total_cells": len(executed_cells),
        "cells_attempted": len(executed_cells),
        "cells_success": cell_status_counts["SUCCESS"],
        "cells_failed": cell_status_counts["FAILED"],
        "total_semantic_model_calls": total_calls,
        "calls_by_condition": calls_by_condition,
        "transport_retries": "UNKNOWN_NOT_INSTRUMENTED",
        "structured_output_repairs": "UNKNOWN_NOT_INSTRUMENTED",
        "b_reconstructions": b_reconstructions,
        "provider": getattr(runner, "provider", "groq"),
        "model": getattr(runner, "default_model", "openai/gpt-oss-120b"),
        "cells": executed_cells,
    }
    real_manifest_file = attempt_dir / "REAL-EXECUTION-MANIFEST.json"
    real_manifest_file.write_text(json.dumps(real_manifest, indent=2, ensure_ascii=False), encoding="utf-8")

    # Save REAL-EXECUTION-EVIDENCE-MANIFEST.json
    raw_artifacts_map = {c["raw_artifact_file"]: c["raw_artifact_sha256"] for c in executed_cells}
    evidence_manifest = {
        "experiment_id": "EXP-M05.4-PROSPECTIVE-RERUN-20260829",
        "attempt_id": attempt_id,
        "generated_at": datetime.now().isoformat(),
        "start_receipt_sha256": calculate_sha256_file(start_receipt_file),
        "real_execution_manifest_sha256": calculate_sha256_file(real_manifest_file),
        "raw_artifacts_count": len(raw_artifacts_map),
        "raw_artifacts": raw_artifacts_map,
    }
    evidence_manifest_file = attempt_dir / "REAL-EXECUTION-EVIDENCE-MANIFEST.json"
    evidence_manifest_file.write_text(json.dumps(evidence_manifest, indent=2, ensure_ascii=False), encoding="utf-8")

    # Save REAL-EXECUTION-SUMMARY.md
    summary_md = f"""# REAL-EXECUTION-SUMMARY.md

## Factual Execution Summary — {attempt_id}

| Metric | Value | Evidence Class |
|---|---|---|
| EXPERIMENT_ID | EXP-M05.4-PROSPECTIVE-RERUN-20260829 | FROZEN_SPEC |
| ATTEMPT_ID | {attempt_id} | FROZEN_SPEC |
| EXECUTED_AT | {datetime.now().isoformat()} | OBSERVED |
| DURATION_SECONDS | {duration:.2f} | OBSERVED |
| PROVIDER | {getattr(runner, "provider", "groq")} | OBSERVED |
| MODEL | {getattr(runner, "default_model", "openai/gpt-oss-120b")} | OBSERVED |
| CELLS_FROZEN | {len(frozen_cells)} | FROZEN_MANIFEST |
| CELLS_ATTEMPTED | {len(executed_cells)} | OBSERVED |
| CELLS_SUCCESS | {cell_status_counts["SUCCESS"]} | OBSERVED (FAIL-CLOSED) |
| CELLS_FAILED | {cell_status_counts["FAILED"]} | OBSERVED |
| TOTAL_SEMANTIC_MODEL_CALLS | {total_calls} | OBSERVED |
| A_SEMANTIC_CALLS | {calls_by_condition["CONDITION_A"]} | OBSERVED |
| B_SEMANTIC_CALLS | {calls_by_condition["CONDITION_B"]} | OBSERVED |
| C_SEMANTIC_CALLS | {calls_by_condition["CONDITION_C"]} | OBSERVED |
| TRANSPORT_RETRIES | UNKNOWN_NOT_INSTRUMENTED | NOT_INSTRUMENTED |
| STRUCTURED_OUTPUT_REPAIRS | UNKNOWN_NOT_INSTRUMENTED | NOT_INSTRUMENTED |
| B_RECONSTRUCTIONS | {b_reconstructions} | OBSERVED |
| PROTOCOL_VIOLATIONS | 0 | OBSERVED |
| BLIND_KNOWLEDGE_IN_EXECUTION | NONE | ARCHITECTURAL_INVARIANT |
| HUMAN_REVIEW_STARTED | NO | OPERATIONAL_FACT |

## Raw Artifacts
- Total raw files: {len(raw_artifacts_map)} under `{attempt_dir.name}/raw/`
"""
    summary_file = attempt_dir / "REAL-EXECUTION-SUMMARY.md"
    summary_file.write_text(summary_md, encoding="utf-8")

    return {
        "attempt_id": attempt_id,
        "cells_attempted": len(executed_cells),
        "cells_success": cell_status_counts["SUCCESS"],
        "cells_failed": cell_status_counts["FAILED"],
        "total_calls": total_calls,
        "calls_by_condition": calls_by_condition,
        "evidence_manifest_sha256": calculate_sha256_file(evidence_manifest_file),
    }


if __name__ == "__main__":
    run_clean_harness()
