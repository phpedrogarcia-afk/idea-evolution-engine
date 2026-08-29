"""
tools/experiments/execute_m05_4_pilot_01.py
Orchestrator for M05.4 Treatment-Delivery Pilot 01.

Executes 6 cells sequentially across 2 calibration ideas:
  CAL-01-CONDITION_A
  CAL-01-CONDITION_B
  CAL-01-CONDITION_C
  CAL-02-CONDITION_A
  CAL-02-CONDITION_B
  CAL-02-CONDITION_C

Zero blinding. Zero human quality review.
"""

from typing import Dict, Any, List, Optional
import os
import sys
import json
import time
import hashlib
from pathlib import Path
from datetime import datetime

from src.idea_evolution.providers.base import ModelRunner
from src.idea_evolution.providers.native import NativeModelRunner
from src.idea_evolution.orchestration.baseline import BaselineRunner
from src.idea_evolution.orchestration.simple_loop import SimpleLoopRunner
from src.idea_evolution.orchestration.lean_loop import LeanLoopRunner
from src.idea_evolution.providers.router import RunnerRouter
from src.idea_evolution.config.routing import ModelRoutingConfig, ModelDefinition

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
PILOT_DIR = REPO_ROOT / "experiments" / "EXP-M05.4-PROSPECTIVE-RERUN-20260829" / "treatment-delivery-pilot-01"


def calculate_sha256_file(path: Path) -> str:
    data = path.read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha256(data).hexdigest()


def _build_condition_b_router(runner: ModelRunner) -> RunnerRouter:
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


def _append_journal(journal_path: Path, entry: Dict[str, Any]) -> None:
    with open(journal_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def execute_pilot(runner: Optional[ModelRunner] = None, verbose: bool = True) -> Dict[str, Any]:
    PILOT_DIR.mkdir(parents=True, exist_ok=True)
    raw_dir = PILOT_DIR / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    journal_path = PILOT_DIR / "PILOT-JOURNAL.jsonl"

    cal_ideas_path = PILOT_DIR / "CALIBRATION-IDEAS.json"
    if not cal_ideas_path.is_file():
        raise RuntimeError("CALIBRATION_IDEAS_MISSING: CALIBRATION-IDEAS.json not found.")

    cal_ideas = {i["idea_id"]: i for i in json.loads(cal_ideas_path.read_text(encoding="utf-8"))}

    if runner is None:
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY_MISSING: Cannot execute pilot without Groq API key.")
        runner = NativeModelRunner(provider="groq", api_key=api_key, default_model="openai/gpt-oss-120b")

    planned_cells = [
        {"cell_id": "CAL-01-CONDITION_A", "idea_id": "CAL-01", "condition": "CONDITION_A"},
        {"cell_id": "CAL-01-CONDITION_B", "idea_id": "CAL-01", "condition": "CONDITION_B"},
        {"cell_id": "CAL-01-CONDITION_C", "idea_id": "CAL-01", "condition": "CONDITION_C"},
        {"cell_id": "CAL-02-CONDITION_A", "idea_id": "CAL-02", "condition": "CONDITION_A"},
        {"cell_id": "CAL-02-CONDITION_B", "idea_id": "CAL-02", "condition": "CONDITION_B"},
        {"cell_id": "CAL-02-CONDITION_C", "idea_id": "CAL-02", "condition": "CONDITION_C"},
    ]

    executed_cells: List[Dict[str, Any]] = []
    total_semantic_calls = 0
    calls_by_cond = {"CONDITION_A": 0, "CONDITION_B": 0, "CONDITION_C": 0}
    delivery_counts = {"DELIVERED": 0, "PARTIALLY_DELIVERED": 0, "NOT_DELIVERED": 0}

    if verbose:
        print(f"=== INITIATING M05.4 TREATMENT-DELIVERY PILOT 01 ({len(planned_cells)} cells) ===")

    start_pilot_time = time.time()

    for idx, cell in enumerate(planned_cells, 1):
        cell_id = cell["cell_id"]
        idea_id = cell["idea_id"]
        cond = cell["condition"]
        raw_idea = cal_ideas[idea_id]["raw_idea"]

        if verbose:
            print(f"[{idx}/6] Executing {cell_id}...", end="", flush=True)

        _append_journal(journal_path, {
            "event": "CELL_STARTED",
            "cell_id": cell_id,
            "idea_id": idea_id,
            "condition": cond,
            "timestamp": datetime.now().isoformat(),
        })

        cell_start = time.time()

        if cond == "CONDITION_A":
            runs_dir = raw_dir / "runs_a"
            runs_dir.mkdir(parents=True, exist_ok=True)
            baseline = BaselineRunner(runner=runner, model_name="openai/gpt-oss-120b")
            res = baseline.run(original_idea=raw_idea, run_id=f"PILOT-{idea_id}-COND-A", runs_dir=runs_dir)
            lat = time.time() - cell_start

            output_data = res.get("parsed_output") or {}
            success = (res.get("success") is True) and bool(output_data)
            calls = 1
            term_status = "SUCCESS" if success else "FAILED"

            # Delivery classification
            refined_text = output_data.get("refined_version", "")
            if success and len(refined_text.strip()) > 50:
                delivery_class = "DELIVERED"
            else:
                delivery_class = "NOT_DELIVERED"

            cell_payload = {
                "cell_id": cell_id,
                "idea_id": idea_id,
                "condition": cond,
                "latency_seconds": round(lat, 3),
                "model_calls": calls,
                "status": "SUCCESS" if success else "FAILED",
                "terminal_status": term_status,
                "delivery_class": delivery_class,
                "error": res.get("error"),
                "candidate_present": bool(refined_text.strip()),
                "parsed_output": output_data,
            }

        elif cond == "CONDITION_B":
            runs_dir = raw_dir / "runs_b"
            runs_dir.mkdir(parents=True, exist_ok=True)
            router = _build_condition_b_router(runner)
            simple_runner = SimpleLoopRunner(router=router, topology="STANDARD_6_STAGE", runs_dir=runs_dir)
            state = simple_runner.run(original_idea=raw_idea, run_id=f"PILOT-{idea_id}-COND-B")
            lat = time.time() - cell_start

            calls = len(state.stage_history)
            status_val = getattr(state.status, "value", str(state.status))
            stages_executed = [s.stage_id for s in state.stage_history]

            candidate_text = state.current_idea or ""
            has_candidate = bool(candidate_text.strip()) and len(candidate_text.strip()) > 50

            if status_val in ("REFINED_IDEA_READY", "COMPLETED", "STABILIZED") and has_candidate:
                delivery_class = "DELIVERED"
            elif status_val == "REFINEMENT_INCOMPLETE" and has_candidate:
                delivery_class = "PARTIALLY_DELIVERED"
            else:
                delivery_class = "NOT_DELIVERED"

            cell_payload = {
                "cell_id": cell_id,
                "idea_id": idea_id,
                "condition": cond,
                "latency_seconds": round(lat, 3),
                "model_calls": calls,
                "status": "SUCCESS" if delivery_class in ("DELIVERED", "PARTIALLY_DELIVERED") else "FAILED",
                "terminal_status": status_val,
                "delivery_class": delivery_class,
                "reconstruction_count": state.reconstruction_count,
                "stages_executed": stages_executed,
                "candidate_present": has_candidate,
            }

        elif cond == "CONDITION_C":
            runs_dir = raw_dir / "runs_c"
            runs_dir.mkdir(parents=True, exist_ok=True)
            lean_runner = LeanLoopRunner(runner=runner, model_name="openai/gpt-oss-120b", runs_dir=runs_dir)
            lean_res = lean_runner.run(original_idea=raw_idea, run_id=f"PILOT-{idea_id}-COND-C")
            lat = time.time() - cell_start

            calls = lean_res.total_model_calls
            term_status = lean_res.terminal_status or "UNKNOWN"
            has_first_pass = lean_res.first_pass is not None

            if term_status in (
                "COMPLETED", "COMPLETED_DIRECT_ONE_PASS", "COMPLETED_WITH_FOCUSED_ESCALATION",
                "HUMAN_DECISION_REQUIRED", "DECISION_REQUIRED", "DECISION_SATISFIED", "EARLY_EXIT"
            ) and has_first_pass:
                delivery_class = "DELIVERED"
            else:
                delivery_class = "NOT_DELIVERED"

            cell_payload = {
                "cell_id": cell_id,
                "idea_id": idea_id,
                "condition": cond,
                "latency_seconds": round(lat, 3),
                "model_calls": calls,
                "status": "SUCCESS" if delivery_class == "DELIVERED" else "FAILED",
                "terminal_status": term_status,
                "delivery_class": delivery_class,
                "gate_outcome": lean_res.gate_result.outcome.value if lean_res.gate_result else "UNKNOWN",
                "human_decision_requested": lean_res.human_decision_requested,
                "candidate_present": has_first_pass,
            }

        else:
            raise ValueError(f"Unknown condition: {cond}")

        # Write raw cell json
        raw_cell_file = raw_dir / f"{idea_id}_{cond.lower()}.json"
        raw_cell_file.write_text(json.dumps(cell_payload, indent=2, ensure_ascii=False), encoding="utf-8")

        total_semantic_calls += calls
        calls_by_cond[cond] += calls
        delivery_counts[delivery_class] = delivery_counts.get(delivery_class, 0) + 1
        executed_cells.append(cell_payload)

        _append_journal(journal_path, {
            "event": "CELL_COMPLETED",
            "cell_id": cell_id,
            "delivery_class": delivery_class,
            "terminal_status": cell_payload.get("terminal_status"),
            "model_calls": calls,
            "latency_seconds": round(lat, 3),
            "timestamp": datetime.now().isoformat(),
        })

        if verbose:
            print(f" -> {delivery_class} ({cell_payload.get('terminal_status')}, {calls} calls, {lat:.1f}s)")

        # Short pause between cells
        time.sleep(1.5)

    # Assess overall verdict
    a_delivered = sum(1 for c in executed_cells if c["condition"] == "CONDITION_A" and c["delivery_class"] == "DELIVERED")
    b_delivered_or_partial = sum(1 for c in executed_cells if c["condition"] == "CONDITION_B" and c["delivery_class"] in ("DELIVERED", "PARTIALLY_DELIVERED"))
    c_delivered = sum(1 for c in executed_cells if c["condition"] == "CONDITION_C" and c["delivery_class"] == "DELIVERED")

    all_delivered_cleanly = (a_delivered == 2) and (b_delivered_or_partial == 2) and (c_delivered == 2)
    verdict = "END_TO_END_TREATMENT_DELIVERY_PROVEN_ON_CALIBRATION" if all_delivered_cleanly else "END_TO_END_TREATMENT_DELIVERY_NOT_YET_PROVEN"

    manifest_payload = {
        "pilot_id": "M05.4-TREATMENT-DELIVERY-PILOT-01",
        "timestamp": datetime.now().isoformat(),
        "total_duration_seconds": round(time.time() - start_pilot_time, 2),
        "total_cells_planned": len(planned_cells),
        "total_cells_completed": len(executed_cells),
        "total_semantic_model_calls": total_semantic_calls,
        "calls_by_condition": calls_by_cond,
        "delivery_counts": delivery_counts,
        "a_delivered_count": a_delivered,
        "b_delivered_or_partial_count": b_delivered_or_partial,
        "c_delivered_count": c_delivered,
        "verdict": verdict,
        "cells": executed_cells,
    }

    manifest_path = PILOT_DIR / "PILOT-MANIFEST.json"
    manifest_path.write_text(json.dumps(manifest_payload, indent=2, ensure_ascii=False), encoding="utf-8")

    # Generate evidence manifest
    evidence_items = {}
    for p in sorted(PILOT_DIR.rglob("*")):
        if p.is_file() and p.name != "PILOT-EVIDENCE-MANIFEST.json":
            rel_path = str(p.relative_to(PILOT_DIR)).replace("\\", "/")
            evidence_items[rel_path] = {
                "sha256": calculate_sha256_file(p),
                "size_bytes": p.stat().st_size,
            }

    evidence_manifest = {
        "pilot_id": "M05.4-TREATMENT-DELIVERY-PILOT-01",
        "generated_at": datetime.now().isoformat(),
        "total_files": len(evidence_items),
        "files": evidence_items,
    }
    (PILOT_DIR / "PILOT-EVIDENCE-MANIFEST.json").write_text(
        json.dumps(evidence_manifest, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # Write human summary markdown
    summary_md = [
        "# PILOT-SUMMARY.md — M05.4 Treatment-Delivery Pilot 01 Summary\n",
        f"- **Pilot ID:** `M05.4-TREATMENT-DELIVERY-PILOT-01`",
        f"- **Verdict:** `{verdict}`",
        f"- **Cells Completed:** `{len(executed_cells)} / {len(planned_cells)}`",
        f"- **Total Semantic Calls:** `{total_semantic_calls} / 26 max`",
        f"- **Calls by Condition:** A={calls_by_cond['CONDITION_A']}, B={calls_by_cond['CONDITION_B']}, C={calls_by_cond['CONDITION_C']}",
        f"- **Delivery Status:** A: {a_delivered}/2 DELIVERED, B: {b_delivered_or_partial}/2 DELIVERED/PARTIAL, C: {c_delivered}/2 DELIVERED\n",
        "## Cell Breakdown\n",
        "| Cell ID | Condition | Status | Terminal Status | Delivery Class | Calls | Latency |",
        "|---|---|---|---|---|---|---|",
    ]
    for c in executed_cells:
        summary_md.append(
            f"| `{c['cell_id']}` | `{c['condition']}` | `{c['status']}` | `{c.get('terminal_status')}` | `{c['delivery_class']}` | {c['model_calls']} | {c['latency_seconds']}s |"
        )

    (PILOT_DIR / "PILOT-SUMMARY.md").write_text("\n".join(summary_md) + "\n", encoding="utf-8")

    return manifest_payload


if __name__ == "__main__":
    execute_pilot(verbose=True)
