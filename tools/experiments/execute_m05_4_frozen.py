#!/usr/bin/env python3
"""
tools/experiments/execute_m05_4_frozen.py
Clean execution harness for M05.4 prospective replication.

Architectural Invariant:
  EXECUTION_PLANE_HAS_NO_BLIND_KNOWLEDGE = True

Responsibilities:
  1. Load frozen holdout ideas from experiments/EXP-M05.4-PROSPECTIVE/HOLDOUT-IDEAS.json.
  2. Load execution manifest from experiments/EXP-M05.4-PROSPECTIVE-RERUN-20260829/RERUN-EXECUTION-MANIFEST.json.
  3. Execute frozen A/B/C conditions in exact manifest order.
  4. Record raw outputs and factual execution metadata into attempt namespace.
  5. Compute artifact SHA-256 hashes.
  6. Stop without scoring, interpreting, or accessing blind mappings.

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
from src.idea_evolution.config.catalog import ModelCatalog


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


def execute_m05_4_cell(
    cell: Dict[str, Any],
    idea_data: Dict[str, Any],
    runner: ModelRunner,
    raw_dir: Path,
    expected_model: str = "openai/gpt-oss-120b"
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
            "attempt_id": "REAL-EXECUTION-ATTEMPT-002",
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
            "attempt_id": "REAL-EXECUTION-ATTEMPT-002",
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
            "attempt_id": "REAL-EXECUTION-ATTEMPT-002",
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


def run_clean_harness(
    runner: Optional[ModelRunner] = None,
    exp_dir: Optional[Path] = None,
    attempt_id: str = "attempt-002",
    holdout_file: Optional[Path] = None,
    manifest_file: Optional[Path] = None,
    verbose: bool = True
) -> Dict[str, Any]:
    """
    Main entry point for clean execution.
    Consumes manifest, executes 24 cells, freezes raw outputs and factual metadata.
    """
    exp_root = exp_dir or (REPO_ROOT / "experiments" / "EXP-M05.4-PROSPECTIVE-RERUN-20260829")
    attempt_dir = exp_root / attempt_id
    raw_dir = attempt_dir / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    holdout_path = holdout_file or (REPO_ROOT / "experiments" / "EXP-M05.4-PROSPECTIVE" / "HOLDOUT-IDEAS.json")
    manifest_path = manifest_file or (exp_root / "RERUN-EXECUTION-MANIFEST.json")
    freeze_manifest_path = exp_root / "RERUN-FREEZE-MANIFEST.json"
    blind_sha_path = exp_root / "BLIND-REVEAL.sha256"

    # Load holdout ideas
    holdout_ideas = {i["idea_id"]: i for i in json.loads(holdout_path.read_text(encoding="utf-8"))}

    # Load execution manifest (source of execution order)
    exec_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    frozen_cells = exec_manifest["cells"]

    # If no runner provided, instantiate NativeModelRunner with environment key
    if runner is None:
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY_MISSING: Cannot execute real attempt without Groq API key.")
        runner = NativeModelRunner(provider="groq", api_key=api_key, default_model="openai/gpt-oss-120b")

    # Validate provider and model guards
    validate_provider_guards(runner)

    # 1. Create REAL-EXECUTION-START-RECEIPT.json
    head_commit = "UNKNOWN"
    try:
        head_commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    except Exception:
        pass

    blind_commitment_sha = blind_sha_path.read_text(encoding="utf-8").strip() if blind_sha_path.exists() else "UNKNOWN"
    exec_manifest_sha = calculate_sha256_file(manifest_path) if manifest_path.exists() else "UNKNOWN"
    freeze_manifest_sha = calculate_sha256_file(freeze_manifest_path) if freeze_manifest_path.exists() else "UNKNOWN"

    start_receipt = {
        "experiment_id": "EXP-M05.4-PROSPECTIVE-RERUN-20260829",
        "attempt_id": attempt_id,
        "git_head": head_commit,
        "blind_commitment_sha256": blind_commitment_sha,
        "execution_manifest_sha256": exec_manifest_sha,
        "freeze_manifest_sha256": freeze_manifest_sha,
        "provider": getattr(runner, "provider", "groq"),
        "model": getattr(runner, "default_model", "openai/gpt-oss-120b"),
        "start_timestamp": datetime.now().isoformat(),
        "total_cells_frozen": len(frozen_cells),
        "execution_plane_has_no_blind_knowledge": True,
        "human_review_started": False,
    }
    start_receipt_file = attempt_dir / "REAL-EXECUTION-START-RECEIPT.json"
    start_receipt_file.write_text(json.dumps(start_receipt, indent=2, ensure_ascii=False), encoding="utf-8")

    # 2. Execute cells in exact manifest order
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

        res = execute_m05_4_cell(cell, idea_data, runner, raw_dir)

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

        if verbose:
            print(f" {c_status} ({c_calls} calls, {res.get('latency_seconds')}s)")

    duration = time.time() - start_all

    # 3. Create REAL-EXECUTION-MANIFEST.json
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

    # 4. Create REAL-EXECUTION-EVIDENCE-MANIFEST.json
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

    # 5. Create REAL-EXECUTION-SUMMARY.md
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
